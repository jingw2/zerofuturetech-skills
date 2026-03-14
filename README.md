# Zero Future Tech Skills

[中文](./README.zh-CN.md)

Public skill registry for reusable Codex writing and publishing workflows from Zero Future Tech.

Supported targets:

- Codex
- OpenClaw
- Claude Code

## Quick Install

Install the WeChat publisher:

```bash
npx github:jingw2/zerofuturetech-skills wechat
```

Install the X essay writer:

```bash
npx github:jingw2/zerofuturetech-skills x-essay
```

Install the illustrated HTML article studio:

```bash
npx github:jingw2/zerofuturetech-skills illustrated-article-html-studio
```

Install the thumbnail + article image skill:

```bash
npx github:jingw2/zerofuturetech-skills article-thumbnail-illustrator
```

Both commands install to `~/.codex/skills` by default.

Other platforms:

```bash
npx github:jingw2/zerofuturetech-skills wechat --platform openclaw
npx github:jingw2/zerofuturetech-skills wechat --platform claude
```

## Skills

### `illustrated-article-html-studio`

Turn a topic or Markdown draft into a complete illustrated editorial article bundle with article copy, image planning, optional generated images, and integrated standalone HTML.

What it does:

- Produces article Markdown, `image-plan.json`, assets, and `article.html`
- Supports configurable image providers including OpenAI and Gemini
- Combines article structure, generated cover images, section images, and polished HTML layout

Best for:

- end-to-end article packages
- editorial demos
- publication preview pages

### `article-thumbnail-illustrator`

Generate thumbnails and inline article illustration sets for essays, newsletters, and editorial pages.

What it does:

- Produces thumbnail prompts and section-image prompts
- Supports OpenAI and Gemini image generation
- Uses a stronger editorial thumbnail-direction workflow instead of generic image prompting

Best for:

- article thumbnails
- section illustrations
- image systems that need more human editorial direction

### `zerofuturetech-wechat-publisher`

Prepare polished WeChat-draft-ready articles from Markdown and image assets, then publish them directly to the WeChat Official Account draft box through the official API.

What it does:

- Cleans Markdown and resolves title, summary, author, cover image, and inline images
- Generates `cleaned.md`, `metadata.json`, and `preview.html`
- Supports 3 WeChat-friendly styles: `minimal-cn`, `tech-editorial`, `bold`
- Renders WeChat-safe inline HTML and publishes drafts through the official API

Best for:

- Markdown articles that need good WeChat draft appearance
- Chinese long-form essays, tutorials, and tech analysis posts
- Preview-first publishing workflow

Auto style recommendation:

- `essay` -> `tech-editorial`
- `tutorial` -> `bold`
- `brief` -> `minimal-cn`

Style preview:

| Style | Preview | Best for |
| --- | --- | --- |
| `minimal-cn` | ![minimal-cn](./assets/readme/wechat-style-minimal-cn.svg) | Chinese essays, opinion pieces, calm long-form reading |
| `tech-editorial` | ![tech-editorial](./assets/readme/wechat-style-tech-editorial.svg) | AI, product, workflow, and tech analysis posts |
| `bold` | ![bold](./assets/readme/wechat-style-bold.svg) | Tutorials, playbooks, and structured step-by-step articles |

### `high-agency-x-essay-writer`

Write high-agency, contrarian long-form X/newsletter essays in English or Chinese without imitating any living author.

What it does:

- Drafts or rewrites long-form essays for X, newsletters, and idea-driven posts
- Uses strong hooks, a clean argument spine, systems-thinking, and actionable endings
- Supports native-feeling Chinese adaptation instead of English-style literal translation

Best for:

- Raw notes, outlines, or half-formed arguments
- Sharpening thesis and structure
- Outputting separate English and Chinese versions

## Install Options

### Option 1: shortest commands

```bash
npx github:jingw2/zerofuturetech-skills wechat
npx github:jingw2/zerofuturetech-skills x-essay
npx github:jingw2/zerofuturetech-skills illustrated-article-html-studio
npx github:jingw2/zerofuturetech-skills article-thumbnail-illustrator
```

Supported aliases:

- `wechat` -> `zerofuturetech-wechat-publisher`
- `x-essay` -> `high-agency-x-essay-writer`
- `essay` -> `high-agency-x-essay-writer`

Supported platforms:

- `codex` -> installs to `~/.codex/skills`
- `openclaw` -> installs to `~/.openclaw/skills`
- `claude` -> installs to `~/.claude/agents`

Examples:

```bash
npx github:jingw2/zerofuturetech-skills wechat --platform codex
npx github:jingw2/zerofuturetech-skills wechat --platform openclaw
npx github:jingw2/zerofuturetech-skills wechat --platform claude
```

### Option 2: global install

```bash
npm install -g github:jingw2/zerofuturetech-skills
zerofuturetech-skills wechat
zerofuturetech-skills x-essay
zerofuturetech-skills wechat --platform openclaw
zerofuturetech-skills wechat --platform claude
```

The old explicit form still works:

```bash
zerofuturetech-skills install zerofuturetech-wechat-publisher
zerofuturetech-skills install high-agency-x-essay-writer
```

Custom target directory:

```bash
npx github:jingw2/zerofuturetech-skills wechat --target ~/.codex/skills
npx github:jingw2/zerofuturetech-skills wechat --platform claude --target ~/.claude/agents
```

### Option 3: copy manually

```bash
cp -R skills/high-agency-x-essay-writer ~/.codex/skills/
cp -R skills/zerofuturetech-wechat-publisher ~/.codex/skills/
```

Or with `rsync`:

```bash
rsync -a skills/high-agency-x-essay-writer/ ~/.codex/skills/high-agency-x-essay-writer/
rsync -a skills/zerofuturetech-wechat-publisher/ ~/.codex/skills/zerofuturetech-wechat-publisher/
```

## WeChat Publisher Setup

### Config

Preferred config paths:

- Project config: `.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`
- User config: `~/.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`
- Project env: `.zerofuturetech-skills/.env`
- User env: `~/.zerofuturetech-skills/.env`

Recommended `EXTEND.md`:

```md
default_theme: default
default_color: green
default_author: Zero Future Tech
need_open_comment: 1
only_fans_can_comment: 0
content_source_url:
```

Recommended `.env`:

```bash
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
```

Legacy `.baoyu-skills` config is still accepted as a migration fallback.

### Usage

Prepare article files:

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style auto --compare-styles
```

Preview the final draft payload first:

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --dry-run
```

Publish to WeChat draft box:

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --method api
```

Recommended frontmatter:

```yaml
---
title: Article title
author: Author name
summary: One-line summary
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

Style selection:

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style tech-editorial
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style minimal-cn
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style bold
```

Or in frontmatter:

```yaml
wechat_style: tech-editorial
```

## Notes

- Each skill is self-contained under `skills/`
- `SKILL.md` is the source of truth
- `references/` stores on-demand guidance
- Codex and OpenClaw install the original skill folders
- Claude Code installs matching subagent markdown files from `platforms/claude/agents/`

## Star Growth

[![Star History Chart](https://api.star-history.com/svg?repos=jingw2/zerofuturetech-skills&type=Date)](https://star-history.com/#jingw2/zerofuturetech-skills&Date)
