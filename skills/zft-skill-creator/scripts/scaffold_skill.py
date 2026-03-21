#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys
from pathlib import Path

SKILL_TYPES = [
    "library",
    "verification",
    "data",
    "automation",
    "scaffolding",
    "quality",
    "cicd",
    "runbook",
    "infrastructure",
]

SKILL_TYPE_LABELS = {
    "library": "Library & API Reference",
    "verification": "Product Verification",
    "data": "Data Fetching & Analysis",
    "automation": "Business Process & Team Automation",
    "scaffolding": "Code Scaffolding & Templates",
    "quality": "Code Quality & Review",
    "cicd": "CI/CD & Deployment",
    "runbook": "Runbooks",
    "infrastructure": "Infrastructure Operations",
}

TYPES_WITH_SCRIPTS = {"verification", "data", "scaffolding", "quality", "cicd", "runbook", "infrastructure"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a new skill folder following zft-skill conventions."
    )
    parser.add_argument(
        "description",
        nargs="?",
        help="Natural language description of the skill to create",
    )
    parser.add_argument(
        "--name",
        help="Skill name in kebab-case (inferred from description if omitted)",
    )
    parser.add_argument(
        "--type",
        choices=SKILL_TYPES,
        help="Skill type (one of: " + ", ".join(SKILL_TYPES) + ")",
    )
    parser.add_argument(
        "--output-dir",
        default="skills",
        help="Parent directory where the skill folder will be created (default: skills/)",
    )
    parser.add_argument(
        "--include-scripts",
        action="store_true",
        default=None,
        help="Force inclusion of a scripts/ stub",
    )
    parser.add_argument(
        "--no-scripts",
        action="store_true",
        help="Skip scripts/ generation even for types that normally include it",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt for each decision interactively",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created without writing files",
    )
    return parser.parse_args()


def slugify(text: str) -> str:
    """Convert a string to kebab-case."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def infer_name(description: str) -> str:
    """Infer a skill name from a description (rough heuristic)."""
    words = description.lower().split()
    # Take first 4 meaningful words, drop filler
    stopwords = {"a", "an", "the", "that", "which", "to", "for", "of", "in", "on", "at", "with"}
    meaningful = [w for w in words if w not in stopwords][:4]
    return slugify("-".join(meaningful))


def display_name(skill_name: str) -> str:
    return " ".join(w.capitalize() for w in skill_name.split("-"))


def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"  [dry-run] would write: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  created: {path}")


def generate_skill_md(name: str, skill_type: str, description: str) -> str:
    type_label = SKILL_TYPE_LABELS.get(skill_type, skill_type)
    dname = display_name(name)
    return f"""---
name: {name}
description: TODO: Replace this with a verb phrase describing what the skill does. Use when a user asks to [specific trigger conditions that distinguish this skill from similar ones].
---

# {dname}

## Overview

TODO: 2-4 sentences describing what this skill does.
This is a **{type_label}** skill.

Read [references/reference-1.md](references/reference-1.md) for TODO.
Read [references/reference-2.md](references/reference-2.md) for TODO.

## What This Skill Owns

This skill owns:

- TODO: list owned responsibilities

This skill does not own:

- TODO: list explicitly excluded responsibilities

## Workflow

### 1. Normalize the input

Accept:

- TODO: list accepted input forms

Resolve:

- TODO: list fields to resolve from input

### 2. TODO: Second step

TODO: describe the second workflow step.

### 3. TODO: Third step

TODO: describe the third workflow step.

## Commands

```bash
# TODO: add real command examples
python3 scripts/{slugify(name)}.py input.md
python3 scripts/{slugify(name)}.py input.md --dry-run
```

## Frontmatter Contract

Preferred frontmatter:

```yaml
---
title: TODO
summary: TODO
---
```

## Quality Bar

Before delivering, check:

- TODO: add specific, checkable quality criteria

## Output Modes

- **TODO mode**: description
- **TODO full mode**: description

## Gotchas

### TODO Category 1

- **TODO gotcha**: explanation and resolution.

### TODO Category 2

- **TODO gotcha**: explanation and resolution.

### TODO Category 3

- **TODO gotcha**: explanation and resolution.
"""


def generate_openai_yaml(name: str) -> str:
    dname = display_name(name)
    return f"""interface:
  display_name: "{dname}"
  short_description: "TODO: verb phrase under 10 words"
  default_prompt: "Use ${name} to TODO: one-sentence default action."
