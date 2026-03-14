#!/usr/bin/env python3

import argparse
import base64
import html
import json
import os
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple


IMAGE_DIRECTIVE_RE = re.compile(r"^\[\[image:\s*(cover|section)\s*\|\s*(.+?)\s*\]\]$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an illustrated editorial HTML article from Markdown."
    )
    parser.add_argument("input", help="Markdown file path")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--title", help="Override title")
    parser.add_argument("--summary", help="Override summary")
    parser.add_argument("--author", help="Override author")
    parser.add_argument(
        "--article-type",
        choices=["essay", "tutorial", "brief"],
        help="Override article type",
    )
    parser.add_argument(
        "--html-style",
        choices=["editorial", "minimal", "bold"],
        help="Override HTML style",
    )
    parser.add_argument(
        "--image-provider",
        choices=["openai", "gemini", "none"],
        help="Override image provider",
    )
    parser.add_argument("--image-model", help="Override image model")
    parser.add_argument("--image-size", help="Override image size")
    parser.add_argument("--dry-run", action="store_true", help="Do not call image APIs")
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


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    ascii_only = re.sub(r"[^\x00-\x7F]+", "", value)
    ascii_only = re.sub(r"-{2,}", "-", ascii_only).strip("-")
    return ascii_only or "article"


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
        config_path = root / ".zerofuturetech-skills" / "illustrated-article-html-studio" / "EXTEND.md"
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


def resolve_title(frontmatter: Dict[str, str], body: str, override: Optional[str]) -> str:
    if override:
        return override.strip()
    if frontmatter.get("title"):
        return frontmatter["title"].strip()
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled Article"


def resolve_summary(frontmatter: Dict[str, str], body: str, override: Optional[str]) -> str:
    if override:
        return override.strip()
    if frontmatter.get("summary"):
        return frontmatter["summary"].strip()
    paragraphs = [line.strip() for line in body.splitlines() if line.strip() and not line.startswith("#")]
    return paragraphs[0][:140] if paragraphs else ""


def resolve_author(frontmatter: Dict[str, str], settings: Dict[str, str], override: Optional[str]) -> str:
    if override:
        return override.strip()
    return frontmatter.get("author") or settings.get("default_author", "Zero Future Tech")


def detect_article_type(body: str, override: Optional[str]) -> str:
    if override:
        return override
    if "```" in body or re.search(r"^\d+\.\s", body, re.M):
        return "tutorial"
    if len(body) < 1800:
        return "brief"
    return "essay"


def resolve_html_style(frontmatter: Dict[str, str], settings: Dict[str, str], article_type: str, override: Optional[str]) -> str:
    if override:
        return override
    if frontmatter.get("html_style"):
        return frontmatter["html_style"]
    if settings.get("default_html_style"):
        return settings["default_html_style"]
    return {
        "essay": "editorial",
        "tutorial": "bold",
        "brief": "minimal",
    }.get(article_type, "editorial")


def resolve_image_provider(frontmatter: Dict[str, str], settings: Dict[str, str], override: Optional[str]) -> str:
    if override:
        return override
    return frontmatter.get("image_provider") or settings.get("default_image_provider", "none")


def resolve_image_model(provider: str, frontmatter: Dict[str, str], settings: Dict[str, str], override: Optional[str]) -> str:
    if override:
        return override
    if frontmatter.get("image_model"):
        return frontmatter["image_model"]
    if provider == "openai":
        return settings.get("default_openai_image_model", "gpt-image-1")
    if provider == "gemini":
        return settings.get("default_gemini_image_model", "gemini-3-pro-image-preview")
    return ""


def resolve_image_size(frontmatter: Dict[str, str], settings: Dict[str, str], override: Optional[str]) -> str:
    if override:
        return override
    return frontmatter.get("image_size") or settings.get("default_image_size", "1536x1024")


def normalize_markdown(body: str, title: str) -> str:
    lines = body.splitlines()
    if lines and lines[0].startswith("# ") and lines[0][2:].strip() == title.strip():
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def extract_markdown_images(body: str) -> List[Tuple[str, str]]:
    return re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", body)


def copy_body_images(body: str, article_dir: Path, assets_dir: Path) -> str:
    rewritten: Dict[str, str] = {}
    for _, image_path in extract_markdown_images(body):
        if re.match(r"^https?://", image_path):
            continue
        source = Path(image_path)
        if not source.is_absolute():
            source = (article_dir / image_path).resolve()
        if not source.exists():
            continue
        target = assets_dir / source.name
        if source != target:
            shutil.copy2(source, target)
        rewritten[image_path] = f"assets/{target.name}"

    def replace(match: re.Match) -> str:
        alt_text = match.group(1)
        image_path = match.group(2)
        new_path = rewritten.get(image_path, image_path)
        return f"![{alt_text}]({new_path})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace, body)


