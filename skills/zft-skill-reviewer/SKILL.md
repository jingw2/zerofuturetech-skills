---
name: zft-skill-reviewer
description: Audit an existing skill folder against best practices from the Thariq skill-building guide, checking SKILL.md structure completeness, description field quality, Gotchas depth, progressive disclosure, railroading, and obvious-statement density, then produce a structured improvement report with scored criteria and prioritized recommendations. Use when a user says "review this skill", "audit my skill", "check skill quality", "how good is this skill", or "review all skills".
---

# ZFT Skill Reviewer

## Overview

Use this skill to audit an existing skill folder for quality and adherence to best practices.
It checks structure, content, and writing patterns against the rubric derived from the Thariq skill-building guide, then produces a scored report with actionable improvement priorities.

Read [references/review-rubric.md](references/review-rubric.md) for the eight scoring criteria and what scores of 1 and 5 look like for each.
Read [references/anti-patterns.md](references/anti-patterns.md) for the catalog of common skill anti-patterns with examples.
Read [references/report-template.md](references/report-template.md) for the structured report format to produce.

Runnable helper:

- `scripts/audit_skill.py`: perform deterministic structural checks on a skill folder and output findings as Markdown or JSON

## What This Skill Owns

This skill owns:

- structural completeness checks (file existence, section order, frontmatter validity)
- description field quality assessment (trigger-oriented vs summary-oriented)
- content quality assessment against the anti-patterns catalog
- scoring against the eight-criterion rubric
- structured improvement report generation

This skill does not own:

- functional testing of the skill's scripts
- domain accuracy of the skill's content (whether the domain knowledge is correct)
- automated fixing of identified issues (it recommends, it does not repair)

## Workflow

### 1. Normalize the input

Accept any of:

- a path to a skill folder (e.g., `skills/zerofuturetech-wechat-publisher`)
- a skill name (resolve to `skills/<name>/` in the repository)
- "review all" or `--all` to batch-audit every skill under `skills/`

Resolve:

- absolute path to the skill folder
- whether SKILL.md exists (if not, note as critical finding and continue)
- whether references/, scripts/, agents/openai.yaml exist
- whether a Claude agent file exists under `platforms/claude/agents/<name>.md`

### 2. Run structural audit

Run `scripts/audit_skill.py <skill-path>` or perform the checks inline.

Check in order:

- SKILL.md exists
- frontmatter parses correctly (valid YAML, name and description fields present)
- name field matches directory name
- description field is non-empty
- required sections present: Overview, What This Skill Owns, Workflow, Commands, Frontmatter Contract, Quality Bar, Output Modes, Gotchas
- sections appear in the canonical order
- Workflow step 1 mentions "normalize" or "input" in its heading
- references/ directory exists
- reference files linked from Overview (check for `[references/` in SKILL.md body)
- agents/openai.yaml exists with display_name, short_description, and default_prompt
- Python scripts in scripts/ import only standard library modules

Note every structural issue as a finding with severity: Critical, Important, or Nice-to-have.

### 3. Evaluate description quality

Apply the criteria from `references/review-rubric.md` (criterion 2: Description Quality).

Check:
- starts with a verb phrase (flag if starts with "This skill", a noun, or a feature list)
- contains "Use when" followed by at least one specific trigger condition
- trigger conditions are specific enough to distinguish this skill from similar ones
- description is not simply repeating the Overview text
- description is under ~150 words (longer descriptions often bury the trigger)

Rate the description on the 1-5 scale from the rubric.
Provide a specific rewrite suggestion if the description scores below 3.

### 4. Assess content quality

Read `references/anti-patterns.md` and check for each anti-pattern:

- **Stating the obvious**: flag sentences that explain things Claude already knows (basic programming concepts, well-known CLI usage). Consider whether the content corrects a known model weakness before flagging — not all "basic" content is obvious to the model.
- **Railroading**: flag workflow steps that prescribe exact commands or implementation details rather than outcomes. Steps like "run exactly this command with these flags" are railroading; "run the test suite and confirm all pass" is not.
- **Empty Gotchas**: check whether the Gotchas section has real, specific failure modes or just skeleton placeholders. Count subsections and entries. Flag if fewer than 3 subsections or if entries contain "TODO".
- **Progressive disclosure failure**: check whether SKILL.md is trying to contain all reference content inline. If any section exceeds ~30 lines of dense prose, it likely belongs in a reference file.
- **Orphaned references**: list all files in references/ and check whether each is linked from the Overview. Flag any that are not linked.

