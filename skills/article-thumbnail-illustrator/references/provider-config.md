# Provider Config

Use this file when the skill needs to generate real images.

## Supported Providers

- `openai`
- `gemini`
- `none`

## Defaults

- OpenAI model: `gpt-image-1`
- Gemini model: `gemini-3-pro-image-preview`

## Env Vars

### OpenAI

```bash
OPENAI_API_KEY=your_openai_api_key
```

### Gemini

```bash
GEMINI_API_KEY=your_gemini_api_key
```

## Optional Config

- `.zerofuturetech-skills/article-thumbnail-illustrator/EXTEND.md`
- `~/.zerofuturetech-skills/article-thumbnail-illustrator/EXTEND.md`

Example:

```md
default_provider: openai
default_openai_model: gpt-image-1
default_gemini_model: gemini-3-pro-image-preview
default_aspect: 16:9
default_size: 1536x1024
```

## Fallback

If credentials are missing:

- still write prompt files
- still write `image-plan.json`
- do not fail the planning workflow
