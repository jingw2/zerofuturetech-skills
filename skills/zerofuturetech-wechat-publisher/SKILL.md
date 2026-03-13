---
name: zerofuturetech-wechat-publisher
description: Prepare polished, WeChat-draft-ready articles from Markdown and image assets, then publish them to WeChat Official Account draft box by reusing baoyu-post-to-wechat as the publishing engine. Use when Codex receives a Markdown article, article images, cover image, or mixed writing assets and needs to optimize typography, spacing, headings, image rhythm, frontmatter, and WeChat metadata before sending the result to 微信公众号草稿箱.
---

# Zerofuturetech Wechat Publisher

## Overview

Turn a Markdown article plus optional images into a WeChat-optimized article draft that looks good inside 微信公众号草稿箱 rather than merely rendering without errors.
This skill is layout-first: it improves structure, Chinese typography, heading rhythm, image placement, and metadata before delegating final publishing to `baoyu-post-to-wechat`.

Read [references/wechat-layout-rules.md](references/wechat-layout-rules.md) for the layout rules, [references/article-prep.md](references/article-prep.md) for Markdown and image preparation, and [references/baoyu-integration.md](references/baoyu-integration.md) for the final publishing handoff.

Runnable helpers:

- `scripts/prepare_article.py`: clean Markdown, resolve cover/images, generate `cleaned.md`, `metadata.json`, and `preview.html`
- `scripts/publish_wechat.py`: read `metadata.json` and call `baoyu-post-to-wechat`

## Architecture

Use a two-layer model:

- This skill owns the preparation layer:
  - article cleanup
  - Markdown normalization
  - image and cover resolution
  - WeChat-specific layout choices
  - preview-oriented HTML expectations
- `baoyu-post-to-wechat` remains the publishing engine:
  - account config
  - API or browser delivery
  - draft box upload
  - WeChat credentials and Chrome profile handling

Do not reimplement WeChat transport unless the user explicitly asks for a standalone replacement.

## Workflow

### 1. Normalize the input package

Accept any of these forms:

- Markdown file path
- Markdown text pasted inline
- Markdown file plus image directory
- Markdown file plus explicit cover image path
- Markdown file with frontmatter containing `title`, `author`, `summary`, `cover`, `coverImage`, or `image`

Resolve these fields before layout work:

- article source
- article type: `essay`, `tutorial`, or `brief`
- style preset: `auto`, `minimal-cn`, `tech-editorial`, or `bold`
- title
- summary / digest
- cover image
- inline images
- publishing method preference: `api` or `browser`

If the input is raw text, save it to a Markdown file before proceeding.

### 2. Clean the Markdown before rendering

Apply these cleanup rules:

- Fix common Chinese Markdown spacing issues when they reduce readability
- Remove duplicated H1 title inside body if frontmatter already supplies title
- Convert noisy divider usage into cleaner section breaks
- Collapse empty paragraphs and accidental list spacing
- Keep code blocks only if the article is actually technical
- Preserve image references and captions
- If the article contains too many long paragraphs, suggest a split before publishing

### 3. Choose a WeChat layout mode

Pick one mode based on article type:

- `essay`: cleaner whitespace, stronger paragraph rhythm, restrained decorations
- `tutorial`: stronger H2/H3 hierarchy, better ordered steps, clearer callout blocks
- `brief`: compact sections, strong opening summary, tighter image spacing

Default to `essay` unless the source is obviously a tutorial or a short bulletin.

### 4. Optimize for WeChat draft appearance

Use the rules in [references/wechat-layout-rules.md](references/wechat-layout-rules.md). The short version:

- Avoid generic Markdown-renderer look
- Favor readable Chinese typography over decorative styling
- Keep H2 visually strong but not banner-heavy unless the user asks
- Make quotes, tips, and lists feel editorial rather than code-doc-like
- Control image rhythm so the article does not become text wall -> image dump -> text wall
- Treat cover image and summary as first-class publishing metadata

### 5. Hand off to `baoyu-post-to-wechat`

After content prep, publish through `baoyu-post-to-wechat` instead of bypassing it.

Preferred handoff:

1. Markdown input stays Markdown
2. Theme/color defaults are resolved intentionally, not left accidental
3. Cover image is confirmed before API publish
4. Use `baoyu-post-to-wechat` for final draft upload

If the article needs a custom HTML pass before publishing, ensure the HTML still remains compatible with WeChat draft rendering and image handling.

## Commands

Prepare an article:

```bash
python3 scripts/prepare_article.py article.md
python3 scripts/prepare_article.py article.md --cover imgs/cover.png --article-type tutorial
python3 scripts/prepare_article.py article.md --style tech-editorial
python3 scripts/prepare_article.py article.md --style auto --compare-styles
```

Publish a prepared article:

```bash
python3 scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --method api
python3 scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --method browser --dry-run
```

## Frontmatter Contract

Prefer these fields in article frontmatter:

```yaml
---
title: 文章标题
author: 作者名
summary: 一句话摘要
cover: imgs/cover.png
article_type: essay
wechat_theme: default
wechat_color: green
wechat_style: tech-editorial
---
```

Accepted cover aliases:

- `cover`
- `coverImage`
- `featureImage`
- `image`

Accepted article type values:

- `essay`
- `tutorial`
- `brief`

Accepted style values:

- `auto`
- `bold`
- `minimal-cn`
- `tech-editorial`

`auto` recommendation:

- `essay` -> `tech-editorial`
- `tutorial` -> `bold`
- `brief` -> `minimal-cn`

## Image Handling

Support both:

- cover image for the draft/article card
- inline images inside the Markdown body

Rules:

- Cover image should be distinct from body images when possible
- Prefer locally available image paths over remote URLs for publishing stability
- If the first inline image is being reused as cover, say so explicitly
- Preserve image captions if present; otherwise do not invent decorative captions

## Quality Bar

Before publishing, check:

- The title is not duplicated in body
- The opening screen does not look cramped in WeChat
- Heading hierarchy is obvious without looking noisy
- Paragraph spacing is comfortable on mobile
- Lists, quotes, and code blocks do not break the visual rhythm
- Cover image and summary are resolved
- The final workflow still uses `baoyu-post-to-wechat` for draft submission

## Output Modes

Use the lightest mode that satisfies the request:

- Prep only: cleaned Markdown plus publishing notes
- Preview mode: WeChat-optimized HTML recommendation plus layout fixes
- Publish mode: prepared article plus handoff to `baoyu-post-to-wechat`

If the user asks to optimize for WeChat before publishing, do the prep and preview steps first instead of jumping straight to upload.
