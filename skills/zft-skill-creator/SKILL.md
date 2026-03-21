---
name: zft-skill-creator
description: Scaffold a complete new skill folder (SKILL.md, references/, scripts/, agents/) from a user's description of what they want the skill to do, automatically classifying the skill into one of nine canonical types and applying best practices from the Thariq skill-building guide. Use when a user says "create a skill for X", "make me a new skill", "scaffold a skill that does Y", or "help me build a skill".
---

# ZFT Skill Creator

## Overview

Use this skill to create a new skill from scratch.
Give it a description of what the skill should do and it will scaffold the complete folder structure — SKILL.md, references/, scripts/, and agents/ — following the conventions used across this repository.

Read [references/skill-type-catalog.md](references/skill-type-catalog.md) to understand the nine canonical skill types and how to classify a new skill.
Read [references/section-contract.md](references/section-contract.md) for the exact SKILL.md section order, frontmatter rules, and per-section constraints.
Read [references/description-examples.md](references/description-examples.md) for good and bad description field examples with annotations.

Runnable helper:

- `scripts/scaffold_skill.py`: accept a description, classify the skill type, and write the complete file tree to disk

## What This Skill Owns

This skill owns:

- skill type classification (mapping a user's description to one of nine types)
- file tree generation (SKILL.md, references/, scripts/, agents/, Claude agent)
- template content for all generated files
- Gotchas skeleton and reference stubs for the user to iterate on

This skill does not own:

- the domain knowledge of the new skill being created
- Python script logic specific to the new skill's domain
- post-creation testing or validation of the new skill's behavior

## Workflow

### 1. Normalize the input

Accept any of:

- a natural language description ("I want a skill that deploys services to staging")
- a bullet list of desired capabilities
- a skill type name plus a topic ("scaffolding skill for database migrations")
- an existing broken skill folder to regenerate

Resolve:

- skill name: kebab-case, descriptive, under 40 characters
- display name: Title Case version of the skill name
- skill type: one of the nine types from `references/skill-type-catalog.md`
- primary platform: codex, openclaw, claude, or all
- whether scripts/ are needed (depends on skill type)
- number of reference files needed (typically 2-3)

If the description is vague, ask one clarifying question before proceeding.

### 2. Classify the skill type

Read `references/skill-type-catalog.md`.
Map the user's description to one of the nine types.

If the description clearly matches one type, proceed.
If it is ambiguous between two types, present both candidates with a one-sentence rationale for each and ask the user to choose.
Do not straddle two types in the generated skill.

The type influences the template:
- **Library & API Reference**: heavier references/, light or no scripts/
- **Product Verification**: strong Commands section, scripts/ with test-runner stub
- **Code Scaffolding & Templates**: template files in references/, generation script
- **Code Quality & Review**: rubric-style references/, optional lint script
- **Business Process & Team Automation**: workflow steps, log-file memory pattern
- **Data Fetching & Analysis**: credential config references, query-helper script
- **CI/CD & Deployment**: hooks section, deployment-step scripts
- **Runbooks**: symptom-to-tool mapping in references/, investigation script
- **Infrastructure Operations**: guardrail notes, destructive-action warnings in Gotchas

### 3. Generate the SKILL.md

Use the section order and constraints from `references/section-contract.md`.

Required sections in order:
1. Overview (link to reference files, list runnable scripts)
2. What This Skill Owns (owns / does not own)
3. Workflow (numbered steps, Step 1 always normalizes input)
4. Commands (bash code blocks showing script usage)
5. Frontmatter Contract (YAML block + accepted values)
6. Quality Bar (checklist of pre-delivery checks)
7. Output Modes (lightest to heaviest)
8. Gotchas (categorized subsections, specific failure modes)

Optional sections (include when relevant):
- Architecture (for skills with complex component boundaries)
- Configuration (if the skill has config.json or EXTEND.md)
- Safety Boundary (for skills that could produce harmful output)

The description field must follow the rules in `references/description-examples.md`:
- start with a verb phrase (not "This skill..." or a noun)
- include "Use when" with specific trigger conditions
- describe when the model should activate, not a feature summary
- keep the trigger conditions concrete enough to disambiguate from similar skills

### 4. Generate reference files

Create 2-3 reference files under `references/` based on the skill type.
Each reference file:
- has no YAML frontmatter
- starts with `# Title`
- has a second line explaining when to read this file ("Read this file when...")
- uses `## Section` headings for structure
- includes TODO markers for domain-specific content the user must fill in

Name reference files with kebab-case descriptive names (e.g., `api-reference.md`, `gotcha-patterns.md`, `template-catalog.md`).

Link every reference file from the Overview section of SKILL.md.

### 5. Generate agents and scripts

**agents/openai.yaml**: always generate with all three required fields:
```yaml
interface:
  display_name: "<Title Case Name>"
  short_description: "<verb phrase, under 10 words>"
  default_prompt: "Use $<skill-name> to <one-sentence default action>."
```

**scripts/**: generate a Python stub only if the skill type benefits from automation (verification, scaffolding, data fetching, CI/CD, runbooks, infrastructure). The stub must:
- use only Python standard library
- use argparse with meaningful argument names
- include a `main()` function called from `if __name__ == "__main__":`
- have TODO comments marking where domain logic goes
- not import any third-party packages

**platforms/claude/agents/<skill-name>.md**: generate a compact Claude agent file (~50 lines). Same frontmatter as SKILL.md but a compressed body: one-line purpose, What This Skill Owns list, Workflow steps as 2-line summaries, Quality Bar as a short checklist.

### 6. Register and validate

Print instructions for the user:
1. Add an alias to `scripts/install-skill.mjs` in the `skillAliases` object
2. Add the skill to README.md Quick Install and Skills sections

Run a self-check:
- all expected files exist
- SKILL.md has valid frontmatter (name and description)
- all reference files are linked from the Overview section
- openai.yaml has all three required fields
- scripts/ Python files import only standard library modules

Report any missing items as warnings, not errors.

## Commands

```bash
python3 scripts/scaffold_skill.py "A skill that deploys services to staging" --name deploy-staging
python3 scripts/scaffold_skill.py "Review PR quality against team standards" --type code-quality
python3 scripts/scaffold_skill.py "Automate the weekly engineering standup post" --output-dir ~/my-skills
python3 scripts/scaffold_skill.py --interactive
python3 scripts/scaffold_skill.py "fetch Grafana dashboards and summarize anomalies" --dry-run
```

## Frontmatter Contract

This skill generates SKILL.md files for new skills.
The generated frontmatter has two required fields:

```yaml
---
name: <kebab-case-skill-name>
description: <verb phrase>. Use when <specific trigger conditions>.
---
```

Accepted name values:
- kebab-case string matching the skill directory name exactly
- no spaces, no uppercase, no underscores

Accepted description values:
- single-line string (no newlines)
- starts with a verb phrase
- contains "Use when" followed by specific trigger conditions
- not a feature list or summary

## Quality Bar

Before delivering the scaffold, check:

- SKILL.md has all required sections in the correct order
- description starts with a verb phrase and includes "Use when"
- Workflow step 1 is "Normalize the input" or "Normalize the source"
- Gotchas section exists with at least three categorized subsections
- every reference file is linked from the Overview
- openai.yaml has display_name, short_description, and default_prompt
- Claude agent file exists and is under 60 lines
- no generated Python script imports a third-party package

## Output Modes

Use the lightest mode that satisfies the request:

- **Classification only**: tell the user which of the nine types fits and why
- **SKILL.md only**: generate just the main skill file without the full folder
- **Full scaffold**: complete directory with SKILL.md, references/, agents/, and optionally scripts/

Default to full scaffold unless the user asks for something lighter.

## Configuration

Optional config path: `.zerofuturetech-skills/zft-skill-creator/config.json`

```json
{
  "default_author": "Your Name",
  "default_platform": "all",
  "preferred_skill_prefix": "",
  "include_scripts": true
}
```

## Gotchas

### Naming Collisions

If the generated skill name matches an existing directory under `skills/`, the scaffold will overwrite existing files without warning.
Always check `ls skills/` before generating to confirm the name does not already exist.
If a collision is detected, ask the user to confirm or choose a different name.

### Description Field Written as a Summary

The most common mistake when generating new skills is writing the description as a feature list: "This skill does X, Y, and Z."
The description field is read by the model at session start to decide whether to activate the skill.
It must describe when to trigger, not what the skill contains.
If the generated description reads like a README paragraph, rewrite it using the formula in `references/description-examples.md`.

### SKILL.md Over-Stuffed with Inline Detail

New skill authors tend to put everything in SKILL.md.
If any section exceeds roughly 30 lines of prose, it likely belongs in a reference file instead.
Progressive disclosure matters: SKILL.md should tell Claude what to do and when to read the references, not contain the references themselves.

### Scripts with External Dependencies

Generated script stubs must use only Python standard library.
If the skill's domain logic needs requests, pandas, boto3, or similar packages, document this as a manual setup step in the Commands section.
Never import third-party packages in the generated stub because the script may be run in environments without those packages installed.

### Gotchas Section Left as Skeleton

The scaffold generates a skeleton Gotchas section with placeholder categories.
A skill deployed with only placeholder gotchas is missing its highest-signal content.
After using the skill for the first time, immediately return to SKILL.md and add at least one real failure mode from the actual experience.
