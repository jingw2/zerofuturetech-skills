# Zero Future Tech Skills

Public skill registry for reusable Codex writing and workflow skills from Zero Future Tech.

## Skills

| Skill | Purpose | Status |
| --- | --- | --- |
| `high-agency-x-essay-writer` | Write high-agency, contrarian long-form X/newsletter essays in English or Chinese without imitating any living author | active |

## Structure

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/   # optional
    assets/    # optional
```

## Install

Copy a skill folder into your local Codex skills directory:

```bash
cp -R skills/high-agency-x-essay-writer ~/.codex/skills/
```

Or sync it:

```bash
rsync -a skills/high-agency-x-essay-writer/ ~/.codex/skills/high-agency-x-essay-writer/
```

## Conventions

- Each skill is self-contained under `skills/`
- `SKILL.md` is the source of truth
- `references/` stores on-demand guidance
- Keep repo-level docs minimal and skill-focused