### 5. Score and categorize

Use the eight criteria from `references/review-rubric.md`. Score each 1-5.

Categorize all findings:
- **Critical**: structural issues that prevent the skill from functioning correctly (missing SKILL.md, invalid frontmatter, missing required sections)
- **Important**: content issues that significantly reduce skill effectiveness (bad description, empty Gotchas, railroading)
- **Nice-to-have**: polish issues that improve but are not essential (orphaned references, slightly over-stuffed sections)

Compute an overall score as the average of the eight criteria rounded to one decimal.

### 6. Generate the report

Use the template from `references/report-template.md`.

Output a Markdown report containing:
- skill name and overall score
- 2-3 sentence summary
- structural audit results as a table
- content quality findings per anti-pattern
- scores for all eight criteria as a table
- top 3 priority improvements (specific, actionable, not vague)
- optional: before/after example for the highest-impact improvement

For batch mode (--all): generate a comparison table first (skill name, overall score, critical count, top issue), then drill-down reports for each skill.

## Commands

```bash
python3 scripts/audit_skill.py skills/zerofuturetech-wechat-publisher
python3 scripts/audit_skill.py skills/high-agency-x-essay-writer --format json
python3 scripts/audit_skill.py --all
python3 scripts/audit_skill.py --all --output-dir reviews/
python3 scripts/audit_skill.py skills/zft-skill-creator --strict
```

## Frontmatter Contract

This skill reads the frontmatter of the skill being reviewed.
It expects:

```yaml
---
name: <skill-name>
description: <description string>
---
```

The `name` field is compared against the directory name.
The `description` field is analyzed for trigger-orientation and verb-phrase start.

## Quality Bar

Before delivering the review report, check:

- every finding cites the specific section or line it applies to
- the overall score is consistent with the individual criterion scores
- the top 3 improvements are actionable (not "make the description better")
- the report does not simply repeat the rubric criteria without applying them to the specific skill
- batch reports lead with a comparison table, not a dump of sequential full reports
- the review does not flag obvious-statement anti-patterns without considering whether the content corrects a known model weakness

## Output Modes

- **Quick check**: pass/fail on structural completeness only (missing files, missing sections, invalid frontmatter)
- **Full review**: scored rubric report with content quality findings and top 3 improvements
- **Batch report**: comparison table followed by per-skill full reviews, for all skills in the repository

Default to full review for a single skill. Use batch report when reviewing all skills.

## Gotchas

### Structural Checks on Skills Without SKILL.md

If the skill folder exists but has no SKILL.md, the audit script will handle this gracefully and report it as a critical structural finding.
It will not crash.
Continue the review by noting all missing files and recommend starting from scratch with zft-skill-creator.

### False Positives on Stating the Obvious

Some skills legitimately explain concepts that Claude gets wrong in that specific context.
A skill that explains WeChat-specific image upload behavior is not "stating the obvious" even if the underlying HTTP concept is basic — the domain-specific constraint is the non-obvious part.
Before flagging a passage as obvious, ask: "Would Claude get this wrong without the instruction?" If yes, it is not obvious.

### Section Order Is Not Perfectly Rigid

Not all skills require every section.
A pure writing skill (like high-agency-x-essay-writer) may legitimately omit Commands (no scripts) and Configuration (no config file).
Distinguish "missing because unnecessary" from "missing because forgotten" by checking whether the skill type logically requires the section.
Do not penalize a skill for omitting sections that its type genuinely does not need.

### Gotchas Quality Is Subjective

Two highly specific gotchas are better than eight generic ones.
When scoring Gotchas depth, weight specificity and actionability over count.
A Gotchas section with three entries that each describe a real failure mode with a resolution is a 4/5.
A section with ten entries that all say "be careful" is a 1/5.

### Batch Review Output Overload

When running --all, do not dump four or six full review reports sequentially.
Always lead with a comparison table that shows skill name, overall score, critical findings count, and the single most important improvement.
Let the user ask for the drill-down on a specific skill rather than presenting everything at once.

### Meta-Skill Review Circularity

Reviewing zft-skill-creator or zft-skill-reviewer requires understanding that meta-skills have different content patterns.
Their "Frontmatter Contract" section documents generated output schemas, not input frontmatter — this is intentional, not a deficiency.
Apply the rubric but do not flag meta-skill-specific patterns as anti-patterns.
