# Description Field Examples

Read this file when generating the `description` field for a new skill's SKILL.md frontmatter.

The description field is read by Claude at session start to build a listing of available skills. It decides **when to trigger** a skill, not **what the skill does**. Write it for the model, not for a human reader.

## The Formula

```
[Verb phrase describing the core action], [optional elaboration on scope or method]. Use when [specific trigger conditions from the model's perspective].
```

## Good Examples (from this repository)

### Example 1: zerofuturetech-wechat-publisher

```
Prepare polished, WeChat-draft-ready articles from Markdown and image assets, then publish them directly to the WeChat Official Account draft box through the official API. Use when Codex receives a Markdown article, article images, cover image, or mixed writing assets and needs to optimize typography, spacing, headings, image rhythm, frontmatter, and WeChat metadata before sending the result to 微信公众号草稿箱.
```

**Why it works**:
- Starts with a verb phrase ("Prepare polished")
- Specifies the method ("through the official API")
- "Use when" condition is specific: lists the exact types of input that trigger this skill
- Names the specific destination ("微信公众号草稿箱") so the model can disambiguate from generic publishing

### Example 2: high-agency-x-essay-writer

```
Draft and rewrite long-form X articles and essay threads that use high-agency, contrarian, self-improvement and systems-thinking structures inspired by public creator essays, without imitating any living author's exact voice. Use when Codex receives raw notes, prompts, outlines, journal entries, arguments, or examples and needs to turn them into punchy long-form posts with strong hooks, clean logic, practical frameworks, and reflective but assertive tone.
```

**Why it works**:
- Starts with a verb phrase ("Draft and rewrite")
- Specifies the quality bar inline ("without imitating any living author's exact voice")
- "Use when" lists specific input types (raw notes, outlines, journal entries) that distinguish this from a general writing skill

### Example 3: article-thumbnail-illustrator

```
Generate thumbnails and article illustration images for essays, newsletters, and editorial pages by combining structured cover-image direction inspired by baoyu-cover-image with configurable image providers inspired by baoyu-image-gen. Use when Codex receives an article, theme, title, summary, or Markdown draft and needs to output thumbnail prompts, section-image prompts, or actual generated images for cover and inline article use.
```

**Why it works**:
- Starts with a verb phrase ("Generate thumbnails")
- Names the specific output types (thumbnail prompts, section-image prompts, generated images)
- "Use when" distinguishes from the full article studio (images only, not full HTML)

## Bad Examples (with annotations)

### Bad Example 1: Summary disguised as description

```
This skill handles WeChat publishing. It can prepare Markdown articles and publish them to WeChat. It supports multiple styles and handles images.
```

**Why it fails**:
- Starts with "This skill" (noun phrase, not verb)
- No "Use when" clause — the model cannot decide when to trigger it
- Generic ("handles images") instead of specific

### Bad Example 2: Feature list

```
Features: Markdown cleanup, style selection (minimal-cn, tech-editorial, bold), image uploading, API publishing, preview generation, frontmatter parsing.
```

**Why it fails**:
- No verb phrase
- No trigger conditions
- A feature list does not help the model decide when to use the skill

### Bad Example 3: Too vague to disambiguate

```
Write essays and articles in a strong, opinionated style. Use when the user wants to write something.
```

**Why it fails**:
- "Use when the user wants to write something" matches almost every conversation — the model will trigger this skill constantly
- No specificity about input types or output targets

### Bad Example 4: Too long and losing the trigger

```
This is a comprehensive skill for creating illustrated articles with HTML output. It uses the high-agency writing workflow developed internally, combined with image generation from OpenAI or Gemini, and produces a final standalone HTML file that can be published anywhere. It supports editorial, minimal, and bold HTML styles. The image planning system infers cover and section images automatically. Use when you want a complete article.
```

**Why it fails**:
- Over-explains the internals (the model doesn't need to know how it works in the description)
- "Use when you want a complete article" is too broad
- Should compress the preamble and make "Use when" more specific about inputs

## Template for New Skills

```
[Verb phrase that names the core action and optionally the method or scope], [one optional clause about what makes this skill distinct]. Use when [specific input types or user intentions that should trigger this skill but not similar skills].
```

Keep the total description under 100 words. If you need more than 100 words, the trigger conditions are probably too broad.
