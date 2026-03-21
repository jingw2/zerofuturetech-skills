---
name: illustrated-article-html-studio
description: Turn a topic, notes, or Markdown draft into a polished illustrated HTML article by combining high-agency article writing, configurable image generation providers such as OpenAI Images and Gemini image generation, and integrated editorial layout. Use when Codex receives a theme, outline, notes, article draft, or Markdown content and needs to output article copy, generated images, and a ready-to-publish HTML page in one pass.
---

# Illustrated Article HTML Studio

## Overview

Use this skill to create a complete article package:

- article copy
- image prompts
- generated cover and section images
- styled HTML output

The writing layer should inherit the sharp argument structure, short-paragraph rhythm, and strong thesis discipline of the existing high-agency essay workflow.
The layout layer should inherit the readable Chinese-first spacing, heading rhythm, and image placement discipline from the WeChat publisher workflow, but produce general-purpose HTML rather than WeChat draft HTML.

Read [references/article-contract.md](references/article-contract.md) for the input contract, [references/image-provider-config.md](references/image-provider-config.md) for provider configuration, and [references/html-layout-modes.md](references/html-layout-modes.md) for layout choices.

Runnable helper:

- `scripts/build_illustrated_article.py`: read Markdown, infer or read image slots, optionally call OpenAI or Gemini image generation, and produce `article.html`, `article.md`, `image-plan.json`, and assets

## What This Skill Owns

This skill owns the full editorial package:

- draft or rewrite the article copy
- define image slots and image prompts
- call a configured image generation provider when available
- generate a complete standalone HTML article with integrated images

It does not need to publish anywhere by default.
Publishing is a separate step.

## Workflow

### 1. Normalize the source

Accept any of these:

- a theme
- notes or bullet points
- a Markdown draft
- a transcript or rough outline
- a finished article that still needs images and layout

Resolve:

- title
- summary
- author
- target language
- article type: `essay`, `tutorial`, or `brief`
- HTML style: `editorial`, `minimal`, or `bold`
- image provider: `openai`, `gemini`, or `none`

If the user only gives a theme and notes, draft the article first before running the pipeline.

### 2. Write the article in the house style

Use the same standards as the high-agency essay workflow:

- lead with a sharp thesis
- build a clean argument spine
- prefer short paragraphs
- keep the prose direct, specific, and original
- make Chinese output read like native Chinese writing, not translated English

If the piece is more explanatory than argumentative, keep the same clarity but soften the confrontational edge.

### 3. Plan the image system

The article can contain image slots using this directive:

```md
[[image: cover | cinematic editorial illustration of autonomous AI workflow dashboards, clean blue-green palette, no text]]
[[image: section | abstract diagram of agent handoffs across tools, minimal editorial style]]
```

If the source has no image directives, infer them automatically:

- one cover image
- up to two section images for the strongest H2 sections

Do not insert decorative images everywhere.
Use images to support rhythm and structure, not to fill space.

### 4. Generate or dry-run images

If provider config is available:

- call the configured provider
- save generated images under `assets/`
- wire them into the final HTML

If provider config is missing:

- still generate `image-plan.json`
- output HTML with visual placeholders
- explain which env vars or config are missing

### 5. Build the final HTML

The final HTML should be:

- standalone
- readable on desktop and mobile
- strong in title area and section rhythm
- image-aware
- suitable for publishing on a site, Substack preview page, internal CMS import, or later platform-specific adaptation

## Commands

Build from Markdown:

```bash
python3 scripts/build_illustrated_article.py article.md --output-dir out/article
python3 scripts/build_illustrated_article.py article.md --image-provider openai --html-style editorial
python3 scripts/build_illustrated_article.py article.md --image-provider gemini --dry-run
```

## Frontmatter Contract

Preferred frontmatter:

```yaml
---
title: Article title
author: Zero Future Tech
summary: One-line summary
article_type: essay
html_style: editorial
image_provider: openai
image_model: gpt-image-1
image_size: 1536x1024
language: en
---
```

Accepted `html_style` values:

- `editorial`
- `minimal`
- `bold`

Accepted `image_provider` values:

- `openai`
- `gemini`
- `none`

Current default models:

- `openai` -> `gpt-image-1`
- `gemini` -> `gemini-3-pro-image-preview`

## Quality Bar

Before delivering, check:

- the article is worth reading without the images
- the title area is strong and not generic
- images reinforce the structure instead of duplicating the text
- the page reads well on mobile
- the output directory includes article Markdown, HTML, image plan, and assets

## Output Modes

Use the lightest useful mode:

- writing only: article Markdown
- image planning: article Markdown plus `image-plan.json`
- full bundle: article Markdown, assets, and polished HTML

If the user asks for the integrated HTML result, prefer the full bundle.

## Gotchas

### Article Writing and Content

- **Writing from a weak premise**: If the input is just a theme or loose notes without a clear thesis, the article will lack focus. Always identify the central argument first: "What is the ONE claim the reader should believe?" If you can't articulate it in one sentence, don't start writing yet.
- **Switching voices mid-article**: The skill should maintain the high-agency essay style throughout. If sections drift into explanatory, gentle, or overly cheerful tones, the piece will feel inconsistent. Review for tonal consistency before finalizing.
- **Over-length**: If the article exceeds 2000-2500 words, consider splitting it. Longer pieces need stronger structural guidance, and mobile reading experience degrades. The HTML output quality assumes a tighter article.

### Image Generation and Slots

- **Image directives in wrong format**: The script expects image slots as `[[image: cover | description]]` or `[[image: section | description]]`. If you use different syntax (e.g., `[image]` or `![[image]]`), the parser won't recognize them. Use the exact format.
- **Too many images**: If you insert image slots for every section, the article becomes an image gallery, not a readable piece. Limit to one cover + one to two section images. Images should support rhythm, not dominate.
- **Image descriptions are too vague**: If the image slot description is "picture of AI" or "tech stuff", the generated image will be generic. Write specific, compositional prompts: "minimalist diagram of agent handoff architecture, blue-gray palette, no text, icon-style".
- **Missing image provider credentials**: If you specify `--image-provider openai` but `OPENAI_API_KEY` is not set, the script will fail or skip image generation silently. Always verify credentials are available before running.

### HTML Output and Layout

- **HTML style mismatch with content**: If you choose `--html-style bold` (strong colors, high contrast) but the article is a subtle, introspective essay, the layout will feel at odds with the writing. Match the HTML style to the article's tone.
- **Mobile rendering issues**: The generated HTML is responsive, but complex CSS or images may render poorly on small screens. Test the HTML file on a mobile device before considering it final.
- **CSS framework compatibility**: The HTML includes inline and `<style>` block CSS. If you import this HTML into another page or CMS, conflicting styles may cause layout breakage. The standalone HTML works best when published as-is or imported into a CSS-isolated container.
- **Image paths in final HTML**: If images are generated and saved under `assets/`, the HTML references them with relative paths (e.g., `assets/cover.png`). If you move the HTML file without moving the assets folder, images will 404. Keep the directory structure intact or rewrite paths to absolute URLs.

### Workflow and Integration

- **Markdown not pre-structured**: If you pass raw notes or a transcript (no H2/H3 structure), the script will try to infer the structure. This may result in odd section breaks or missing section images. Provide a well-organized Markdown with clear section headings.
- **Conflicting frontmatter and CLI flags**: If the Markdown includes `html_style: minimal` but you pass `--html-style bold`, the CLI flag will override. This can be confusing. Use either frontmatter OR CLI flags, not both, for consistency.
- **Output directory collisions**: If you run the script twice on the same input, old files in the output directory will be overwritten. Backup important outputs before re-running.
- **Article already has images embedded**: If the input Markdown includes image references (`![caption](path/to/image.png)`), these are *different* from the `[[image: ...]]` slots. Embedded images stay as-is; `[[image: ...]]` slots are replaced with generated images. Don't mix both systems unless you understand the interaction.

### Provider and Configuration Issues

- **Switching image providers mid-workflow**: If you generate images with OpenAI and later want to regenerate with Gemini, the prompts and image sizes may not be compatible. The visual family may feel inconsistent. Decide on a provider upfront.
- **Image model deprecation**: OpenAI and Gemini periodically deprecate or rename models. If your config specifies an old model name, the script will fail. Check the provider's latest available models.
- **API quota and rate limits**: Generating a full article with cover + section images can incur costs and may hit rate limits, especially with OpenAI. Use `--dry-run` first to preview before committing to generation.
- **Language mismatch**: If frontmatter specifies `language: zh` (Chinese) but the article content is in English, some image prompts or HTML generation may produce unexpected results. Match language to content.
