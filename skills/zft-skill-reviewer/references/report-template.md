# Review Report Template

Read this file when generating the structured review report in step 6 of the review workflow. Fill in each section with findings from the audit.

## Template

---

# Skill Review: `<skill-name>`

**Overall Score**: X.X / 5.0
**Review Date**: YYYY-MM-DD

## Summary

<2-3 sentences. State the overall quality level, the most important strength, and the most important improvement area.>

## Structural Audit

| Item | Status | Notes |
|------|--------|-------|
| SKILL.md exists | ✅ / ❌ | |
| frontmatter valid | ✅ / ⚠️ / ❌ | name and description fields present |
| name matches directory | ✅ / ❌ | |
| Overview | ✅ / ⚠️ / ❌ | |
| What This Skill Owns | ✅ / ⚠️ / ❌ | |
| Workflow | ✅ / ⚠️ / ❌ | step 1 normalizes input? |
| Commands | ✅ / ⚠️ / N/A | |
| Frontmatter Contract | ✅ / ⚠️ / ❌ | |
| Quality Bar | ✅ / ⚠️ / ❌ | |
| Output Modes | ✅ / ⚠️ / ❌ | |
| Gotchas | ✅ / ⚠️ / ❌ | subsection count |
| references/ exists | ✅ / ❌ | |
| all references linked | ✅ / ⚠️ / ❌ | orphaned files if ⚠️ |
| agents/openai.yaml | ✅ / ⚠️ / ❌ | |
| Claude agent file | ✅ / ❌ | |

Legend: ✅ pass · ⚠️ warning · ❌ fail · N/A not applicable

## Content Quality

### Description Assessment

**Score**: X / 5

**Findings**:
- <finding 1>
- <finding 2>

**Rewrite suggestion** (if score < 3):
```
<suggested description rewrite>
```

### Gotchas Assessment

**Score**: X / 5
**Subsection count**: N
**Entries with TODO markers**: N

**Findings**:
- <finding>

### Progressive Disclosure

**Score**: X / 5

**Orphaned reference files**: <none / list>
**Sections exceeding 30 lines**: <none / list>

### Anti-Pattern Findings

| Anti-Pattern | Present | Severity | Evidence |
|---|---|---|---|
| Stating the Obvious | Yes / No | Critical / Important / Nice-to-have | <section> |
| Railroading | Yes / No | | <section> |
| Empty Gotchas | Yes / No | | |
| Monolithic SKILL.md | Yes / No | | |
| Summary-as-Description | Yes / No | | |
| Missing Trigger Conditions | Yes / No | | |
| Generic Quality Bar | Yes / No | | |
| Orphaned References | Yes / No | | |

## Scores by Criterion

| Criterion | Score | Key Evidence |
|---|---|---|
| 1. Structure Completeness | X / 5 | |
| 2. Description Quality | X / 5 | |
| 3. Workflow Quality | X / 5 | |
| 4. Gotchas Depth | X / 5 | |
| 5. Progressive Disclosure | X / 5 | |
| 6. Avoiding Obvious Statements | X / 5 | |
| 7. Scripts Quality | X / 5 or N/A | |
| 8. Agent Files Quality | X / 5 | |
| **Overall** | **X.X / 5.0** | |

## Top 3 Priority Improvements

1. **<Improvement title>** — <Specific, actionable description. Reference the exact section to change. Include a concrete example of the fix.>

2. **<Improvement title>** — <Specific, actionable description.>

3. **<Improvement title>** — <Specific, actionable description.>

## Detailed Findings

<Optional: per-section notes for findings not captured above.>

---

## Batch Report Table (for --all mode)

Use this table as the opening of a batch report before any per-skill drill-downs:

| Skill | Score | Critical | Important | Top Issue |
|---|---|---|---|---|
| skill-name-1 | X.X | N | N | <one-line top issue> |
| skill-name-2 | X.X | N | N | <one-line top issue> |
| ... | | | | |
