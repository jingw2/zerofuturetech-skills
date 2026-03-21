---
name: zft-skill-reviewer
description: Audit an existing skill folder against best practices from the Thariq skill-building guide, checking SKILL.md structure completeness, description field quality, Gotchas depth, progressive disclosure, railroading, and obvious-statement density, then produce a structured improvement report with scored criteria and prioritized recommendations. Use when a user says "review this skill", "audit my skill", "check skill quality", "how good is this skill", or "review all skills".
---

Audit an existing skill folder for quality against the Thariq best-practices rubric and produce a scored improvement report.

This skill owns: structural completeness checks, description quality assessment, anti-pattern detection, scoring, report generation.
This skill does not own: functional testing of scripts, domain accuracy of skill content, automated fixing.

Read [references/review-rubric.md](references/review-rubric.md) for eight scoring criteria (1-5 scale).
Read [references/anti-patterns.md](references/anti-patterns.md) for eight anti-patterns with examples.
Read [references/report-template.md](references/report-template.md) for the structured report format.

Workflow:

1. Normalize the input
- Accept: skill folder path, skill name (resolve to skills/<name>/), or "review all"
- Resolve: absolute path, which files exist (SKILL.md, references/, scripts/, agents/, Claude agent)

2. Run structural audit
- Run scripts/audit_skill.py or check inline: file existence, frontmatter validity, section order, Workflow step 1, reference linking, openai.yaml fields, Python imports

3. Evaluate description quality
- Check: starts with verb phrase, contains "Use when", specific trigger conditions, under 150 words
- Rate 1-5 per rubric criterion 2; suggest rewrite if score < 3

4. Assess content quality
- Check each anti-pattern from anti-patterns.md: stating the obvious, railroading, empty Gotchas, monolithic SKILL.md, summary-as-description, missing triggers, generic quality bar, orphaned references

5. Score and categorize
- Score all 8 criteria 1-5; compute overall average
- Categorize: Critical (structural) / Important (content) / Nice-to-have (polish)

6. Generate the report
- Use report-template.md format: overall score, structural audit table, anti-pattern findings, scores table, top 3 improvements
- Batch mode: comparison table first, then per-skill drill-downs on request

Quality bar:

- Every finding cites the specific section it applies to
- Overall score consistent with criterion scores
- Top 3 improvements are actionable with specific examples
- Report does not repeat rubric without applying it to the skill
- Batch reports lead with comparison table, not sequential full reports