def extract_image_directives(body: str) -> Tuple[str, List[Dict[str, str]]]:
    slots: List[Dict[str, str]] = []
    kept_lines: List[str] = []
    current_section = ""
    for raw in body.splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            current_section = line[3:].strip()
        match = IMAGE_DIRECTIVE_RE.match(line.strip())
        if match:
            slots.append(
                {
                    "slot_type": match.group(1),
                    "prompt": match.group(2),
                    "section_title": current_section,
                }
            )
            continue
        kept_lines.append(raw)
    return "\n".join(kept_lines).strip() + "\n", slots


def infer_image_slots(title: str, summary: str, body: str) -> List[Dict[str, str]]:
    slots = [
        {
            "slot_type": "cover",
            "prompt": f"Editorial hero illustration for '{title}'. {summary}. Clean composition, no text, visually striking, publication-quality.",
            "section_title": "",
        }
    ]
    section_titles = re.findall(r"^##\s+(.+)$", body, re.M)[:2]
    for section in section_titles:
        slots.append(
            {
                "slot_type": "section",
                "prompt": f"Section illustration for '{section}' in article '{title}'. Editorial style, concept-driven, no text overlay.",
                "section_title": section,
            }
        )
    return slots


def request_json(url: str, payload: Optional[dict], headers: Optional[Dict[str, str]] = None) -> dict:
    body = None
    merged_headers = dict(headers or {})
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        merged_headers.setdefault("Content-Type", "application/json")
    request = urllib.request.Request(url, data=body, headers=merged_headers)
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP error {exc.code}: {details}") from exc


def generate_openai_image(prompt: str, model: str, size: str, output_path: Path, api_key: str) -> None:
    result = request_json(
        "https://api.openai.com/v1/images/generations",
        {
            "model": model,
            "prompt": prompt,
            "size": size,
        },
        {"Authorization": f"Bearer {api_key}"},
    )
    image_b64 = result["data"][0]["b64_json"]
    output_path.write_bytes(base64.b64decode(image_b64))


def generate_gemini_image(prompt: str, model: str, output_path: Path, api_key: str) -> None:
    result = request_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={urllib.parse.quote(api_key)}",
        {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
        },
        None,
    )
    for candidate in result.get("candidates", []):
        parts = candidate.get("content", {}).get("parts", [])
        for part in parts:
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                output_path.write_bytes(base64.b64decode(inline["data"]))
                return
    raise SystemExit("Gemini image response did not contain inline image data.")


def ensure_image_asset(slot: Dict[str, str], index: int, provider: str, model: str, size: str, settings: Dict[str, str], assets_dir: Path, dry_run: bool) -> Dict[str, str]:
    extension = ".png"
    output_path = assets_dir / f"{slot['slot_type']}-{index + 1}{extension}"
    missing_reason = ""
    status = "planned"
    if provider == "none":
        missing_reason = "image_provider=none"
    elif dry_run:
        missing_reason = "dry-run"
    elif provider == "openai":
        api_key = settings.get("OPENAI_API_KEY")
        if not api_key:
            missing_reason = "missing OPENAI_API_KEY"
        else:
            generate_openai_image(slot["prompt"], model, size, output_path, api_key)
            status = "generated"
    elif provider == "gemini":
        api_key = settings.get("GEMINI_API_KEY")
        if not api_key:
            missing_reason = "missing GEMINI_API_KEY"
        else:
            generate_gemini_image(slot["prompt"], model, output_path, api_key)
            status = "generated"
    return {
        **slot,
        "status": status,
        "reason": missing_reason,
        "asset_path": str(output_path) if output_path.exists() else "",
        "asset_name": output_path.name,
    }


