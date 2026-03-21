# Review Rubric

Read this file when scoring a skill across the eight quality criteria. Each criterion is scored 1-5. The overall score is the average rounded to one decimal.

## How to Score

For each criterion: read the 1/5 anchors, then place the skill on the scale based on evidence from the skill folder. Cite specific sections or lines when assigning a score below 4.

---

## Criterion 1: Structure Completeness

**Definition**: All required sections are present and in the canonical order.

**Score 1**: SKILL.md is missing, or fewer than half the required sections are present, or sections are in a random order.

**Score 5**: All eight required sections present (Overview, What This Skill Owns, Workflow, Commands, Frontmatter Contract, Quality Bar, Output Modes, Gotchas), in the exact canonical order. Optional sections (Architecture, Configuration, Safety Boundary) are included when appropriate and excluded when not needed.

**Guiding questions**:
- Are any required sections absent?
- Are sections out of canonical order?
- Are optional sections present when they should not be (or absent when they should be)?

---

## Criterion 2: Description Quality

**Definition**: The description field is trigger-oriented, starts with a verb phrase, and contains specific "Use when" conditions.

**Score 1**: Description starts with "This skill", is a noun phrase, is a feature list, or has no "Use when" clause.

**Score 5**: Description starts with a verb phrase, contains "Use when" followed by at least two specific, distinguishing trigger conditions, and is specific enough to differentiate this skill from similar skills. Under 150 words.

**Guiding questions**:
- Does it start with a verb phrase?
- Does it contain "Use when"?
- Are the trigger conditions specific enough to prevent constant false triggering?
- Does it read like a model-facing trigger or a human-facing summary?

---

## Criterion 3: Workflow Quality

**Definition**: Workflow steps are additive, avoid railroading, and step 1 always normalizes input.

**Score 1**: Step 1 does not normalize input. Steps repeat the same information. Steps prescribe exact commands or implementation details at every sub-step (railroading). Fewer than 3 steps.

**Score 5**: Step 1 normalizes the input (lists accepted forms, resolves fields). Each subsequent step advances the workflow without repeating previous steps. Steps describe outcomes and constraints, not exact commands to run. 3-8 steps total.

**Guiding questions**:
- Does step 1 normalize input?
- Do steps build on each other or repeat?
- Are steps over-prescriptive about how (railroading) vs what to achieve?

---

## Criterion 4: Gotchas Depth

**Definition**: Gotchas section contains real, specific failure modes from actual usage, organized in categorized subsections.

**Score 1**: Gotchas section is absent, contains only TODO markers, or has generic warnings without specific failure modes ("be careful with edge cases").

**Score 5**: At least 3 subsections with thematic groupings. Each entry: bold problem statement + specific failure scenario + resolution. Entries describe real edge cases a user would actually encounter, not speculative risks. Specificity weighted over count.

**Guiding questions**:
- Does the Gotchas section exist?
- Do entries describe specific failure modes or generic warnings?
- Are there at least 3 subsections?
- Are any entries still TODO placeholders?

---

## Criterion 5: Progressive Disclosure

**Definition**: SKILL.md is a navigation document; reference files hold the detailed content; all reference files are linked from Overview.

**Score 1**: SKILL.md contains all reference content inline (no references/ directory, or references/ exists but nothing links to it). Or references/ files exist but are not linked from Overview (orphaned).

**Score 5**: SKILL.md sections are concise (none exceeds ~30 lines). All detailed content lives in references/ files. Every reference file is linked from the Overview section. No orphaned reference files.

**Guiding questions**:
- Are any SKILL.md sections excessively long (>30 lines)?
- Are all reference files linked from the Overview?
- Is there content in SKILL.md that belongs in a reference file?

---

## Criterion 6: Avoiding Obvious Statements

**Definition**: The skill focuses on information Claude does not already know, corrects known model weaknesses, and avoids explaining basic concepts.

**Score 1**: More than 20% of the content explains concepts Claude already knows without adding skill-specific constraints (e.g., "Python uses indentation", "JSON is a data format", "git is a version control system").

**Score 5**: Every instruction provides non-obvious, skill-specific guidance. When basic concepts appear, they are accompanied by skill-specific constraints that Claude would not infer on its own.

**Guiding questions**:
- Does any content explain things Claude already knows without adding context?
- Would Claude perform the step correctly without the instruction?
- Is the "obvious" content actually correcting a known model weakness in this domain?

---

## Criterion 7: Scripts Quality

**Definition**: Scripts are runnable, use only standard library, use argparse, and provide meaningful helper functions.

**Score 1**: Scripts exist but crash on `--help`. Scripts import third-party packages without documentation. Scripts have no argparse or meaningful structure.

**Score 5**: All scripts run without errors on `--help`. Standard library only. argparse with meaningful argument names and help text. `main()` function. `if __name__ == "__main__": main()`. Helper functions that Claude can reuse without modification.

**Score N/A**: Skip this criterion (exclude from average) if the skill type does not warrant scripts (Library & API Reference, Business Process skills without external calls).

**Guiding questions**:
- Do scripts run?
- Are third-party imports present?
- Is argparse used?
- Are there reusable helper functions?

---

## Criterion 8: Agent Files Quality

**Definition**: openai.yaml has all three required fields; Claude agent file is concise and self-contained.

**Score 1**: openai.yaml is missing or has fewer than three fields. Claude agent file is absent or exceeds 80 lines with redundant content.

**Score 5**: openai.yaml has display_name (Title Case), short_description (verb phrase, under 10 words), and default_prompt (starts with "Use $skill-name"). Claude agent file is 40-60 lines, covers workflow in compressed form, has the same description as SKILL.md.

**Guiding questions**:
- Does openai.yaml have all three fields?
- Is the Claude agent file under 60 lines?
- Does the Claude agent description match the SKILL.md description?
