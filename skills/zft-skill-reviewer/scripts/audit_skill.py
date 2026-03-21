#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Overview",
    "What This Skill Owns",
    "Workflow",
    "Commands",
    "Frontmatter Contract",
    "Quality Bar",
    "Output Modes",
    "Gotchas",
]

STANDARD_LIBRARY_MODULES = {
    "abc", "argparse", "ast", "asyncio", "base64", "binascii", "builtins",
    "collections", "contextlib", "copy", "csv", "dataclasses", "datetime",
    "decimal", "difflib", "email", "enum", "fnmatch", "fractions", "functools",
    "glob", "gzip", "hashlib", "hmac", "html", "http", "importlib", "inspect",
    "io", "itertools", "json", "logging", "math", "mimetypes", "multiprocessing",
    "operator", "os", "pathlib", "pickle", "platform", "pprint", "queue", "random",
    "re", "shlex", "shutil", "signal", "socket", "sqlite3", "ssl", "stat",
    "string", "struct", "subprocess", "sys", "tempfile", "textwrap", "threading",
    "time", "traceback", "typing", "unicodedata", "unittest", "urllib", "uuid",
    "warnings", "weakref", "xml", "zipfile", "__future__",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Perform structural audit of a skill folder against zft-skill conventions."
    )
    parser.add_argument(
        "skill_path",
        nargs="?",
        help="Path to the skill folder to audit",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Audit all skills under skills/ directory",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--output-dir",
        help="Write reports to this directory instead of stdout",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures",
    )
    return parser.parse_args()


def parse_frontmatter(content: str) -> tuple:
    """Return (frontmatter_dict, body_text) or ({}, content) if no frontmatter."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end + 4:].strip()
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm, body


def find_sections(body: str) -> list:
    """Return list of (heading_text, line_number) for ## headings."""
    sections = []
    for i, line in enumerate(body.splitlines(), 1):
        if line.startswith("## "):
            sections.append((line[3:].strip(), i))
    return sections


def check_references_linked(body: str, references_dir: Path) -> tuple:
    """Return (all_linked, orphaned_files)."""
    if not references_dir.exists():
        return True, []
    ref_files = [f.name for f in references_dir.iterdir() if f.suffix == ".md"]
    orphaned = []
    for ref_file in ref_files:
        if f"references/{ref_file}" not in body:
            orphaned.append(ref_file)
    return len(orphaned) == 0, orphaned


def check_python_imports(scripts_dir: Path) -> list:
    """Return list of non-standard imports found in scripts/."""
    third_party = []
    if not scripts_dir.exists():
        return third_party
    for py_file in scripts_dir.glob("*.py"):
        content = py_file.read_text(encoding="utf-8", errors="ignore")
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("import ") or line.startswith("from "):
                module = line.split()[1].split(".")[0]
                if module not in STANDARD_LIBRARY_MODULES:
                    third_party.append(f"{py_file.name}: {line}")
    return third_party


def check_openai_yaml(yaml_path: Path) -> dict:
    """Check openai.yaml for required fields."""
    if not yaml_path.exists():
        return {"exists": False, "fields": []}
    content = yaml_path.read_text(encoding="utf-8", errors="ignore")
    fields = []
    for field in ["display_name", "short_description", "default_prompt"]:
        if field in content:
            fields.append(field)
    return {"exists": True, "fields": fields}


def count_gotchas(body: str) -> tuple:
    """Return (subsection_count, has_todos)."""
    sections = 0
    has_todos = False
    in_gotchas = False
    for line in body.splitlines():
        if line.startswith("## Gotchas"):
            in_gotchas = True
            continue
        if in_gotchas and line.startswith("## "):
            break
        if in_gotchas:
            if line.startswith("### "):
                sections += 1
            if "TODO" in line:
                has_todos = True
    return sections, has_todos