def render_inline_text(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def layout_palette(style: str) -> Dict[str, str]:
    palettes = {
        "editorial": {"bg": "#eef2f6", "paper": "#fbfcfe", "accent": "#245fba", "soft": "#eef4fb", "text": "#1a2632"},
        "minimal": {"bg": "#f5f2ea", "paper": "#fffdf8", "accent": "#8e774e", "soft": "#f4efe3", "text": "#222222"},
        "bold": {"bg": "#ecebe7", "paper": "#ffffff", "accent": "#1f7a5c", "soft": "#eaf6f0", "text": "#18252b"},
    }
    return palettes.get(style, palettes["editorial"])


def render_image_block(slot: Dict[str, str]) -> str:
    if slot.get("asset_path"):
        src = f"assets/{html.escape(slot['asset_name'])}"
        caption = html.escape(slot.get("section_title") or slot["slot_type"])
        return f'<figure class="article-figure"><img src="{src}" alt="{caption}" /><figcaption>{caption}</figcaption></figure>'
    reason = html.escape(slot.get("reason", "image planned"))
    return (
        '<div class="image-placeholder">'
        f'<div class="image-placeholder-label">{html.escape(slot["slot_type"])} image</div>'
        f'<div class="image-placeholder-reason">{reason}</div>'
        "</div>"
    )


def build_body_html(body: str, section_images: List[Dict[str, str]]) -> str:
    section_image_map = {slot.get("section_title"): slot for slot in section_images if slot.get("section_title")}
    html_parts: List[str] = []
    list_type: Optional[str] = None
    in_code = False
    code_lines: List[str] = []

    def flush_list() -> None:
        nonlocal list_type
        if list_type:
            html_parts.append(f"</{list_type}>")
            list_type = None

    def flush_code() -> None:
        nonlocal in_code, code_lines
        if in_code:
            html_parts.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
            in_code = False
            code_lines = []

    for raw in body.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            flush_list()
            if in_code:
                flush_code()
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            flush_list()
            continue
        if line.startswith("### "):
            flush_list()
            html_parts.append(f"<h3>{render_inline_text(line[4:].strip())}</h3>")
        elif line.startswith("## "):
            flush_list()
            section_title = line[3:].strip()
            html_parts.append(f"<h2>{render_inline_text(section_title)}</h2>")
            slot = section_image_map.get(section_title)
            if slot:
                html_parts.append(render_image_block(slot))
        elif line.startswith("# "):
            flush_list()
        elif line.startswith("> "):
            flush_list()
            html_parts.append(f"<blockquote><p>{render_inline_text(line[2:].strip())}</p></blockquote>")
        elif re.match(r"^[-*]\s", line):
            if list_type != "ul":
                flush_list()
                html_parts.append("<ul>")
                list_type = "ul"
            html_parts.append(f"<li>{render_inline_text(line[2:].strip())}</li>")
        elif re.match(r"^\d+\.\s", line):
            if list_type != "ol":
                flush_list()
                html_parts.append("<ol>")
                list_type = "ol"
            item = re.sub(r"^\d+\.\s*", "", line)
            html_parts.append(f"<li>{render_inline_text(item)}</li>")
        elif re.match(r"!\[[^\]]*\]\(([^)]+)\)", line):
            flush_list()
            match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
            alt = match.group(1) if match else ""
            src = match.group(2) if match else ""
            caption = html.escape(alt) if alt else ""
            html_parts.append(
                f'<figure class="article-figure"><img src="{html.escape(src)}" alt="{html.escape(alt)}" />'
                + (f"<figcaption>{caption}</figcaption>" if caption else "")
                + "</figure>"
            )
        else:
            flush_list()
            html_parts.append(f"<p>{render_inline_text(line.strip())}</p>")

    flush_list()
    flush_code()
    return "".join(html_parts)


def build_html(title: str, summary: str, author: str, style: str, cover_slot: Optional[Dict[str, str]], body_html: str) -> str:
    palette = layout_palette(style)
    cover_html = render_image_block(cover_slot) if cover_slot else ""
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: {palette['bg']}; color: {palette['text']}; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", sans-serif; }}
    .shell {{ max-width: 1024px; margin: 0 auto; padding: 32px 18px 64px; }}
    .page {{ max-width: 780px; margin: 0 auto; background: {palette['paper']}; border-radius: 28px; overflow: hidden; box-shadow: 0 22px 60px rgba(0,0,0,0.08); }}
    .hero {{ padding: 28px 28px 8px; background: linear-gradient(180deg, {palette['soft']} 0%, {palette['paper']} 100%); }}
    .hero .image-placeholder, .hero .article-figure {{ margin-bottom: 0; }}
    .article {{ padding: 22px 28px 60px; line-height: 1.82; }}
    .eyebrow {{ color: {palette['accent']}; text-transform: uppercase; letter-spacing: 0.08em; font-size: 12px; font-weight: 700; }}
    h1 {{ margin: 10px 0 0; font-size: 40px; line-height: 1.15; }}
    .summary {{ margin: 16px 0 0; font-size: 18px; line-height: 1.75; color: #59646e; }}
    .meta {{ margin: 18px 0 0; padding-bottom: 18px; border-bottom: 1px solid rgba(0,0,0,0.06); font-size: 14px; color: #6d7780; }}
    h2 {{ margin: 36px 0 14px; font-size: 26px; line-height: 1.35; color: {palette['accent']}; }}
    h3 {{ margin: 28px 0 10px; font-size: 20px; line-height: 1.45; }}
    p {{ margin: 0 0 16px; font-size: 17px; }}
    ul, ol {{ margin: 0 0 18px; padding-left: 1.4em; }}
    li {{ margin-bottom: 10px; font-size: 16.5px; }}
    blockquote {{ margin: 24px 0; padding: 16px 18px; background: {palette['soft']}; border-left: 4px solid {palette['accent']}; }}
    pre {{ margin: 24px 0; overflow-x: auto; padding: 14px 16px; background: #111827; color: #f3f4f6; border-radius: 14px; }}
    code {{ background: rgba(0,0,0,0.05); padding: 0.15em 0.4em; border-radius: 6px; }}
    .article-figure {{ margin: 28px 0; }}
    .article-figure img {{ width: 100%; display: block; border-radius: 18px; }}
    .article-figure figcaption {{ margin-top: 10px; font-size: 13px; color: #76818b; text-align: center; }}
    .image-placeholder {{ margin: 28px 0; border-radius: 18px; padding: 28px; min-height: 180px; background: linear-gradient(135deg, {palette['soft']} 0%, #ffffff 100%); border: 1px dashed rgba(0,0,0,0.12); display: flex; flex-direction: column; justify-content: center; gap: 8px; }}
    .image-placeholder-label {{ font-size: 18px; font-weight: 700; color: {palette['accent']}; }}
    .image-placeholder-reason {{ font-size: 14px; color: #6d7780; }}
    @media (max-width: 640px) {{
      .shell {{ padding: 12px 6px 24px; }}
      .page {{ border-radius: 0; }}
      .hero {{ padding: 18px 18px 6px; }}
      .article {{ padding: 18px 18px 40px; }}
      h1 {{ font-size: 32px; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <div class="page">
      <div class="hero">
        {cover_html}
        <div class="eyebrow">Illustrated Article</div>
        <h1>{html.escape(title)}</h1>
        <p class="summary">{html.escape(summary)}</p>
        <div class="meta">{html.escape(author)}</div>
      </div>
      <div class="article">
        {body_html}
      </div>
    </div>
  </div>
</body>
</html>"""


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
    author = resolve_author(frontmatter, settings, args.author)
    article_type = detect_article_type(body, args.article_type or frontmatter.get("article_type"))
    html_style = resolve_html_style(frontmatter, settings, article_type, args.html_style)
    image_provider = resolve_image_provider(frontmatter, settings, args.image_provider)
    image_model = resolve_image_model(image_provider, frontmatter, settings, args.image_model)
    image_size = resolve_image_size(frontmatter, settings, args.image_size)

    body = normalize_markdown(body, title)
    body, explicit_slots = extract_image_directives(body)
    slots = explicit_slots or infer_image_slots(title, summary, body)

    slug = slugify(title)
    output_dir = Path(args.output_dir).resolve() if args.output_dir else (input_path.parent / ".illustrated-article" / slug).resolve()
    assets_dir = output_dir / "assets"
    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)
    body = copy_body_images(body, input_path.parent, assets_dir)

    resolved_slots = [
        ensure_image_asset(slot, index, image_provider, image_model, image_size, settings, assets_dir, args.dry_run)
        for index, slot in enumerate(slots)
    ]
    cover_slot = next((slot for slot in resolved_slots if slot["slot_type"] == "cover"), None)
    section_slots = [slot for slot in resolved_slots if slot["slot_type"] == "section"]

    article_md = {
        "title": title,
        "author": author,
        "summary": summary,
        "article_type": article_type,
        "html_style": html_style,
        "image_provider": image_provider,
    }
    if image_model:
        article_md["image_model"] = image_model
    if image_size:
        article_md["image_size"] = image_size
    article_markdown = "---\n" + "\n".join(f"{k}: {v}" for k, v in article_md.items()) + "\n---\n\n" + body
    (output_dir / "article.md").write_text(article_markdown, encoding="utf-8")

    image_plan = {
        "provider": image_provider,
        "model": image_model,
        "size": image_size,
        "slots": resolved_slots,
    }
    (output_dir / "image-plan.json").write_text(json.dumps(image_plan, ensure_ascii=False, indent=2), encoding="utf-8")

    body_html = build_body_html(body, section_slots)
    final_html = build_html(title, summary, author, html_style, cover_slot, body_html)
    (output_dir / "article.html").write_text(final_html, encoding="utf-8")

    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "article_markdown": str(output_dir / "article.md"),
                "article_html": str(output_dir / "article.html"),
                "image_plan": str(output_dir / "image-plan.json"),
                "provider": image_provider,
                "html_style": html_style,
                "generated_images": [slot["asset_name"] for slot in resolved_slots if slot.get("asset_path")],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
