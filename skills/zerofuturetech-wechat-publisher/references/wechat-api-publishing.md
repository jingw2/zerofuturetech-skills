# WeChat API Publishing

Use this file when the prepared article needs to go straight into 微信公众号草稿箱 without any external publishing skill.

## Config Locations

Preferred config paths:

- project config: `.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`
- user config: `~/.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`
- project env: `.zerofuturetech-skills/.env`
- user env: `~/.zerofuturetech-skills/.env`

Legacy fallback paths are still accepted for migration:

- `.baoyu-skills/baoyu-post-to-wechat/EXTEND.md`
- `~/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md`
- `.baoyu-skills/.env`
- `~/.baoyu-skills/.env`

## Required Credentials

For API publishing, the skill needs:

- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`

These credentials are used to fetch `access_token` before uploading assets and creating a draft.

## Supported Publish Metadata

The publisher resolves these fields from `metadata.json`, article frontmatter, CLI overrides, and config defaults:

- `title`
- `author`
- `summary` / `digest`
- `cover`
- `content_source_url`
- `need_open_comment`
- `only_fans_can_comment`
- `wechat_theme`
- `wechat_color`
- `wechat_style`

## Publish Steps

1. Read `metadata.json`
2. Load WeChat credentials and publish defaults
3. Render Markdown into WeChat-safe inline HTML
4. Upload inline images with `media/uploadimg`
5. Upload cover image with `material/add_material`
6. Create draft with `draft/add`

## Design Constraints

- Prefer inline styles over `<style>` blocks because WeChat draft rendering is more predictable with inline article HTML
- Keep generated HTML simple: headings, paragraphs, lists, quotes, images, and code blocks
- Preserve image captions when they exist in Markdown alt text
- Fail fast when cover image or credentials are missing for API publish

## Current Scope

The skill currently owns the API publishing path end to end.

Browser-based publish can be added later, but should remain optional because the main value of this skill is:

- Markdown cleanup
- style-aware preview
- reliable API draft creation