"""


def generate_reference_stub(filename: str, purpose: str) -> str:
    title = " ".join(w.capitalize() for w in filename.replace(".md", "").split("-"))
    return f"""# {title}

Read this file when TODO: {purpose}.

## TODO Section

TODO: add content here.

## TODO Section 2

TODO: add content here.
"""


def generate_script_stub(name: str) -> str:
    func_name = name.replace("-", "_")
    return f"""#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TODO: one-line description of what this script does."
    )
    parser.add_argument("input", help="TODO: describe the input")
    parser.add_argument("--output-dir", help="Output directory (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # TODO: implement main logic here
    print(f"Processing: {{args.input}}")

    if args.dry_run:
        print("[dry-run] would write output files")
        return

    # TODO: write output files
    output_dir = Path(args.output_dir) if args.output_dir else Path(".")
    output_dir.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()
"""


def generate_claude_agent(name: str, skill_type: str) -> str:
    dname = display_name(name)
    type_label = SKILL_TYPE_LABELS.get(skill_type, skill_type)
    return f"""---
name: {name}
description: TODO: Replace with the same description as SKILL.md. Use when TODO: trigger conditions.
---

TODO: one-line purpose of this skill.

This is a **{type_label}** skill.

This skill owns: TODO list.
This skill does not own: TODO list.

Workflow:

1. Normalize the input
- Accept: TODO input types
- Resolve: TODO fields

2. TODO step 2
- TODO key points

3. TODO step 3
- TODO key points

Quality bar:

- TODO checkable criterion
- TODO checkable criterion
"""


def scaffold(args: argparse.Namespace) -> None:
    description = args.description or ""

    if args.interactive:
        if not description:
            description = input("Describe what the skill should do: ").strip()
        if not args.name:
            suggested = infer_name(description)
            answer = input(f"Skill name [{suggested}]: ").strip()
            args.name = answer or suggested
        if not args.type:
            print("Skill types: " + ", ".join(SKILL_TYPES))
            args.type = input("Skill type: ").strip()

    name = args.name or infer_name(description) or "my-new-skill"
    skill_type = args.type or "library"

    include_scripts = args.include_scripts or (skill_type in TYPES_WITH_SCRIPTS and not args.no_scripts)

    output_dir = Path(args.output_dir) / name

    print(f"\nScaffolding skill: {name}")
    print(f"  Type: {SKILL_TYPE_LABELS.get(skill_type, skill_type)}")
    print(f"  Output: {output_dir}")
    print(f"  Scripts: {'yes' if include_scripts else 'no'}")
    print()

    if not args.dry_run and output_dir.exists():
        answer = input(f"  WARNING: {output_dir} already exists. Overwrite? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            sys.exit(0)

    files = {}

    files[output_dir / "SKILL.md"] = generate_skill_md(name, skill_type, description)
    files[output_dir / "agents" / "openai.yaml"] = generate_openai_yaml(name)
    files[output_dir / "references" / "reference-1.md"] = generate_reference_stub("reference-1.md", "describe purpose 1")
    files[output_dir / "references" / "reference-2.md"] = generate_reference_stub("reference-2.md", "describe purpose 2")

    if include_scripts:
        files[output_dir / "scripts" / f"{slugify(name)}.py"] = generate_script_stub(name)

    for path, content in files.items():
        write_file(path, content, args.dry_run)

    # Claude agent file goes in platforms/claude/agents/
    platforms_dir = Path(args.output_dir).parent / "platforms" / "claude" / "agents"
    claude_agent_path = platforms_dir / f"{name}.md"
    write_file(claude_agent_path, generate_claude_agent(name, skill_type), args.dry_run)

    print(f"\nScaffold complete.")
    print(f"\nNext steps:")
    print(f"  1. Fill in the TODO sections in {output_dir}/SKILL.md")
    print(f"  2. Replace the description field with a real trigger-oriented description")
    print(f"  3. Fill in references/ stub files with domain knowledge")
    if include_scripts:
        print(f"  4. Implement {output_dir}/scripts/{slugify(name)}.py")
    print(f"  5. Add alias to scripts/install-skill.mjs:")
    short_alias = name.split("-")[0]
    print(f'       {short_alias}: "{name}",')
    print(f"  6. Add to README.md Quick Install and Skills sections")


def main() -> None:
    args = parse_args()
    scaffold(args)


if __name__ == "__main__":
    main()
