# Zero Future Tech Skills

[English](./README.md)

Zero Future Tech 的公开 Codex skill 仓库，主要放可复用的写作和发布工作流。

当前支持的平台：

- Codex
- OpenClaw
- Claude Code

## 快速安装

安装微信公众号发布 skill：

```bash
npx github:jingw2/zerofuturetech-skills wechat
```

安装 X 长文写作 skill：

```bash
npx github:jingw2/zerofuturetech-skills x-essay
```

安装图文一体化 HTML skill：

```bash
npx github:jingw2/zerofuturetech-skills illustrated-article-html-studio
```

安装 thumbnail 和文章配图 skill：

```bash
npx github:jingw2/zerofuturetech-skills article-thumbnail-illustrator
```

默认会安装到 `~/.codex/skills`。其他平台安装示例：

```bash
npx github:jingw2/zerofuturetech-skills wechat --platform openclaw
npx github:jingw2/zerofuturetech-skills wechat --platform claude
```

**v0.1.0 新增功能**：列出所有 skills 和查看帮助文档：

```bash
npx github:jingw2/zerofuturetech-skills --list
npx github:jingw2/zerofuturetech-skills --help
npx github:jingw2/zerofuturetech-skills wechat --dry-run
```

## Skills

### `illustrated-article-html-studio`

把主题或 Markdown 草稿直接整理成完整的图文一体化文章包，输出文章 Markdown、图片规划、可选生成图片和最终独立 HTML。

它可以做的事：

- 输出 `article.md`、`image-plan.json`、图片资产和 `article.html`
- 支持 OpenAI、Gemini 等图片 provider
- 把文章结构、封面图、分节图和最终 HTML 排版串成一条链路

适合：

- 图文一体化文章 demo
- 发布前预览页
- 从内容到页面的一体化产物

### `article-thumbnail-illustrator`

专门生成 thumbnail 和正文配图的 skill，适合文章封面图、newsletter 配图和分节插图。

它可以做的事：

- 输出 thumbnail prompt 和 section image prompts
- 支持 OpenAI、Gemini 出图
- 用更像编辑部视觉方向的方式做配图，而不是泛化 AI prompt

适合：

- 文章缩略图
- 分节插图
- 更有“活人感”的文章视觉系统

### `zerofuturetech-wechat-publisher`

把 Markdown 文章和配图整理成适合微信公众号草稿箱的稿件，支持预览、样式控制、封面图和正文图处理，并直接通过官方 API 发到草稿箱。

它可以做的事：

- 清理 Markdown，解析标题、摘要、作者、封面图和正文图片
- 生成 `cleaned.md`、`metadata.json` 和 `preview.html`
- 支持 3 种更适合微信公众号的样式：`minimal-cn`、`tech-editorial`、`bold`
- 渲染成适合微信草稿箱的内联 HTML，并通过官方 API 发布

适合：

- 想把 Markdown 文章发到微信公众号草稿箱
- 在意排版观感，而不只是“能发成功”
- 希望先预览再发布

样式自动推荐：

- `essay` -> `tech-editorial`
- `tutorial` -> `bold`
- `brief` -> `minimal-cn`

样式示例：

| Style | 示例 | 适合 |
| --- | --- | --- |
| `minimal-cn` | ![minimal-cn](./assets/readme/wechat-style-minimal-cn.svg) | 中文观点长文、专栏、强调阅读舒适度的内容 |
| `tech-editorial` | ![tech-editorial](./assets/readme/wechat-style-tech-editorial.svg) | AI、产品、工作流、科技分析类文章 |
| `bold` | ![bold](./assets/readme/wechat-style-bold.svg) | 教程、步骤文、方法论和操作指南 |

### `high-agency-x-essay-writer`

用于写高 agency、强 hook、强论点推进的 X 长文和 newsletter，支持英文和更自然的中文适配，不直接模仿具体在世作者。

它可以做的事：

- 基于笔记、提纲、半成品观点生成长文
- 强化 hook、论点推进、系统感和结尾行动性
- 分别输出英文版和中文版，而不是生硬直译

适合：

- 原始笔记、提纲、半成品想法
- 想把观点打磨得更锋利
- 想分别输出中英文两个版本

## 安装方式

### 方式 1：最短命令

