# SKILL.md Section Contract

Read this file when generating the SKILL.md for a new skill. It defines the required section order, frontmatter rules, per-section constraints, and anti-patterns to avoid.

## Frontmatter

Every SKILL.md starts with a YAML frontmatter block with exactly two fields:

```yaml
---
name: <skill-name>
description: <single-line description>
---
```

**name constraints**:
- must exactly match the skill directory name
- kebab-case, all lowercase, no spaces, no underscores
- under 40 characters

**description constraints**:
- single-line string (no newlines)
- starts with a verb phrase (not "This skill...", not a noun phrase)
- contains "Use when" followed by concrete trigger conditions
- describes when to trigger, not what the skill contains
- should be specific enough to distinguish from similar skills

## Required Sections (in this order)

### 1. Overview

Purpose: orient Claude to the skill's purpose, link to reference files, list runnable scripts.

Rules:
- 2-4 sentences describing what the skill does
- link every reference file using relative markdown syntax: `[references/foo.md](references/foo.md)`
- list runnable scripts in a bullet list labeled "Runnable helper:" or "Runnable helpers:"
- do not repeat the frontmatter description verbatim

Anti-patterns:
- embedding reference content inline instead of linking to it
- omitting links to reference files (orphaned references)

### 2. What This Skill Owns

Purpose: define clear boundaries between this skill and related skills or tools.

Rules:
- two subsections: "This skill owns:" and "This skill does not own:"
- each is a short bullet list (3-6 items)
- be specific: "image provider dispatch" not "image handling"

Anti-patterns:
- vague ownership ("everything related to X")
- omitting the "does not own" section

### 3. Workflow

Purpose: describe the step-by-step process Claude should follow.

Rules:
- use numbered subsections: `### 1. Normalize the input`
- **Step 1 must always normalize the input**: list what forms of input are accepted, what fields are resolved
- each step should advance the workflow (not restate the previous step)
- give Claude flexibility to adapt within each step — avoid over-prescribing implementation details
- include conditional logic (if X, do Y) for common branching points

Anti-patterns:
- step 1 that is not input normalization
- steps that simply restate the previous step
- over-constraining with exact output formats in every step (railroading)
- more than 8 steps (split into sub-steps or simplify)

### 4. Commands

Purpose: show Claude the exact bash invocations for runnable scripts.

Rules:
- use a bash code block for each set of related commands
- show realistic arguments, not just `--help`
- include the most common usage patterns (2-5 examples)
- omit this section only if the skill has no scripts/

Anti-patterns:
- showing only `--help` without real examples
- showing commands that don't match the actual script arguments

### 5. Frontmatter Contract

Purpose: document what frontmatter fields the skill reads from input files.

Rules:
- show a YAML code block with example frontmatter
- list accepted values for each enum field
- mark required vs optional fields

Anti-patterns:
- listing every possible frontmatter field from all sources
- omitting accepted values for fields with a fixed set of options

### 6. Quality Bar

Purpose: a pre-delivery checklist Claude runs before outputting results.

Rules:
- bullet list of specific, checkable conditions
- each item should be verifiable (not "make sure the output is good")
- 4-8 items

Anti-patterns:
- vague items ("ensure quality")
- more than 10 items (becomes noise)

### 7. Output Modes

Purpose: describe the range of output fidelity from lightest to heaviest.

Rules:
- list modes from lightest to heaviest (2-4 modes)
- each mode has a short label and a one-line description
- end with a note about when to default to which mode

Anti-patterns:
- only one mode (add at least a dry-run or planning mode)
- modes that are identical except in name

### 8. Gotchas

Purpose: document real failure modes that Claude encounters when using this skill.

Rules:
- use `### Subsection Title` to group related gotchas
- each gotcha: `- **Bold problem statement**: explanation and resolution`
- gotchas must be specific (not "be careful with edge cases")
- add gotchas from real experience, not speculation
- minimum 3 subsections, minimum 2 gotchas each

Anti-patterns:
- empty skeleton gotchas ("TODO: add gotchas")
- generic warnings without specific failure modes
- gotchas that apply to every skill (not skill-specific)

## Optional Sections

Include these when relevant, inserted after Workflow and before Commands:

- **Architecture**: for skills with complex internal component boundaries
- **Configuration**: if the skill reads a config.json or EXTEND.md
- **Safety Boundary**: for skills that could generate sensitive or harmful output
- **Image Handling**: for image-generation skills

## General Anti-Patterns

- **Stating the obvious**: do not explain things Claude already knows (basic Python syntax, how to use git, what JSON is). Focus on non-obvious, skill-specific knowledge.
- **Railroading**: do not over-specify implementation details. Tell Claude the outcome to achieve, not the exact commands to run at each sub-step.
- **Monolithic SKILL.md**: if any section exceeds ~30 lines, move the detailed content to a reference file and link it from the Overview.
- **Orphaned references**: if a file exists in references/ but is not linked from the Overview, Claude will not know to read it at the right time.
