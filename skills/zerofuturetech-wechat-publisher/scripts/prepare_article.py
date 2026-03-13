#!/usr/bin/env python3

import argparse
import html
import json
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple


COVER_ALIASES = ("cover", "coverImage", "featureImage", "image")
STYLE_PRESETS = ("minimal-cn", "tech-editorial", "bold")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare a Markdown article for WeChat draft publishing."
    )
    parser.add_argument("input", help="Markdown file path")
    parser.add_argument("--cover", help="Explicit cover image path")
    parser.add_argument("--images-dir", help="Directory containing article images")
    parser.add_argument("--title", help="Override article title")
    parser.add_argument("--summary", help="Override article summary")
    parser.add_argument("--author", help="Override article author")
    parser.add_argument(
        "--article-type",
        choices=["essay", "tutorial", "brief"],
        help="Override article type",
    )
    parser.add_argument("--theme", help="Override WeChat theme")
    parser.add_argument("--color", help="Override WeChat color")
    parser.add_argument(
        "--style",
        choices=("auto",) + STYLE_PRESETS,
        help="Preview style preset. Use auto to recommend based on article type.",
    )
    parser.add_argument(
        "--compare-styles",
        action="store_true",
        help="Generate preview variants for all style presets.",
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory. Defaults to <article-dir>/.wechat-prep/<slug>",
    )
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
    if not value:
        return "article"
    ascii_only = re.sub(r"[^\x00-\x7F]+", "", value)
    ascii_only = re.sub(r"-{2,}", "-", ascii_only).strip("-")
    return ascii_only or "article"


def resolve_title(frontmatter: Dict[str, str], body: str, override: Optional[str]) -> str:
    if override:
        return override.strip()
    if frontmatter.get("title"):
        return frontmatter["title"].strip()
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    for line in body.splitlines():
        if line.strip():
            return line.strip()[:60]
    return "Untitled Article"


def resolve_summary(frontmatter: Dict[str, str], body: str, override: Optional[str]) -> str:
    if override:
        return override.strip()
    for key in ("summary", "digest", "description"):
        if frontmatter.get(key):
            return frontmatter[key].strip()
    paragraphs = [
        line.strip()
        for line in body.splitlines()
        if line.strip() and not line.startswith("#") and not line.startswith("![")
    ]
    if not paragraphs:
        return ""
    summary = paragraphs[0]
    return summary[:117] + "..." if len(summary) > 120 else summary


def resolve_author(frontmatter: Dict[str, str], override: Optional[str]) -> str:
    if override:
        return override.strip()
    return frontmatter.get("author", "").strip()


def detect_article_type(body: str, override: Optional[str]) -> str:
    if override:
        return override
    if "```" in body or re.search(r"^\d+\.\s", body, re.M):
        return "tutorial"
    if len(re.findall(r"^##\s", body, re.M)) <= 2 and len(body) < 1800:
        return "brief"
    return "essay"


def normalize_markdown(body: str, title: str) -> str:
    lines = body.splitlines()
    if lines and lines[0].startswith("# ") and lines[0][2:].strip() == title.strip():
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"([。！？；：])([^\n ])", r"\1 \2", text)
    return text.strip() + "\n"


def extract_markdown_images(body: str) -> List[str]:
    return re.findall(r"!\[[^\]]*\]\(([^)]+)\)", body)


def resolve_cover(
    frontmatter: Dict[str, str],
    explicit_cover: Optional[str],
    article_dir: Path,
    inline_images: List[str],
) -> str:
    candidates: List[str] = []
    if explicit_cover:
        candidates.append(explicit_cover)
    for key in COVER_ALIASES:
        if frontmatter.get(key):
            candidates.append(frontmatter[key])
    candidates.append("imgs/cover.png")
    if inline_images:
        candidates.append(inline_images[0])

    for candidate in candidates:
        candidate_path = Path(candidate)
        if candidate_path.is_absolute() and candidate_path.exists():
            return str(candidate_path)
        resolved = (article_dir / candidate).resolve()
        if resolved.exists():
            return str(resolved)
    return ""


def copy_asset_if_exists(asset: str, article_dir: Path, output_dir: Path) -> str:
    if not asset:
        return ""
    source = Path(asset)
    if not source.is_absolute():
        source = (article_dir / asset).resolve()
    if not source.exists():
        return ""
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    target = assets_dir / source.name
    if source != target:
        shutil.copy2(source, target)
    return str(target)


