# Zero Future Tech Skills

[English](./README.md)

可复用的 [Codex](https://openai.com/codex)、[OpenClaw](https://openclaw.ai) 和 [Claude Code](https://claude.ai/code) skills，涵盖内容写作、图片生成和发布工作流。

## 快速安装

```bash
npx github:jingw2/zerofuturetech-skills wechat
npx github:jingw2/zerofuturetech-skills x-essay
npx github:jingw2/zerofuturetech-skills illustrated-article-html-studio
npx github:jingw2/zerofuturetech-skills article-thumbnail-illustrator
```

默认安装到 `~/.codex/skills`。用 `--platform` 指定其他平台：

```bash
npx github:jingw2/zerofuturetech-skills wechat --platform openclaw
npx github:jingw2/zerofuturetech-skills wechat --platform claude
```

## CLI 命令参考

| 命令 | 说明 |
| --- | --- |
| `zerofuturetech-skills --list` | 列出所有可用 skills |
| `zerofuturetech-skills --version` | 显示版本号 |
| `zerofuturetech-skills --help` | 显示帮助 |
| `zerofuturetech-skills <skill> --dry-run` | 预演安装，不实际复制文件 |
| `zerofuturetech-skills <skill> --platform <p>` | 安装到指定平台 `codex`、`openclaw` 或 `claude` |
| `zerofuturetech-skills <skill> --target <dir>` | 安装到自定义目录 |

## Skills

### `zerofuturetech-wechat-publisher`

把 Markdown 文章和配图整理成适合微信公众号草稿箱的稿件，支持预览、样式控制、封面图和正文图处理，并直接通过官方 API 发到草稿箱。

它可以做的事：

- 清理 Markdown，解析标题、摘要、作者、封面图和正文图片
- 生成 `cleaned.md`、`metadata.json` 和 `preview.html`
- 支持 3 种适合微信公众号的样式：`minimal-cn`、`tech-editorial`、`bold`
- 渲染成适合微信草稿箱的内联 HTML，并通过官方 API 发布

适合：

- 想把 Markdown 文章发到微信公众号草稿箱
- 在意排版观感，不只是"能发成功"
- 希望先预览再发布

样式自动推荐：

- `essay` → `tech-editorial`
- `tutorial` → `bold`
- `brief` → `minimal-cn`

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

### `illustrated-article-html-studio`

把主题或 Markdown 草稿整理成完整的图文一体化文章包，输出文章 Markdown、图片规划、可选生成图片和最终独立 HTML。

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
- 更有"活人感"的文章视觉系统

## 安装方式

### 方式 1：npx（推荐）

```bash
npx github:jingw2/zerofuturetech-skills wechat
npx github:jingw2/zerofuturetech-skills x-essay
npx github:jingw2/zerofuturetech-skills illustrated-article-html-studio
npx github:jingw2/zerofuturetech-skills article-thumbnail-illustrator
```

支持的别名：

| 别名 | Skill |
| --- | --- |
| `wechat` | `zerofuturetech-wechat-publisher` |
| `x-essay`、`essay` | `high-agency-x-essay-writer` |

支持的平台：

| 平台 | 安装路径 |
| --- | --- |
| `codex`（默认） | `~/.codex/skills` |
| `openclaw` | `~/.openclaw/skills` |
| `claude` | `~/.claude/agents` |

### 方式 2：全局安装

```bash
npm install -g github:jingw2/zerofuturetech-skills
zerofuturetech-skills wechat
zerofuturetech-skills x-essay --platform claude
```

### 方式 3：手动复制

```bash
cp -R skills/zerofuturetech-wechat-publisher ~/.codex/skills/
cp -R skills/high-agency-x-essay-writer ~/.codex/skills/
```

## 微信发布 Skill 配置

### 配置文件

| 路径 | 说明 |
| --- | --- |
| `.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md` | 项目级配置 |
| `~/.zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md` | 用户级配置 |
| `.zerofuturetech-skills/.env` | 项目环境变量 |
| `~/.zerofuturetech-skills/.env` | 用户环境变量 |

推荐的 `EXTEND.md`：

```
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

### 使用方式

```bash
# 准备文章
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/prepare_article.py article.md --style auto --compare-styles

# 预览
python3 ~/.codex/skills/zerofuturetech-wechat-publisher/scripts/publish_wechat.py .wechat-prep/<slug>/metadata.json --dry-run

# 发布到草稿箱
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
wechat_style: tech-editorial
need_open_comment: 1
only_fans_can_comment: 0
---
```

## 故障排查

每个 skill 的 `SKILL.md` 都有 **Gotchas** 部分，记录常见问题和解决方案：

| Skill | 常见问题 |
| --- | --- |
| `zerofuturetech-wechat-publisher` | API 凭证、图片路径、Markdown 编码 |
| `high-agency-x-essay-writer` | 观点不清晰、主张太泛、翻译腔陷阱 |
| `article-thumbnail-illustrator` | Provider 凭证、图片质量、Prompt 不够具体 |
| `illustrated-article-html-studio` | 文章结构、图片槽位格式、HTML 兼容性 |

## 说明

- 每个 skill 都是 `skills/` 下的独立目录
- `SKILL.md` 是 skill 的唯一事实来源
- `references/` 放按需读取的补充资料
- Codex 和 OpenClaw 会安装原始 skill 目录
- Claude Code 会安装 `platforms/claude/agents/` 下对应的 subagent 文件

## Star 增长图

[![Star History Chart](https://api.star-history.com/svg?repos=jingw2/zerofuturetech-skills&type=Date)](https://star-history.com/#jingw2/zerofuturetech-skills&Date)
