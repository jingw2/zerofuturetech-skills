#!/usr/bin/env python3

import argparse
import base64
import json
import os
import re
import shutil
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate thumbnail and section-image prompts or images for an article."
    )
    parser.add_argument("input", help="Markdown file path")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--title", help="Override title")
    parser.add_argument("--summary", help="Override summary")
    parser.add_argument(
        "--provider",
        choices=["openai", "gemini", "replicate", "none"],
        help="Image provider",
    )
    parser.add_argument("--model", help="Override image model")
    parser.add_argument("--size", help="Override image size")
    parser.add_argument("--aspect", help="Override thumbnail aspect ratio")
    parser.add_argument("--dry-run", action="store_true", help="Only write plan and prompt files")
    return parser.parse_args()


def split_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + 4 :].lstrip("\n")
    data: Dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data, body


def parse_key_value_text(text: str) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data


def load_settings(base_dir: Path) -> Dict[str, str]:
    settings: Dict[str, str] = {}
    for root in (base_dir.resolve(), Path.home()):
        config_path = root / ".zerofuturetech-skills" / "article-thumbnail-illustrator" / "EXTEND.md"
        env_path = root / ".zerofuturetech-skills" / ".env"
        if config_path.exists():
            settings.update(parse_key_value_text(config_path.read_text(encoding="utf-8")))
        if env_path.exists():
            for raw_line in env_path.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                settings.setdefault(key.strip(), value.strip().strip("'\""))
    for key, value in os.environ.items():
        settings[key] = value
    return settings


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    ascii_only = re.sub(r"[^\x00-\x7F]+", "", value)
    ascii_only = re.sub(r"-{2,}", "-", ascii_only).strip("-")
    return ascii_only or "article"


def resolve_title(frontmatter: Dict[str, str], body: str, override: Optional[str]) -> str:
    if override:
        return override.strip()
    if frontmatter.get("title"):
        return frontmatter["title"]
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled Article"


def resolve_summary(frontmatter: Dict[str, str], body: str, override: Optional[str]) -> str:
    if override:
        return override.strip()
    if frontmatter.get("summary"):
        return frontmatter["summary"]
    paragraphs = [line.strip() for line in body.splitlines() if line.strip() and not line.startswith("#")]
    return paragraphs[0][:140] if paragraphs else ""


def detect_article_type(frontmatter: Dict[str, str], body: str) -> str:
    if frontmatter.get("article_type"):
        return frontmatter["article_type"]
    if "```" in body or re.search(r"^\d+\.\s", body, re.M):
        return "tutorial"
    if len(body) < 1800:
        return "brief"
    return "essay"


def resolve_provider(frontmatter: Dict[str, str], settings: Dict[str, str], override: Optional[str]) -> str:
    return override or frontmatter.get("image_provider") or settings.get("default_provider", "none")


def resolve_model(provider: str, frontmatter: Dict[str, str], settings: Dict[str, str], override: Optional[str]) -> str:
    if override:
        return override
    if frontmatter.get("image_model"):
        return frontmatter["image_model"]
    defaults = {
        "openai": settings.get("default_openai_model", "gpt-image-1"),
        "gemini": settings.get("default_gemini_model", "gemini-3-pro-image-preview"),
        "replicate": settings.get("default_replicate_model", "google/nano-banana-pro"),
        "none": "",
    }
    return defaults.get(provider, "")


def resolve_size(frontmatter: Dict[str, str], settings: Dict[str, str], override: Optional[str]) -> str:
    return override or frontmatter.get("image_size") or settings.get("default_size", "1536x1024")


def resolve_aspect(frontmatter: Dict[str, str], settings: Dict[str, str], override: Optional[str]) -> str:
    return override or frontmatter.get("thumbnail_aspect") or settings.get("default_aspect", "16:9")


def choose_dimensions(article_type: str) -> Dict[str, str]:
    if article_type == "tutorial":
        return {
            "type": "diagrammatic",
            "palette": "cool",
            "rendering": "diagram",
            "text": "none",
            "mood": "balanced",
        }
    return {
        "type": "conceptual",
        "palette": "elegant",
        "rendering": "editorial-digital",
        "text": "none",
        "mood": "balanced",
    }


