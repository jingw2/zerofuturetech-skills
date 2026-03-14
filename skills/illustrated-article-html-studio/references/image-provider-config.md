# Image Provider Config

Use this file when the article bundle needs generated images.

## Supported Providers

- `openai`
- `gemini`
- `none`

## Env Vars

### OpenAI

```bash
OPENAI_API_KEY=your_openai_api_key
```

Default model:

- `gpt-image-1`

### Gemini

```bash
GEMINI_API_KEY=your_gemini_api_key
```

Default model:

- `gemini-3-pro-image-preview`

## Recommended Project Config

Place settings in either:

- `.zerofuturetech-skills/illustrated-article-html-studio/EXTEND.md`
- `~/.zerofuturetech-skills/illustrated-article-html-studio/EXTEND.md`

Example:

```md
default_author: Zero Future Tech
default_html_style: editorial
default_image_provider: openai
default_openai_image_model: gpt-image-1
default_gemini_image_model: gemini-3-pro-image-preview
default_image_size: 1536x1024
```

## Fallback Behavior

If credentials are missing:

- do not fail the whole article bundle
- emit `image-plan.json`
- render placeholder blocks in the final HTML
- report the missing env vars clearly
