---
name: zerofuturetech-wechat-publisher
description: Prepare polished, WeChat-draft-ready articles from Markdown and image assets, then publish them directly to the WeChat Official Account draft box through the official API. Use when Codex receives a Markdown article, article images, cover image, or mixed writing assets and needs to optimize typography, spacing, headings, image rhythm, frontmatter, and WeChat metadata before sending the result to 微信公众号草稿箱.
---

# Zerofuturetech Wechat Publisher

## Overview

Turn a Markdown article plus optional images into a WeChat-optimized article draft that looks good inside 微信公众号草稿箱 rather than merely rendering without errors.
This skill is layout-first: it improves structure, Chinese typography, heading rhythm, image placement, and metadata before publishing directly through the WeChat draft API.

Read [references/wechat-layout-rules.md](references/wechat-layout-rules.md) for the layout rules, [references/article-prep.md](references/article-prep.md) for Markdown and image preparation, and [references/wechat-api-publishing.md](references/wechat-api-publishing.md) for the direct publishing flow.

Runnable helpers:

- `scripts/prepare_article.py`: clean Markdown, resolve cover/images, generate `cleaned.md`, `metadata.json`, and `preview.html`
- `scripts/publish_wechat.py`: read `metadata.json`, render WeChat-safe inline HTML, upload assets, and create a draft through the official WeChat API

## Architecture

Use a single-skill model:

- This skill owns the preparation layer:
  - article cleanup
  - Markdown normalization
  - image and cover resolution
  - WeChat-specific layout choices
  - preview-oriented HTML expectations
- This skill also owns the API publishing layer:
  - credential loading
  - access token retrieval
  - inline image upload
  - cover upload
  - draft creation

Keep the browser publishing path optional and separate from the core workflow.

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
- publishing method preference: `api`

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

### 5. Publish through the WeChat draft API

After content prep, publish through the official WeChat API.

Preferred flow:

1. Markdown input stays Markdown until publish time
2. Theme/color/style defaults are resolved intentionally
3. Cover image is confirmed before API publish
4. Inline images are uploaded and rewritten to WeChat-hosted URLs
5. The final draft is created through `draft/add`

If the article needs a custom HTML pass before publishing, keep the generated HTML simple and inline-styled so it remains compatible with WeChat draft rendering.

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
python3 scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --dry-run
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
content_source_url: https://example.com/original-post
need_open_comment: 1
only_fans_can_comment: 0
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
- API credentials are available
- The final workflow stays inside this skill

## Output Modes

Use the lightest mode that satisfies the request:

- Prep only: cleaned Markdown plus publishing notes
- Preview mode: WeChat-optimized HTML recommendation plus layout fixes
- Publish mode: prepared article plus direct draft creation through the WeChat API

## Configuration

Preferred config paths:

- `.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`
- `~/.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`
- `.zerofuturetech-skills/.env`
- `~/.zerofuturetech-skills/.env`

Legacy `.baoyu-skills` config is still read as a fallback for migration, but it is no longer required.

If the user asks to optimize for WeChat before publishing, do the prep and preview steps first instead of jumping straight to upload.