def request_json(url: str, payload: Optional[dict], headers: Optional[Dict[str, str]] = None, timeout: int = 120) -> dict:
    body = None
    merged_headers = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        merged_headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=merged_headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP error {exc.code}: {details}") from exc


def download_file(url: str, output_path: Path, headers: Optional[Dict[str, str]] = None) -> None:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=120) as resp:
        output_path.write_bytes(resp.read())


def generate_openai(prompt: str, model: str, size: str, output_path: Path, api_key: str) -> None:
    result = request_json(
        "https://api.openai.com/v1/images/generations",
        {"model": model, "prompt": prompt, "size": size},
        {"Authorization": f"Bearer {api_key}"},
    )
    output_path.write_bytes(base64.b64decode(result["data"][0]["b64_json"]))


def generate_gemini(prompt: str, model: str, output_path: Path, api_key: str) -> None:
    result = request_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={urllib.parse.quote(api_key)}",
        {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
        },
        None,
    )
    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                output_path.write_bytes(base64.b64decode(inline["data"]))
                return
    raise SystemExit("Gemini did not return image data.")


def parse_replicate_model(model: str) -> Tuple[str, str]:
    if "/" not in model:
        raise SystemExit(f"Replicate model must be owner/name, got: {model}")
    owner, name = model.split("/", 1)
    return owner, name


def generate_replicate(prompt: str, model: str, aspect: str, output_path: Path, api_token: str) -> None:
    owner, name = parse_replicate_model(model)
    payload = {"input": {"prompt": prompt, "aspect_ratio": aspect}}
    result = request_json(
        f"https://api.replicate.com/v1/models/{owner}/{name}/predictions",
        payload,
        {"Authorization": f"Bearer {api_token}", "Prefer": "wait=60"},
        timeout=120,
    )
    prediction = result
    get_url = prediction.get("urls", {}).get("get")
    while prediction.get("status") in ("starting", "processing") and get_url:
        time.sleep(2)
        prediction = request_json(get_url, None, {"Authorization": f"Bearer {api_token}"}, timeout=120)
    if prediction.get("status") != "succeeded":
        raise SystemExit(f"Replicate prediction failed with status {prediction.get('status')}: {prediction.get('error', '')}")
    output = prediction.get("output")
    image_url = output[0] if isinstance(output, list) else output
    if not image_url:
        raise SystemExit("Replicate did not return an image URL.")
    download_file(image_url, output_path, {"Authorization": f"Bearer {api_token}"})


def write_prompt_file(path: Path, title: str, prompt: str, meta: Dict[str, str]) -> None:
    frontmatter = ["---"] + [f"{k}: {v}" for k, v in meta.items() if v] + ["---", ""]
    path.write_text("\n".join(frontmatter) + prompt + "\n", encoding="utf-8")


