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

Prepare polished WeChat-draft-ready articles from Markdown and image assets, then publish them to the WeChat Official Account draft box by reusing `baoyu-post-to-wechat` as the publishing engine.

What it does:

- Cleans Markdown before publishing and removes common WeChat-unfriendly structure issues
- Resolves title, summary, author, cover image, and inline images
- Generates `cleaned.md`, `metadata.json`, and `preview.html`
- Supports multiple preview styles for Chinese WeChat article layouts
- Hands off final publishing to `baoyu-post-to-wechat` using API or browser mode

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

### Option 1: Copy locally

Copy a skill folder into your local Codex skills directory:

```bash
cp -R skills/high-agency-x-essay-writer ~/.codex/skills/
cp -R skills/zerofuturetech-wechat-publisher ~/.codex/skills/
```

Or sync it:

```bash
rsync -a skills/high-agency-x-essay-writer/ ~/.codex/skills/high-agency-x-essay-writer/
rsync -a skills/zerofuturetech-wechat-publisher/ ~/.codex/skills/zerofuturetech-wechat-publisher/
```

### Option 2: Install with npm from GitHub

Install the repo as a package and copy the skill into `~/.codex/skills`:

```bash
npx github:jingw2/zerofuturetech-skills install high-agency-x-essay-writer
npx github:jingw2/zerofuturetech-skills install zerofuturetech-wechat-publisher
```

You can also install globally first:

```bash
npm install -g github:jingw2/zerofuturetech-skills
zerofuturetech-skills install high-agency-x-essay-writer
zerofuturetech-skills install zerofuturetech-wechat-publisher
```

Optional target directory:

```bash
zerofuturetech-skills install high-agency-x-essay-writer --target ~/.codex/skills
zerofuturetech-skills install zerofuturetech-wechat-publisher --target ~/.codex/skills
```

## WeChat Publisher Setup

`zerofuturetech-wechat-publisher` depends on `baoyu-post-to-wechat` for final publishing.

Install the dependency first:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo JimLiu/baoyu-skills \
  --path skills/baoyu-post-to-wechat
```

### WeChat account configuration

Configure `baoyu-post-to-wechat` via:

- Project config: `.baoyu-skills/baoyu-post-to-wechat/EXTEND.md`
- User config: `~/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md`

Recommended minimum config:

```md
default_theme: default
default_color: green
default_publish_method: api
default_author: Zero Future Tech
need_open_comment: 1
only_fans_can_comment: 0
chrome_profile_path:
```

### API credentials

For API publishing, add WeChat credentials to one of:

- `<project>/.baoyu-skills/.env`
- `~/.baoyu-skills/.env`

Example:

```bash
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
```

### Browser publishing

If you prefer browser mode:

- install Chrome
- log in to the target WeChat Official Account
- configure `chrome_profile_path` if you want isolated account sessions

## WeChat Publisher Usage

Prepare article files:

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style auto --compare-styles
```

Publish after preview:

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --method api
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --method browser --dry-run
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
