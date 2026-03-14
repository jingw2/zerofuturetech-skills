---
name: article-thumbnail-illustrator
description: Generate thumbnails and article illustration images for essays, newsletters, and editorial pages by combining structured cover-image direction inspired by baoyu-cover-image with configurable image providers inspired by baoyu-image-gen. Use when Codex receives an article, theme, title, summary, or Markdown draft and needs to output thumbnail prompts, section-image prompts, or actual generated images for cover and inline article use.
---

# Article Thumbnail Illustrator

## Overview

Use this skill when the article already exists or when the user has a theme and needs the visual system around it.
This skill focuses on image direction, not article writing.

It should produce:

- thumbnail direction
- thumbnail prompt
- section-image prompts
- optional generated images

Read [references/visual-dimensions.md](references/visual-dimensions.md) for the thumbnail style system, [references/provider-config.md](references/provider-config.md) for provider and model configuration, and [references/image-planning.md](references/image-planning.md) for how to infer section images from article structure.

Runnable helper:

- `scripts/build_article_images.py`: read article content, infer thumbnail + section image plan, write prompt files, and optionally generate images

## What This Skill Owns

This skill owns:

- visual direction for article covers
- thumbnail prompt generation
- section image planning
- image provider dispatch

This skill does not own:

- full article writing
- final HTML page construction
- platform publishing

## Workflow

### 1. Normalize the source

Accept:

- a title
- a theme
- a summary
- a Markdown article
- a Markdown article with frontmatter

Resolve:

- title
- summary
- article type
- language
- thumbnail aspect ratio
- provider
- model

### 2. Choose thumbnail dimensions

Use the five-direction model inspired by the cover workflow:

- `type`
- `palette`
- `rendering`
- `text`
- `mood`

Default to a restrained editorial look unless the article clearly needs something louder.

### 3. Plan article illustrations

Infer:

- one thumbnail / hero image
- zero to three section images

Section images should be used only when they strengthen structure, pacing, or explanation.
Do not flood the article with decorative visuals.

### 4. Generate prompts

Create:

- `prompts/thumbnail.md`
- `prompts/section-01.md`, `section-02.md`, ...
- `image-plan.json`

### 5. Generate images when configured

If provider credentials are available:

- generate thumbnail
- generate section images
- save under `assets/`

If not:

- still produce prompt files and image plan
- explain what is missing

## Commands

```bash
python3 scripts/build_article_images.py article.md --dry-run
python3 scripts/build_article_images.py article.md --provider openai
python3 scripts/build_article_images.py article.md --provider gemini
python3 scripts/build_article_images.py article.md --provider replicate --model google/nano-banana-pro
```

## Frontmatter Contract

Preferred frontmatter:

```yaml
---
title: Article title
summary: One-line summary
article_type: essay
image_provider: openai
image_model: gpt-image-1
image_size: 1536x1024
thumbnail_aspect: 16:9
thumbnail_style: editorial
---
```

## Output Modes

- planning only: prompt files + plan JSON
- generation mode: prompt files + plan JSON + assets

## Quality Bar

Before delivering, check:

- the thumbnail feels editorial, not generic AI wallpaper
- image prompts are specific and composition-aware
- section images map to actual article sections
- the image set feels like one visual family
