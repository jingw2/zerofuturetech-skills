# Zero Future Tech Skills

[中文](./README.zh-CN.md)

Reusable skills for [Codex](https://openai.com/codex), [OpenClaw](https://openclaw.ai), and [Claude Code](https://claude.ai/code) — content writing, image generation, and publishing workflows.

## Quick Install

```bash
npx github:jingw2/zerofuturetech-skills wechat
npx github:jingw2/zerofuturetech-skills x-essay
npx github:jingw2/zerofuturetech-skills illustrated-article-html-studio
npx github:jingw2/zerofuturetech-skills article-thumbnail-illustrator
```

Installs to `~/.codex/skills` by default. Use `--platform` to target other platforms:

```bash
npx github:jingw2/zerofuturetech-skills wechat --platform openclaw
npx github:jingw2/zerofuturetech-skills wechat --platform claude
```

## CLI Reference

| Command | Description |
| --- | --- |
| `zerofuturetech-skills --list` | List all available skills |
| `zerofuturetech-skills --version` | Show version |
| `zerofuturetech-skills --help` | Show help |
| `zerofuturetech-skills <skill> --dry-run` | Preview install without copying |
| `zerofuturetech-skills <skill> --platform <p>` | Install to `codex`, `openclaw`, or `claude` |
| `zerofuturetech-skills <skill> --target <dir>` | Install to a custom directory |

## Skills

### `zerofuturetech-wechat-publisher`

Prepare polished WeChat-draft-ready articles from Markdown and image assets, then publish directly to the WeChat Official Account draft box through the official API.

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

- `essay` → `tech-editorial`
- `tutorial` → `bold`
- `brief` → `minimal-cn`

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

### `illustrated-article-html-studio`

Turn a topic or Markdown draft into a complete illustrated editorial article bundle with article copy, image planning, optional generated images, and integrated standalone HTML.

What it does:

- Produces article Markdown, `image-plan.json`, assets, and `article.html`
- Supports configurable image providers including OpenAI and Gemini
- Combines article structure, generated cover images, section images, and polished HTML layout

Best for:

- End-to-end article packages
- Editorial demos
- Publication preview pages

### `article-thumbnail-illustrator`

Generate thumbnails and inline article illustration sets for essays, newsletters, and editorial pages.

What it does:

- Produces thumbnail prompts and section-image prompts
- Supports OpenAI and Gemini image generation
- Uses a stronger editorial thumbnail-direction workflow instead of generic image prompting

Best for:

- Article thumbnails
- Section illustrations
- Image systems that need more human editorial direction

## Install Options

### Option 1: npx (recommended)

```bash
npx github:jingw2/zerofuturetech-skills wechat
npx github:jingw2/zerofuturetech-skills x-essay
npx github:jingw2/zerofuturetech-skills illustrated-article-html-studio
npx github:jingw2/zerofuturetech-skills article-thumbnail-illustrator
```

Supported aliases:

| Alias | Skill |
| --- | --- |
| `wechat` | `zerofuturetech-wechat-publisher` |
| `x-essay`, `essay` | `high-agency-x-essay-writer` |

Supported platforms:

| Platform | Install path |
| --- | --- |
| `codex` (default) | `~/.codex/skills` |
| `openclaw` | `~/.openclaw/skills` |
| `claude` | `~/.claude/agents` |

### Option 2: global install

```bash
npm install -g github:jingw2/zerofuturetech-skills
zerofuturetech-skills wechat
zerofuturetech-skills x-essay --platform claude
```

### Option 3: copy manually

```bash
cp -R skills/zerofuturetech-wechat-publisher ~/.codex/skills/
cp -R skills/high-agency-x-essay-writer ~/.codex/skills/
```

## WeChat Publisher Setup

### Config

Preferred config paths:

- Project: `.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`
- User: `~/.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`
- Project env: `.zerofuturetech-skills/.env`
- User env: `~/.zerofuturetech-skills/.env`

Recommended `EXTEND.md`:

```
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

### Usage

```bash
# Prepare
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style auto --compare-styles

# Preview
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --dry-run

# Publish
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
wechat_style: tech-editorial
need_open_comment: 1
only_fans_can_comment: 0
---
```

## Troubleshooting

Each skill's `SKILL.md` includes a **Gotchas** section with solutions to common issues:

| Skill | Common issues |
| --- | --- |
| `zerofuturetech-wechat-publisher` | API credentials, image paths, Markdown encoding |
| `high-agency-x-essay-writer` | Weak source material, vague claims, translation pitfalls |
| `article-thumbnail-illustrator` | Provider credentials, image quality, prompt specificity |
| `illustrated-article-html-studio` | Article structure, image slots, HTML compatibility |

## Notes

- Each skill is self-contained under `skills/`
- `SKILL.md` is the source of truth for each skill
- `references/` stores on-demand guidance docs
- Codex and OpenClaw install the full skill folder
- Claude Code installs a matching agent file from `platforms/claude/agents/`

## Star Growth

[![Star History Chart](https://api.star-history.com/svg?repos=jingw2/zerofuturetech-skills&type=Date)](https://star-history.com/#jingw2/zerofuturetech-skills&Date)
