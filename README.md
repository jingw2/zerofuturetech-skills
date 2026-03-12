# Zero Future Tech Skills

Public skill registry for reusable Codex writing and workflow skills from Zero Future Tech.

## Skills

### `high-agency-x-essay-writer`

Write high-agency, contrarian long-form X/newsletter essays in English or Chinese without imitating any living author.

What it does:

- Drafts or rewrites long-form essays for X, newsletters, and idea-driven posts
- Uses strong hooks, clean argument spine, systems-thinking, and actionable endings
- Supports native-feeling Chinese adaptation instead of English-style literal translation
- Preserves a safe boundary: inspiration from public creator article patterns, not direct style imitation

Use it when:

- You have raw notes, a journal entry, an outline, or a half-formed argument
- You want a sharper thesis and stronger article structure
- You want separate English and Chinese versions of the same core idea

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

### Option 1: Copy locally

Copy a skill folder into your local Codex skills directory:

```bash
cp -R skills/high-agency-x-essay-writer ~/.codex/skills/
```

Or sync it:

```bash
rsync -a skills/high-agency-x-essay-writer/ ~/.codex/skills/high-agency-x-essay-writer/
```

### Option 2: Install with npm from GitHub

Install the repo as a package and copy the skill into `~/.codex/skills`:

```bash
npx github:jingw2/zerofuturetech-skills install high-agency-x-essay-writer
```

You can also install globally first:

```bash
npm install -g github:jingw2/zerofuturetech-skills
zerofuturetech-skills install high-agency-x-essay-writer
```

Optional target directory:

```bash
zerofuturetech-skills install high-agency-x-essay-writer --target ~/.codex/skills
```

## Conventions

- Each skill is self-contained under `skills/`
- `SKILL.md` is the source of truth
- `references/` stores on-demand guidance
- Keep repo-level docs minimal and skill-focused
