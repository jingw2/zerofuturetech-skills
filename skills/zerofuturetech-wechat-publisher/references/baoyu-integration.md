# Baoyu Integration

Use this file when handing the prepared article to `baoyu-post-to-wechat`.

## Role Split

This skill:

- cleans content
- chooses article type
- resolves metadata
- chooses a WeChat-friendly layout approach
- decides whether preview is needed before publish

`baoyu-post-to-wechat`:

- loads account settings
- resolves API/browser publish method
- uploads assets
- creates draft in WeChat Official Account

## Recommended Handoff Rules

- Keep Markdown as Markdown when possible.
- Do not pre-convert unless you have a clear reason and know the resulting HTML still behaves well in WeChat.
- Always resolve `title`, `summary`, `author`, and `cover` before handoff.
- Prefer explicit `--theme` and optional `--color` instead of relying on accidental defaults.

## Suggested Publish Commands

API path:

```bash
${BUN_X} {baoyuBaseDir}/scripts/wechat-api.ts <article.md> --theme <theme> --title <title> --summary <summary> --author <author> --cover <cover_path>
```

Browser path:

```bash
${BUN_X} {baoyuBaseDir}/scripts/wechat-article.ts --markdown <article.md> --theme <theme>
```

## Publishing Decision

Prefer `api` when:

- cover image is ready
- account credentials already exist
- the goal is fast draft upload

Prefer `browser` when:

- API credentials are unavailable
- article needs closer visual inspection during paste flow
- the user already relies on Chrome login workflow

## Pre-Publish Review

Before handoff, check:

- no duplicated title
- summary is present
- cover path exists
- image references are stable
- article type and theme match the content

If these are not true, fix them before publish instead of hoping the draft box will hide the problems.
