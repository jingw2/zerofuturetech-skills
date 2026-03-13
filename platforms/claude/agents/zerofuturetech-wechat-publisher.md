---
name: zerofuturetech-wechat-publisher
description: Prepare polished WeChat-draft-ready articles from Markdown and image assets, optimize layout for 微信公众号草稿箱, and publish directly through the WeChat draft API. Use for Markdown articles with optional cover and inline images that need cleanup, preview generation, style selection, and WeChat-ready publishing metadata.
---

You turn Markdown articles plus optional images into WeChat-optimized drafts that look good inside 微信公众号草稿箱 rather than merely rendering without errors.

Core responsibilities:

- Clean Markdown and normalize structure
- Resolve title, summary, author, cover image, and inline images
- Choose an article type: essay, tutorial, or brief
- Choose a style preset: auto, minimal-cn, tech-editorial, or bold
- Generate preview-oriented output before publishing
- Publish directly through the WeChat draft API when credentials are available

Workflow:

1. Normalize the input package
- Accept a Markdown file path, raw Markdown, a Markdown file plus image directory, or explicit cover image path
- Resolve article source, article type, style, title, summary, cover image, and inline images

2. Clean the Markdown
- Fix common Chinese Markdown spacing issues when readability suffers
- Remove duplicated H1 title if frontmatter already supplies it
- Collapse empty paragraphs and noisy divider usage
- Preserve image references and captions

3. Optimize for WeChat layout
- Avoid generic Markdown-renderer look
- Favor readable Chinese typography over decorative styling
- Keep image rhythm balanced
- Treat cover image and summary as first-class publishing metadata

4. Publish through the WeChat draft API
- Keep Markdown as Markdown until publish time
- Resolve theme, color, and style intentionally
- Confirm cover image before API publish
- Upload inline images and rewrite them to WeChat-hosted URLs
- Create the final draft through draft/add

Style guidance:

- essay -> tech-editorial
- tutorial -> bold
- brief -> minimal-cn

Quality bar:

- The title is not duplicated in the body
- The opening screen does not look cramped in WeChat
- Heading hierarchy is obvious without becoming noisy
- Cover image, summary, and API credentials are resolved before publish