```bash
npx github:jingw2/zerofuturetech-skills wechat
npx github:jingw2/zerofuturetech-skills x-essay
npx github:jingw2/zerofuturetech-skills illustrated-article-html-studio
npx github:jingw2/zerofuturetech-skills article-thumbnail-illustrator
```

支持这些别名：

- `wechat` -> `zerofuturetech-wechat-publisher`
- `x-essay` -> `high-agency-x-essay-writer`
- `essay` -> `high-agency-x-essay-writer`

支持这些平台参数：

- `codex` -> 安装到 `~/.codex/skills`
- `openclaw` -> 安装到 `~/.openclaw/skills`
- `claude` -> 安装到 `~/.claude/agents`

示例：

```bash
npx github:jingw2/zerofuturetech-skills wechat --platform codex
npx github:jingw2/zerofuturetech-skills wechat --platform openclaw
npx github:jingw2/zerofuturetech-skills wechat --platform claude
```

### 方式 2：全局安装

```bash
npm install -g github:jingw2/zerofuturetech-skills
zerofuturetech-skills wechat
zerofuturetech-skills x-essay
zerofuturetech-skills wechat --platform openclaw
zerofuturetech-skills wechat --platform claude
```

旧写法也兼容：

```bash
zerofuturetech-skills install zerofuturetech-wechat-publisher
zerofuturetech-skills install high-agency-x-essay-writer
```

如果想安装到其他目录：

```bash
npx github:jingw2/zerofuturetech-skills wechat --target ~/.codex/skills
npx github:jingw2/zerofuturetech-skills wechat --platform claude --target ~/.claude/agents
```

### 方式 3：手动复制

```bash
cp -R skills/high-agency-x-essay-writer ~/.codex/skills/
cp -R skills/zerofuturetech-wechat-publisher ~/.codex/skills/
```

或者用 `rsync`：

```bash
rsync -a skills/high-agency-x-essay-writer/ ~/.codex/skills/high-agency-x-essay-writer/
rsync -a skills/zerofuturetech-wechat-publisher/ ~/.codex/skills/zerofuturetech-wechat-publisher/
```

## 微信公众号发布 Skill 配置

### 配置文件

推荐配置路径：

- 项目级配置：`.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`
- 用户级配置：`~/.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md`
- 项目级环境变量：`.zerofuturetech-skills/.env`
- 用户级环境变量：`~/.zerofuturetech-skills/.env`

推荐的 `EXTEND.md`：

```md
default_theme: default
default_color: green
default_author: Zero Future Tech
need_open_comment: 1
only_fans_can_comment: 0
content_source_url:
```

推荐的 `.env`：

```bash
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret
```

旧的 `.baoyu-skills` 配置仍然兼容，方便迁移。

### 使用方式

先准备文章：

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style auto --compare-styles
```

先看 dry-run：

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --dry-run
```

确认后正式发布到草稿箱：

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --method api
```

推荐 frontmatter：

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

样式选择：

```bash
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style tech-editorial
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style minimal-cn
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style bold
```

或者在 frontmatter 里写：

```yaml
wechat_style: tech-editorial
```

## 故障排查

每个 skill 的 `SKILL.md` 都有一个 **"Gotchas"** 部分，记录常见问题和解决方案：

- **微信发布**：图片处理、API 凭证、Markdown 编码
- **X 长文写作**：弱观点、不清晰的主张、翻译陷阱
- **Thumbnail 生成**：Image provider 凭证、图片一致性、Prompt 质量
- **HTML 文章工作室**：文章结构、图片槽位、HTML 兼容性

详细故障排查请查看：

- `skills/zerofuturetech-wechat-publisher/SKILL.md`
- `skills/high-agency-x-essay-writer/SKILL.md`
- `skills/article-thumbnail-illustrator/SKILL.md`
- `skills/illustrated-article-html-studio/SKILL.md`

## 说明

- 每个 skill 都是 `skills/` 下的独立目录
- `SKILL.md` 是 skill 的唯一事实来源
- `references/` 放按需读取的补充资料
- Codex 和 OpenClaw 会安装原始 skill 目录
- Claude Code 会安装 `platforms/claude/agents/` 下对应的 subagent 文件

## Star 增长图

[![Star History Chart](https://api.star-history.com/svg?repos=jingw2/zerofuturetech-skills&type=Date)](https://star-history.com/#jingw2/zerofuturetech-skills&Date)