def rewrite_markdown_image_paths(
    body: str,
    rewritten_map: Dict[str, str],
    output_dir: Path,
) -> str:
    def replace(match: re.Match) -> str:
        alt_text = match.group(1)
        original_path = match.group(2)
        replacement = rewritten_map.get(original_path)
        if not replacement:
            return match.group(0)
        relative_path = os.path.relpath(replacement, output_dir)
        return f"![{alt_text}]({relative_path})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace, body)


def render_inline_text(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped


def resolve_preview_palette(theme: str, color: str) -> Dict[str, str]:
    named = {
        "green": {"accent": "#1f7a5c", "accent_soft": "#eaf6f0", "accent_line": "#89b89f"},
        "blue": {"accent": "#245fba", "accent_soft": "#eef4ff", "accent_line": "#9bb8ee"},
        "red": {"accent": "#a13f35", "accent_soft": "#fff2ef", "accent_line": "#e2b2aa"},
        "orange": {"accent": "#b96a2c", "accent_soft": "#fff5eb", "accent_line": "#ecc7a2"},
    }
    theme_defaults = {
        "default": "green",
        "grace": "red",
        "simple": "green",
        "modern": "orange",
    }
    key = color or theme_defaults.get(theme, "green")
    if key in named:
        return named[key]
    if re.fullmatch(r"#[0-9a-fA-F]{6}", key):
        return {"accent": key, "accent_soft": "#f5f7f8", "accent_line": "#cfd8dc"}
    return named["green"]


def resolve_style_preset(style: str) -> Dict[str, str]:
    presets = {
        "bold": {
            "page_radius": "24px",
            "header_layout": "balanced",
            "hero_padding": "10px",
            "h2_mode": "solid-box",
            "body_bg": "linear-gradient(180deg, #f4f5f6 0%, #e8eaed 100%)",
        },
        "minimal-cn": {
            "page_radius": "0px",
            "header_layout": "minimal-cn",
            "hero_padding": "0",
            "h2_mode": "minimal-line",
            "body_bg": "#f7f7f5",
        },
        "tech-editorial": {
            "page_radius": "24px",
            "header_layout": "tech-editorial",
            "hero_padding": "0",
            "h2_mode": "tech-line",
            "body_bg": "linear-gradient(180deg, #eef2f6 0%, #e7ebf0 100%)",
        },
    }
    return presets.get(style, presets["tech-editorial"])


def recommend_style(article_type: str) -> str:
    mapping = {
        "essay": "tech-editorial",
        "tutorial": "bold",
        "brief": "minimal-cn",
    }
    return mapping.get(article_type, "tech-editorial")


def build_preview_html(
    title: str,
    summary: str,
    article_type: str,
    body: str,
    cover_image: str,
    author: str,
    theme: str,
    color: str,
    output_dir: Path,
    style: str,
) -> str:
    lines = body.splitlines()
    html_parts: List[str] = []
    list_type: Optional[str] = None
    in_code = False
    code_lines: List[str] = []
    palette = resolve_preview_palette(theme, color)
    style_preset = resolve_style_preset(style)
    type_class = f"type-{article_type}"
    style_class = f"style-{style}"

    def flush_list() -> None:
        nonlocal list_type
        if list_type:
            html_parts.append(f"</{list_type}>")
            list_type = None

    def flush_code() -> None:
        nonlocal in_code, code_lines
        if in_code:
            code = "\n".join(code_lines)
            html_parts.append(f"<pre><code>{html.escape(code)}</code></pre>")
            in_code = False
            code_lines = []

    for raw in lines:
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
            html_parts.append(f"<h2>{render_inline_text(line[3:].strip())}</h2>")
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
            html_parts.append(
                f"<figure><img src=\"{html.escape(src)}\" alt=\"{html.escape(alt)}\" />"
                + (f"<figcaption>{html.escape(alt)}</figcaption>" if alt else "")
                + "</figure>"
            )
        else:
            flush_list()
            html_parts.append(f"<p>{render_inline_text(line.strip())}</p>")

    flush_list()
    flush_code()

    hero_html = ""
    if cover_image:
        cover_src = html.escape(os.path.relpath(cover_image, output_dir))
        hero_html = (
            "<div class=\"hero\">"
            f"<img class=\"hero-image\" src=\"{cover_src}\" alt=\"cover\" />"
            "</div>"
        )

    author_html = f"<span>{html.escape(author)}</span>" if author else "<span>Zero Future Tech Preview</span>"
    css = f"""
    :root {{
      --accent: {palette['accent']};
      --accent-soft: {palette['accent_soft']};
      --accent-line: {palette['accent_line']};
      --text-main: #1f1f1f;
      --text-sub: #59636b;
      --paper: #ffffff;
      --bg: #eef1f3;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: {style_preset['body_bg']}; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", sans-serif; color: var(--text-main); }}
    .shell {{ max-width: 860px; margin: 0 auto; padding: 32px 18px 56px; }}
    .phone-hint {{ margin: 0 auto 16px; max-width: 720px; color: #7a848d; font-size: 12px; letter-spacing: 0.03em; }}
    .page {{ max-width: 720px; margin: 0 auto; background: var(--paper); border-radius: {style_preset['page_radius']}; overflow: hidden; box-shadow: 0 20px 60px rgba(27, 39, 51, 0.08); }}
    .hero {{ background: var(--accent-soft); padding: {style_preset['hero_padding']}; }}
    .hero-image {{ width: 100%; display: block; border-radius: 16px; }}
    .article {{ padding: 26px 24px 54px; line-height: 1.84; position: relative; }}
    .article-header {{ margin-bottom: 26px; }}
    .type-badge {{ display: inline-flex; align-items: center; gap: 8px; margin-bottom: 14px; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent); }}
    .type-badge::before {{ content: ""; width: 8px; height: 8px; border-radius: 99px; background: var(--accent); display: inline-block; }}
    h1 {{ margin: 0; font-size: 33px; line-height: 1.28; letter-spacing: -0.02em; }}
    .summary {{ margin: 16px 0 0; font-size: 17px; line-height: 1.75; color: var(--text-sub); }}
    .summary-box {{ margin-top: 16px; }}
    .meta {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; margin: 18px 0 28px; padding-bottom: 18px; border-bottom: 1px solid #edf1f3; font-size: 13px; color: #7d8790; }}
    .meta strong {{ color: var(--accent); font-weight: 600; }}
    h2 {{ margin: 34px 0 14px; font-size: 24px; line-height: 1.4; padding-left: 12px; border-left: 4px solid var(--accent); }}
    h3 {{ margin: 26px 0 10px; font-size: 20px; line-height: 1.5; color: #24303a; }}
    p {{ margin: 0 0 16px; font-size: 17px; }}
    strong {{ color: #14232c; font-weight: 700; }}
    em {{ font-style: normal; color: var(--accent); }}
    code {{ padding: 0.15em 0.42em; border-radius: 6px; background: #f4f7f9; font-size: 0.92em; }}
    ul, ol {{ margin: 0 0 18px; padding-left: 1.35em; }}
    li {{ margin: 0 0 10px; font-size: 16.5px; }}
    blockquote {{ margin: 24px 0; padding: 16px 18px; background: var(--accent-soft); border-left: 4px solid var(--accent-line); color: #355247; border-radius: 0 12px 12px 0; }}
    pre {{ overflow-x: auto; margin: 24px 0; padding: 14px 16px; background: #111827; color: #f3f4f6; border-radius: 14px; font-size: 13px; line-height: 1.65; }}
    figure {{ margin: 28px 0; }}
    figure img {{ max-width: 100%; display: block; margin: 0 auto; border-radius: 14px; }}
    figcaption {{ margin-top: 9px; color: #77828b; font-size: 13px; text-align: center; }}
    .type-essay p {{ margin-bottom: 17px; }}
    .type-tutorial h2 {{ background: var(--accent-soft); border-left-width: 0; border-radius: 12px; padding: 12px 14px; }}
    .type-tutorial ol {{ padding-left: 1.55em; }}
    .type-brief .article {{ padding-top: 22px; }}
    .type-brief h2 {{ margin-top: 28px; }}
    .type-brief p {{ margin-bottom: 14px; }}
    .style-bold .article-header {{ padding: 0 0 6px; }}
    .style-bold .type-badge {{ font-size: 13px; letter-spacing: 0.12em; }}
    .style-bold .summary {{ padding: 14px 16px; background: linear-gradient(135deg, var(--accent-soft) 0%, #ffffff 100%); border-radius: 14px; border: 1px solid rgba(31,122,92,0.12); }}
    .style-bold .meta {{ margin-top: 16px; }}
    .style-bold h2 {{ background: var(--accent); color: white; border-left-width: 0; border-radius: 14px; padding: 12px 16px; box-shadow: 0 10px 24px rgba(31,122,92,0.18); }}
    .style-bold h3 {{ padding-left: 10px; border-left: 3px solid rgba(31,122,92,0.35); }}
    .style-bold ul li, .style-bold ol li {{ padding: 8px 0; }}
    .style-bold blockquote {{ background: #f8f6f3; border-left-color: var(--accent); box-shadow: inset 0 0 0 1px rgba(31,122,92,0.08); }}
    .style-bold figure img {{ border: 3px solid rgba(31,122,92,0.12); }}
    .style-minimal-cn .page {{ max-width: 760px; border-radius: 0; box-shadow: none; background: #fffdfa; }}
    .style-minimal-cn .hero {{ display: none; }}
    .style-minimal-cn .article {{ padding: 32px 28px 60px; line-height: 1.92; }}
    .style-minimal-cn .article-header {{ margin-bottom: 30px; padding-bottom: 18px; border-bottom: 1px solid #ece8de; }}
    .style-minimal-cn .type-badge {{ color: #8b8578; letter-spacing: 0.06em; }}
    .style-minimal-cn .type-badge::before {{ background: #b9b1a0; }}
    .style-minimal-cn h1 {{ font-size: 34px; line-height: 1.34; letter-spacing: -0.01em; }}
    .style-minimal-cn .summary {{ font-size: 18px; color: #5f625f; padding: 0; background: none; }}
    .style-minimal-cn .meta {{ border-bottom: 0; padding-bottom: 0; margin-bottom: 0; color: #8d8a80; }}
    .style-minimal-cn h2 {{ margin-top: 38px; padding-left: 0; border-left-width: 0; font-size: 25px; position: relative; }}
    .style-minimal-cn h2::before {{ content: "—"; color: var(--accent); margin-right: 8px; }}
    .style-minimal-cn h3 {{ font-size: 19px; color: #2d3130; }}
    .style-minimal-cn p {{ font-size: 17.5px; color: #2b2f2e; }}
    .style-minimal-cn ul, .style-minimal-cn ol {{ padding-left: 1.6em; }}
    .style-minimal-cn li {{ margin-bottom: 12px; }}
    .style-minimal-cn blockquote {{ background: transparent; border-left: 3px solid #d8d1c3; border-radius: 0; padding: 8px 0 8px 16px; color: #575d59; }}
    .style-minimal-cn figure {{ margin: 32px 0; }}
    .style-minimal-cn figure img {{ border-radius: 6px; }}
    .style-minimal-cn figcaption {{ color: #8a8a85; }}
    .style-tech-editorial .page {{ background: #fbfcfe; border-radius: 24px; overflow: hidden; }}
    .style-tech-editorial .hero {{ background: linear-gradient(135deg, #13202e 0%, #203348 100%); padding: 0; }}
    .style-tech-editorial .hero-image {{ border-radius: 0; opacity: 0.92; }}
    .style-tech-editorial .article {{ padding-top: 0; }}
    .style-tech-editorial .article-header {{ margin: -42px 20px 28px; background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,0.98) 100%); border: 1px solid rgba(36,95,186,0.08); border-radius: 20px; padding: 22px 22px 18px; box-shadow: 0 18px 44px rgba(15,24,35,0.12); }}
    .style-tech-editorial .type-badge {{ color: #245fba; }}
    .style-tech-editorial .type-badge::before {{ background: #245fba; box-shadow: 0 0 0 4px rgba(36,95,186,0.12); }}
    .style-tech-editorial h1 {{ font-size: 37px; line-height: 1.16; color: #152535; }}
    .style-tech-editorial .summary {{ font-size: 17px; color: #546474; max-width: 94%; }}
    .style-tech-editorial .meta {{ color: #70808f; }}
    .style-tech-editorial h2 {{ border-left-width: 0; padding-left: 0; font-size: 24px; color: #17324e; position: relative; }}
    .style-tech-editorial h2::after {{ content: ""; display: block; width: 88px; height: 3px; margin-top: 10px; background: linear-gradient(90deg, #245fba 0%, #6ca4f2 100%); border-radius: 999px; }}
    .style-tech-editorial h3 {{ color: #21496e; }}
    .style-tech-editorial p {{ color: #273746; }}
    .style-tech-editorial strong {{ color: #10263b; }}
    .style-tech-editorial blockquote {{ background: linear-gradient(135deg, #f2f7ff 0%, #fbfdff 100%); border-left-color: #7ea8e8; color: #33506b; }}
    .style-tech-editorial code {{ background: #eef4fb; color: #1d4f83; }}
    .style-tech-editorial figure {{ margin: 30px 0; padding: 10px; background: #f5f8fb; border: 1px solid #e2eaf4; border-radius: 16px; }}
    .style-tech-editorial figure img {{ border-radius: 10px; }}
    @media (max-width: 640px) {{
      .shell {{ padding: 12px 8px 24px; }}
      .page {{ border-radius: 0; box-shadow: none; }}
      .hero {{ padding: 0; }}
      .hero-image {{ border-radius: 0; }}
      .article {{ padding: 22px 18px 40px; }}
      h1 {{ font-size: 29px; }}
      p, .summary {{ font-size: 16px; }}
      h2 {{ font-size: 22px; }}
    }}
    """
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{html.escape(title)}</title><style>{css}</style></head><body><div class=\"shell\"><div class=\"phone-hint\">WeChat draft preview</div><div class=\"page\">"
        f"{hero_html}<div class=\"article {type_class} {style_class}\"><div class=\"article-header\"><div class=\"type-badge\">{html.escape(article_type)} · {html.escape(style)}</div><h1>{html.escape(title)}</h1>"
        f"<div class=\"summary-box\"><p class=\"summary\">{html.escape(summary)}</p></div><div class=\"meta\">{author_html}<strong>{html.escape(theme)}{(' · ' + html.escape(color)) if color else ''}</strong></div></div>"
        f"{''.join(html_parts)}</div></div></div></body></html>"
    )


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    if input_path.suffix.lower() != ".md":
        raise SystemExit("Input must be a Markdown file ending with .md")

    raw = input_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(raw)
    title = resolve_title(frontmatter, body, args.title)
    summary = resolve_summary(frontmatter, body, args.summary)
    author = resolve_author(frontmatter, args.author)
    article_type = detect_article_type(body, args.article_type or frontmatter.get("article_type"))
    cleaned_body = normalize_markdown(body, title)
    inline_images = extract_markdown_images(cleaned_body)

    article_dir = input_path.parent
    slug = slugify(title)
    output_dir = Path(args.output_dir).resolve() if args.output_dir else (article_dir / ".wechat-prep" / slug).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    cover_source = resolve_cover(frontmatter, args.cover, article_dir, inline_images)
    local_cover = copy_asset_if_exists(cover_source, article_dir, output_dir)

    local_inline_images: List[str] = []
    rewritten_images: Dict[str, str] = {}
    for image in inline_images:
        local = copy_asset_if_exists(image, article_dir, output_dir)
        if local:
            local_inline_images.append(local)
            rewritten_images[image] = local

    cleaned_body = rewrite_markdown_image_paths(cleaned_body, rewritten_images, output_dir)

    theme = args.theme or frontmatter.get("wechat_theme") or "default"
    color = args.color or frontmatter.get("wechat_color") or ""
    requested_style = args.style or frontmatter.get("wechat_style") or "auto"
    style = recommend_style(article_type) if requested_style == "auto" else requested_style

    cleaned_frontmatter = {
        "title": title,
        "author": author,
        "summary": summary,
        "cover": local_cover or cover_source,
        "article_type": article_type,
        "wechat_theme": theme,
        "wechat_style": style,
    }
    if color:
        cleaned_frontmatter["wechat_color"] = color

    frontmatter_lines = ["---"]
    for key, value in cleaned_frontmatter.items():
        if value:
            frontmatter_lines.append(f"{key}: {value}")
    frontmatter_lines.append("---")
    cleaned_markdown = "\n".join(frontmatter_lines) + "\n\n" + cleaned_body

    cleaned_path = output_dir / "cleaned.md"
    cleaned_path.write_text(cleaned_markdown, encoding="utf-8")

    preview_path = output_dir / "preview.html"
    preview_path.write_text(
        build_preview_html(title, summary, article_type, cleaned_body, local_cover or cover_source, author, theme, color, output_dir, style),
        encoding="utf-8",
    )

    generated_previews = {style: str(preview_path)}
    if args.compare_styles:
        compare_dir = output_dir / "style-previews"
        if compare_dir.exists():
            shutil.rmtree(compare_dir)
        compare_dir.mkdir(parents=True, exist_ok=True)
        for preset in STYLE_PRESETS:
            variant_path = compare_dir / f"{preset}.html"
            variant_path.write_text(
                build_preview_html(
                    title,
                    summary,
                    article_type,
                    cleaned_body,
                    local_cover or cover_source,
                    author,
                    theme,
                    color,
                    output_dir,
                    preset,
                ),
                encoding="utf-8",
            )
            generated_previews[preset] = str(variant_path)

    metadata = {
        "source_markdown": str(input_path),
        "output_dir": str(output_dir),
        "cleaned_markdown": str(cleaned_path),
        "preview_html": str(preview_path),
        "style_previews": generated_previews,
        "title": title,
        "summary": summary,
        "author": author,
        "article_type": article_type,
        "theme": theme,
        "color": color,
        "style": style,
        "requested_style": requested_style,
        "cover_image": local_cover or cover_source,
        "inline_images": local_inline_images or inline_images,
        "publish_notes": [
            "Review preview.html before publishing.",
            "Confirm cover image is correct for API publishing.",
            "Use browser mode if visual paste verification is needed.",
        ],
    }
    metadata_path = output_dir / "metadata.json"
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