def audit_skill(skill_path: Path, strict: bool = False) -> dict:
    """Audit a single skill folder. Return findings dict."""
    findings = {
        "skill_name": skill_path.name,
        "skill_path": str(skill_path),
        "findings": [],
        "summary": {},
    }

    def add(severity: str, item: str, status: str, notes: str = ""):
        findings["findings"].append({
            "severity": severity,
            "item": item,
            "status": status,
            "notes": notes,
        })

    # 1. SKILL.md existence
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        add("critical", "SKILL.md exists", "fail", "File not found")
        findings["summary"]["critical"] = 1
        return findings

    add("info", "SKILL.md exists", "pass")

    content = skill_md.read_text(encoding="utf-8", errors="ignore")
    fm, body = parse_frontmatter(content)

    # 2. Frontmatter
    if not fm:
        add("critical", "frontmatter valid", "fail", "No YAML frontmatter found")
    else:
        add("info", "frontmatter valid", "pass")
        name_field = fm.get("name", "")
        desc_field = fm.get("description", "")
        if not name_field:
            add("critical", "name field", "fail", "name field missing or empty")
        elif name_field != skill_path.name:
            add("important", "name matches directory", "warn",
                f"name '{name_field}' does not match directory '{skill_path.name}'")
        else:
            add("info", "name matches directory", "pass")

        if not desc_field:
            add("critical", "description field", "fail", "description field missing or empty")
        else:
            add("info", "description field", "pass")
            if not desc_field[0].isupper() or desc_field.startswith("This skill") or desc_field.startswith("A "):
                add("important", "description verb phrase", "warn",
                    "description should start with a verb phrase, not 'This skill' or an article")
            if "Use when" not in desc_field:
                add("critical", "description trigger conditions", "fail",
                    "description missing 'Use when' clause")
            else:
                add("info", "description has 'Use when'", "pass")

    # 3. Required sections
    sections_found = find_sections(body)
    section_names = [s[0] for s in sections_found]

    for required in REQUIRED_SECTIONS:
        if required in section_names:
            add("info", f"section: {required}", "pass")
        else:
            severity = "critical" if required in ("Overview", "Workflow", "Gotchas") else "important"
            add(severity, f"section: {required}", "fail", "Section missing")

    # 4. Workflow step 1
    workflow_lines = []
    in_workflow = False
    for line in body.splitlines():
        if line.startswith("## Workflow"):
            in_workflow = True
            continue
        if in_workflow and line.startswith("## "):
            break
        if in_workflow:
            workflow_lines.append(line)
    first_step = next((l for l in workflow_lines if l.startswith("### 1.")), "")
    if first_step and ("normalize" in first_step.lower() or "input" in first_step.lower() or "source" in first_step.lower()):
        add("info", "workflow step 1 normalizes input", "pass")
    elif first_step:
        add("important", "workflow step 1 normalizes input", "warn",
            f"Step 1 is '{first_step}' — should normalize the input")
    else:
        add("important", "workflow step 1", "fail", "No numbered step 1 found in Workflow")

    # 5. References
    refs_dir = skill_path / "references"
    if refs_dir.exists():
        add("info", "references/ exists", "pass")
        all_linked, orphaned = check_references_linked(body, refs_dir)
        if all_linked:
            add("info", "all references linked", "pass")
        else:
            add("important", "all references linked", "warn",
                f"Orphaned: {', '.join(orphaned)}")
    else:
        add("important", "references/ exists", "warn", "No references/ directory")

    # 6. agents/openai.yaml
    yaml_result = check_openai_yaml(skill_path / "agents" / "openai.yaml")
    if not yaml_result["exists"]:
        add("important", "agents/openai.yaml", "fail", "File not found")
    else:
        add("info", "agents/openai.yaml exists", "pass")
        missing = [f for f in ["display_name", "short_description", "default_prompt"] if f not in yaml_result["fields"]]
        if missing:
            add("important", "openai.yaml fields", "warn", f"Missing fields: {', '.join(missing)}")
        else:
            add("info", "openai.yaml fields", "pass")

    # 7. Claude agent
    repo_root = skill_path.parent.parent
    claude_agent = repo_root / "platforms" / "claude" / "agents" / f"{skill_path.name}.md"
    if claude_agent.exists():
        add("info", "Claude agent file", "pass")
    else:
        add("nice-to-have", "Claude agent file", "warn",
            f"Not found at platforms/claude/agents/{skill_path.name}.md")

    # 8. Python imports
    third_party = check_python_imports(skill_path / "scripts")
    if third_party:
        add("important", "scripts standard library only", "warn",
            "Non-standard imports: " + "; ".join(third_party))
    elif (skill_path / "scripts").exists():
        add("info", "scripts standard library only", "pass")

    # 9. Gotchas depth
    gotcha_subsections, has_todos = count_gotchas(body)
    if gotcha_subsections == 0:
        add("critical", "gotchas subsections", "fail", "No ### subsections in Gotchas")
    elif gotcha_subsections < 3:
        add("important", "gotchas subsections", "warn",
            f"Only {gotcha_subsections} subsections (recommend 3+)")
    else:
        add("info", "gotchas subsections", "pass", f"{gotcha_subsections} subsections")
    if has_todos:
        add("important", "gotchas has TODO markers", "warn",
            "Gotchas section contains TODO placeholders — fill with real failure modes")

    # Summary counts
    findings["summary"] = {
        "critical": sum(1 for f in findings["findings"] if f["severity"] == "critical" and f["status"] in ("fail", "warn")),
        "important": sum(1 for f in findings["findings"] if f["severity"] == "important" and f["status"] in ("fail", "warn")),
        "nice_to_have": sum(1 for f in findings["findings"] if f["severity"] == "nice-to-have" and f["status"] in ("fail", "warn")),
        "passed": sum(1 for f in findings["findings"] if f["status"] == "pass"),
    }

    return findings


