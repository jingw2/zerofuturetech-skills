---
name: zft-skill-creator
description: Scaffold a complete new skill folder (SKILL.md, references/, scripts/, agents/) from a user's description of what they want the skill to do, automatically classifying the skill into one of nine canonical types and applying best practices from the Thariq skill-building guide. Use when a user says "create a skill for X", "make me a new skill", "scaffold a skill that does Y", or "help me build a skill".
---

Scaffold a new skill from a description by classifying it into one of nine types and generating the complete file structure following zft-skill conventions.

This skill owns: type classification, file tree generation, SKILL.md template, reference stubs, agent files.
This skill does not own: domain knowledge of the new skill, script logic, post-creation testing.

Read [references/skill-type-catalog.md](references/skill-type-catalog.md) for the nine types and selection criteria.
Read [references/section-contract.md](references/section-contract.md) for SKILL.md section rules.
Read [references/description-examples.md](references/description-examples.md) for description field patterns.

Workflow:

1. Normalize the input
- Accept: natural language description, bullet list, type + topic, or existing folder to regenerate
- Resolve: skill name (kebab-case), display name, skill type, whether scripts/ needed

2. Classify the skill type
- Match description to one of nine types using skill-type-catalog.md
- If ambiguous, present top two candidates and ask user to choose

3. Generate the SKILL.md
- Follow section order from section-contract.md exactly
- description field: verb phrase start, "Use when" trigger, model-facing not summary

4. Generate reference files
- Create 2-3 stubs under references/ with TODO markers
- Link every file from the Overview section

5. Generate agents and scripts
- Always generate agents/openai.yaml with all three fields
- Generate Python script stub if skill type benefits from automation (standard library only)
- Generate platforms/claude/agents/<name>.md as compact ~50-line version

6. Register and validate
- Print alias registration instructions for install-skill.mjs
- Self-check: all expected files exist, frontmatter valid, references linked

Quality bar:

- All required SKILL.md sections present in correct order
- description starts with verb phrase and includes "Use when"
- Workflow step 1 normalizes input
- Gotchas has at least three skeleton subsections
- openai.yaml has all three fields
- Claude agent file under 60 lines
- No generated Python script imports third-party packages
