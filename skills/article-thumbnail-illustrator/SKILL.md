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

## Gotchas

### Image Provider Configuration

- **Missing API keys**: If `OPENAI_API_KEY` or `GEMINI_API_KEY` is not set in your environment or config, the script will fail with "provider credentials not available". Set these in `.env` or export them as environment variables before running the script. The `--dry-run` flag will still work and generate prompts without attempting generation.
- **Provider model name mismatch**: OpenAI's image models change (e.g., `dall-e-2` vs `dall-e-3`). If you specify a model that no longer exists, the API call will fail. Check the latest available models in the image provider's documentation.
- **Rate limits and quota**: Both OpenAI and Gemini have rate limits and usage quotas. If you generate multiple images in rapid succession, you may hit these limits. Space out requests or check your account usage.

### Image Generation and Quality

- **Generic "AI wallpaper" look**: The script's default prompts might generate clichéd images (stock photos, obvious AI look). To get editorial-quality thumbnails, craft specific, detailed prompts in the `prompts/thumbnail.md` file. Include mood, style, composition, and palette guidance.
- **Image size mismatches**: If the generated image doesn't match your `thumbnail_aspect` (e.g., you want 16:9 but OpenAI generates square), the final layout may look off. Specify exact aspect ratios in the frontmatter and/or prompt.
- **Color palette inconsistency**: If you generate a cover image with OpenAI and section images with Gemini, the visual family may feel disjointed (different color palettes, rendering styles). Stick to one provider for a complete article or manually adjust prompts to maintain consistency.

### Markdown and Content Parsing

- **Missing or malformed frontmatter**: If the article Markdown doesn't have frontmatter with `title` and `summary`, the script will try to infer them from the body, which may produce awkward results. Always include frontmatter.
- **Article too short or poorly structured**: If the article has no H2 sections, the script cannot infer where section images should go. Provide a well-structured article with clear sections.
- **Image paths in Markdown**: If your Markdown contains image references (`![alt](path)`), these are distinct from the image generation system. The script generates *new* images; it doesn't use existing images referenced in the Markdown.

### Workflow and Output

- **Output directory already exists with old assets**: If you run the script twice on the same article, it may overwrite old prompts and assets without warning. Back up important assets before re-running.
- **Prompts not matching the article**: If you edit the Markdown significantly after running the script, the old prompts in `prompts/*.md` may no longer match the current article. Regenerate prompts after major content changes.
- **Image plan (image-plan.json) format changes**: If you manually edit the `image-plan.json` file and introduce errors, downstream processes that consume this file (like `illustrated-article-html-studio`) may fail. Always regenerate via the script.

### Provider-Specific Issues

- **OpenAI image API costs**: Each image generation request costs money. Running `--provider openai` without `--dry-run` will incur charges. Use `--dry-run` first to preview prompts.
- **Gemini API format differences**: Gemini's image generation API has different parameter names and response structures than OpenAI. If switching providers, test the configuration first with a small article.
- **Timeout on slow connections**: Large image downloads may timeout on slow internet. The script may need retry logic or timeout configuration if running in unstable network environments.
