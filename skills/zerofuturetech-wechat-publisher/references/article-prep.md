# Article Preparation

Use this file when the input is Markdown and the article needs cleanup before WeChat publishing.

## Input Expectations

Best input package:

- one Markdown file
- one cover image
- optional body image directory
- frontmatter with title, author, summary if available

If any key metadata is missing, resolve it before publishing.

## Preferred Frontmatter

```yaml
---
title: 文章标题
author: 作者名
summary: 摘要
cover: imgs/cover.png
article_type: essay
wechat_theme: default
wechat_color: green
---
```

## Cleanup Checklist

1. Remove duplicated H1 title if frontmatter already defines title.
2. Normalize Chinese punctuation and spacing when obviously broken.
3. Remove accidental empty bullets or empty headings.
4. Check whether each image path exists locally.
5. Promote weak bullet dumps into clearer sections when needed.
6. Shorten the first screen if the opening is too long.
7. Ensure the article has a usable summary for WeChat metadata.

## Summary Rules

- Prefer one sentence.
- Keep it concrete.
- Avoid generic slogans.
- Treat it as metadata, not as a teaser thread.

## Image Resolution Order

For cover image:

1. explicit user input
2. frontmatter `cover`
3. frontmatter aliases `coverImage`, `featureImage`, `image`
4. `imgs/cover.png`
5. first inline image as fallback

For inline images:

- preserve Markdown order
- prefer local paths
- keep captions only if they already exist or are clearly useful

## When to Stop and Ask for Fixes

Stop and clarify if:

- the cover image is missing for API publish
- most image paths are broken
- title and body disagree about the article topic
- the Markdown structure is too malformed to publish safely
