# Zero Future Tech Skills

Public skill registry for reusable Codex writing and workflow skills from Zero Future Tech.

## Skills

### `high-agency-x-essay-writer`

Write high-agency, contrarian long-form X/newsletter essays in English or Chinese without imitating any living author.

What it does:

- Drafts or rewrites long-form essays for X, newsletters, and idea-driven posts
- Uses strong hooks, clean argument spine, systems-thinking, and actionable endings
- Supports native-feeling Chinese adaptation instead of English-style literal translation
- Preserves a safe boundary: inspiration from public creator article patterns, not direct style imitation

Use it when:

- You have raw notes, a journal entry, an outline, or a half-formed argument
- You want a sharper thesis and stronger article structure
- You want separate English and Chinese versions of the same core idea

### `zerofuturetech-wechat-publisher`

Prepare polished WeChat-draft-ready articles from Markdown and image assets, then publish them directly to the WeChat Official Account draft box through the official API.

What it does:

- Cleans Markdown before publishing and removes common WeChat-unfriendly structure issues
- Resolves title, summary, author, cover image, and inline images
- Generates `cleaned.md`, `metadata.json`, and `preview.html`
- Supports multiple preview styles for Chinese WeChat article layouts
- Renders WeChat-safe inline HTML and publishes drafts through the official API

Use it when:

- You have a Markdown article plus cover/body images and want to publish to 微信公众号草稿箱
- You care about WeChat draft appearance, not just successful upload
- You want preview-first workflow before pushing an article to draft

Available styles:

- `minimal-cn`: cleaner Chinese long-form column style
- `tech-editorial`: Chinese tech media / analysis style
- `bold`: stronger hierarchy for tutorials and structured content

Auto recommendation:

- `essay` -> `tech-editorial`
- `tutorial` -> `bold`
- `brief` -> `minimal-cn`

## Structure

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/   # optional
    assets/    # optional
```

## Install

推荐直接用一行安装：

```bash
npx github:jingw2/zerofuturetech-skills zerofuturetech-wechat-publisher
npx github:jingw2/zerofuturetech-skills high-agency-x-essay-writer
```

默认会安装到 `~/.codex/skills`。

### Alternative: global install

如果你会频繁装多个 skill，可以先全局安装：

```bash
npm install -g github:jingw2/zerofuturetech-skills
zerofuturetech-skills zerofuturetech-wechat-publisher
zerofuturetech-skills high-agency-x-essay-writer
```

也兼容旧写法：

```bash
zerofuturetech-skills install zerofuturetech-wechat-publisher
zerofuturetech-skills install high-agency-x-essay-writer
```

如果你想安装到别的目录：

```bash
npx github:jingw2/zerofuturetech-skills zerofuturetech-wechat-publisher --target ~/.codex/skills
```

### Alternative: copy manually

也可以直接复制目录：

```bash
cp -R skills/high-agency-x-essay-writer ~/.codex/skills/
cp -R skills/zerofuturetech-wechat-publisher ~/.codex/skills/
```

或者用 `rsync`：

```bash
rsync -a skills/high-agency-x-essay-writer/ ~/.codex/skills/high-agency-x-essay-writer/
rsync -a skills/zerofuturetech-wechat-publisher/ ~/.codex/skills/zerofuturetech-wechat-publisher/
```

## WeChat Publisher Setup

### WeChat account configuration

Preferred config paths:

- Project config: `.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`
- User config: `~/.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`

Recommended minimum config:

```md
default_theme: default
default_color: green
default_author: Zero Future Tech
need_open_comment: 1
only_fans_can_comment: 0
content_source_url:
```

### API credentials

For API publishing, add WeChat credentials to one of:

- `<project>/.zerofuturetech-skills/.env`
- `~/.zerofuturetech-skills/.env`

Example:

```bash
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
```

Legacy `.baoyu-skills` config is still accepted as a migration fallback, but it is no longer required.

## WeChat Publisher Usage

Prepare article files:

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style auto --compare-styles
```

发布到草稿箱前先看 dry-run：

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --dry-run
```

确认无误后再正式发布：

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --method api
```

### Frontmatter

Recommended article frontmatter:

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

### Style selection

Use the CLI:

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style tech-editorial
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style minimal-cn
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style bold
```

Or set the article frontmatter field:

```yaml
wechat_style: tech-editorial
```

## Conventions

- Each skill is self-contained under `skills/`
- `SKILL.md` is the source of truth
- `references/` stores on-demand guidance
- Keep repo-level docs minimal and skill-focused