def format_markdown(findings: dict) -> str:
    lines = []
    name = findings["skill_name"]
    s = findings["summary"]
    lines.append(f"# Structural Audit: `{name}`\n")
    lines.append(f"Critical: {s.get('critical', 0)} | Important: {s.get('important', 0)} | "
                 f"Nice-to-have: {s.get('nice_to_have', 0)} | Passed: {s.get('passed', 0)}\n")
    lines.append("| Severity | Item | Status | Notes |")
    lines.append("|---|---|---|---|")
    for f in findings["findings"]:
        if f["status"] == "pass":
            continue
        icon = {"critical": "❌", "important": "⚠️", "nice-to-have": "💡", "info": "✅"}.get(f["severity"], "")
        lines.append(f"| {icon} {f['severity']} | {f['item']} | {f['status']} | {f['notes']} |")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()

    if args.all:
        # Find skills directory relative to this script
        script_dir = Path(__file__).parent
        skills_dir = script_dir.parent.parent / "skills"
        if not skills_dir.exists():
            skills_dir = Path("skills")
        skill_paths = sorted([p for p in skills_dir.iterdir() if p.is_dir()])
    elif args.skill_path:
        skill_paths = [Path(args.skill_path)]
    else:
        print("Error: provide a skill path or use --all", file=sys.stderr)
        sys.exit(1)

    all_findings = []
    for skill_path in skill_paths:
        result = audit_skill(skill_path, args.strict)
        all_findings.append(result)

    if args.format == "json":
        output = json.dumps(all_findings, indent=2, ensure_ascii=False)
        if args.output_dir:
            out_path = Path(args.output_dir) / "audit-results.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(output, encoding="utf-8")
            print(f"Written to {out_path}")
        else:
            print(output)
    else:
        if args.all and len(all_findings) > 1:
            # Batch summary table first
            print("# Skill Audit Summary\n")
            print("| Skill | Critical | Important | Nice-to-have | Passed |")
            print("|---|---|---|---|---|")
            for f in all_findings:
                s = f["summary"]
                print(f"| {f['skill_name']} | {s.get('critical', 0)} | {s.get('important', 0)} | "
                      f"{s.get('nice_to_have', 0)} | {s.get('passed', 0)} |")
            print()

        for result in all_findings:
            report = format_markdown(result)
            if args.output_dir:
                out_path = Path(args.output_dir) / f"{result['skill_name']}-audit.md"
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(report, encoding="utf-8")
                print(f"Written to {out_path}")
            else:
                print(report)
                print()


if __name__ == "__main__":
    main()
