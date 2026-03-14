# Article Contract

Use this file when turning raw themes, notes, or drafts into the final illustrated HTML bundle.

## Accepted Inputs

- topic only
- topic plus bullet points
- transcript
- Markdown draft
- Markdown draft with image directives

## Preferred Frontmatter

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

## Image Directives

Use explicit directives when you want strong control:

```md
[[image: cover | cinematic editorial illustration of AI tools coordinating a workflow, soft blue-green palette, no text]]
[[image: section | abstract minimal diagram of agent handoffs, editorial vector feel, no labels]]
```

Directive format:

- `cover`: hero image
- `section`: inline section image

## Automatic Image Planning

If no directives are present, infer:

- one cover image
- up to two section images based on the strongest H2 sections

## Output Package

The script should produce:

- `article.md`
- `article.html`
- `image-plan.json`
- `assets/`