def generate_asset(prompt: str, provider: str, model: str, size: str, aspect: str, settings: Dict[str, str], output_path: Path, dry_run: bool) -> Dict[str, str]:
    if provider == "none":
        return {"status": "planned", "reason": "image_provider=none", "path": ""}
    if dry_run:
        return {"status": "planned", "reason": "dry-run", "path": ""}
    if provider == "openai":
        api_key = settings.get("OPENAI_API_KEY")
        if not api_key:
            return {"status": "planned", "reason": "missing OPENAI_API_KEY", "path": ""}
        generate_openai(prompt, model, size, output_path, api_key)
        return {"status": "generated", "reason": "", "path": str(output_path)}
    if provider == "gemini":
        api_key = settings.get("GEMINI_API_KEY")
        if not api_key:
            return {"status": "planned", "reason": "missing GEMINI_API_KEY", "path": ""}
        generate_gemini(prompt, model, output_path, api_key)
        return {"status": "generated", "reason": "", "path": str(output_path)}
    if provider == "replicate":
        api_token = settings.get("REPLICATE_API_TOKEN")
        if not api_token:
            return {"status": "planned", "reason": "missing REPLICATE_API_TOKEN", "path": ""}
        generate_replicate(prompt, model, aspect, output_path, api_token)
        return {"status": "generated", "reason": "", "path": str(output_path)}
    return {"status": "planned", "reason": f"unsupported provider {provider}", "path": ""}


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    raw = input_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(raw)
    settings = load_settings(Path.cwd())

    title = resolve_title(frontmatter, body, args.title)
    summary = resolve_summary(frontmatter, body, args.summary)
    article_type = detect_article_type(frontmatter, body)
    provider = resolve_provider(frontmatter, settings, args.provider)
    model = resolve_model(provider, frontmatter, settings, args.model)
    size = resolve_size(frontmatter, settings, args.size)
    aspect = resolve_aspect(frontmatter, settings, args.aspect)
    dimensions = choose_dimensions(article_type)

    slug = slugify(title)
    output_dir = Path(args.output_dir).resolve() if args.output_dir else (input_path.parent / ".article-images" / slug).resolve()
    prompts_dir = output_dir / "prompts"
    assets_dir = output_dir / "assets"
    output_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    sections = re.findall(r"^##\s+(.+)$", body, re.M)[:3]
    thumbnail_prompt = (
        f"{dimensions['type']} editorial thumbnail for article '{title}'. "
        f"Summary: {summary}. Palette: {dimensions['palette']}. Rendering: {dimensions['rendering']}. "
        f"Mood: {dimensions['mood']}. Composition should feel intentional, human, publication-quality, no random AI glow, no meaningless futuristic clutter, no text."
    )
    write_prompt_file(
        prompts_dir / "thumbnail.md",
        title,
        thumbnail_prompt,
        {
            "slot": "thumbnail",
            "provider": provider,
            "model": model,
            "aspect": aspect,
            "size": size,
        },
    )
    thumbnail_result = generate_asset(
        thumbnail_prompt,
        provider,
        model,
        size,
        aspect,
        settings,
        assets_dir / "thumbnail.png",
        args.dry_run,
    )

    planned_sections: List[Dict[str, str]] = []
    for index, section in enumerate(sections, start=1):
        section_prompt = (
            f"Editorial section illustration for article '{title}', section '{section}'. "
            f"Use the same visual family as the thumbnail. "
            f"Concept-driven, clean composition, human editorial feel, no text overlay."
        )
        prompt_path = prompts_dir / f"section-{index:02d}.md"
        write_prompt_file(
            prompt_path,
            title,
            section_prompt,
            {
                "slot": f"section-{index:02d}",
                "provider": provider,
                "model": model,
                "aspect": aspect,
                "size": size,
            },
        )
        asset_path = assets_dir / f"section-{index:02d}.png"
        result = generate_asset(section_prompt, provider, model, size, aspect, settings, asset_path, args.dry_run)
        planned_sections.append(
            {
                "section_title": section,
                "prompt_file": str(prompt_path),
                "prompt": section_prompt,
                "status": result["status"],
                "reason": result["reason"],
                "asset_path": result["path"],
            }
        )

    image_plan = {
        "title": title,
        "summary": summary,
        "article_type": article_type,
        "provider": provider,
        "model": model,
        "size": size,
        "aspect": aspect,
        "dimensions": dimensions,
        "thumbnail": {
            "prompt_file": str(prompts_dir / "thumbnail.md"),
            "prompt": thumbnail_prompt,
            "status": thumbnail_result["status"],
            "reason": thumbnail_result["reason"],
            "asset_path": thumbnail_result["path"],
        },
        "sections": planned_sections,
    }
    (output_dir / "image-plan.json").write_text(json.dumps(image_plan, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "thumbnail_prompt": str(prompts_dir / "thumbnail.md"),
                "image_plan": str(output_dir / "image-plan.json"),
                "generated_assets": [item["asset_path"] for item in [image_plan["thumbnail"], *planned_sections] if item.get("asset_path")],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
