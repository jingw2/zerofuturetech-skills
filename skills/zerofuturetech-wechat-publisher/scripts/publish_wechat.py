#!/usr/bin/env python3

import argparse
import html
import json
import mimetypes
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from prepare_article import (
    render_inline_text,
    resolve_preview_palette,
    split_frontmatter,
)


CONFIG_RELATIVE_PATHS = (
    ".zerofuturetech-skills/zerofuturetech-wechat-publisher/EXTEND.md",
    ".baoyu-skills/baoyu-post-to-wechat/EXTEND.md",
)
ENV_RELATIVE_PATHS = (
    ".zerofuturetech-skills/.env",
    ".baoyu-skills/.env",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish a prepared WeChat article directly through the official API."
    )
    parser.add_argument("metadata", help="Path to metadata.json from prepare_article.py")
    parser.add_argument(
        "--method",
        choices=["api", "browser"],
        default="api",
        help="Publishing method. Only api is implemented in this standalone version.",
    )
    parser.add_argument("--title", help="Override article title")
    parser.add_argument("--summary", help="Override article summary")
    parser.add_argument("--author", help="Override article author")
    parser.add_argument("--source-url", help="Override content_source_url")
    parser.add_argument("--cover", help="Override cover image path")
    parser.add_argument("--dry-run", action="store_true", help="Prepare payload without sending it")
    return parser.parse_args()


def load_json(path_str: str) -> dict:
    path = Path(path_str).resolve()
    if not path.exists():
        raise SystemExit(f"Metadata file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


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


def load_env_file(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    if not path.exists():
        return data
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data


def load_settings(base_dir: Path) -> Dict[str, str]:
    settings: Dict[str, str] = {}
    search_roots = [base_dir.resolve(), Path.home()]
    for root in search_roots:
        for rel_path in CONFIG_RELATIVE_PATHS:
            path = root / rel_path
            if path.exists():
                settings.update(parse_key_value_text(path.read_text(encoding="utf-8")))
        for rel_path in ENV_RELATIVE_PATHS:
            path = root / rel_path
            if path.exists():
                for key, value in load_env_file(path).items():
                    settings.setdefault(key, value)
    for key, value in os.environ.items():
        settings[key] = value
    return settings


def resolve_frontmatter_metadata(metadata: dict) -> Tuple[Dict[str, str], str, Path]:
    cleaned_path = Path(metadata["cleaned_markdown"]).resolve()
    output_dir = Path(metadata["output_dir"]).resolve()
    raw = cleaned_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(raw)
    return frontmatter, body, output_dir


def ensure_local_path(candidate: str, output_dir: Path) -> str:
    if not candidate:
        return ""
    if re.match(r"^https?://", candidate):
        return candidate
    path = Path(candidate)
    if not path.is_absolute():
        path = (output_dir / candidate).resolve()
    return str(path)


def request_json(url: str, payload: Optional[dict] = None) -> dict:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    request = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"WeChat API HTTP error {exc.code}: {details}") from exc
    result = json.loads(body)
    if result.get("errcode") not in (None, 0):
        raise SystemExit(f"WeChat API error {result['errcode']}: {result.get('errmsg', '')}")
    return result


def upload_file(url: str, field_name: str, file_path: Path, extra_fields: Optional[Dict[str, str]] = None) -> dict:
    if not file_path.exists():
        raise SystemExit(f"File not found for upload: {file_path}")
    boundary = f"----CodexForm{uuid.uuid4().hex}"
    body = bytearray()
    if extra_fields:
        for key, value in extra_fields.items():
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"))
            body.extend(str(value).encode("utf-8"))
            body.extend(b"\r\n")
    mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        f'Content-Disposition: form-data; name="{field_name}"; filename="{file_path.name}"\r\n'.encode("utf-8")
    )
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_path.read_bytes())
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    request = urllib.request.Request(
        url,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"WeChat upload HTTP error {exc.code}: {details}") from exc
    result = json.loads(raw)
    if result.get("errcode") not in (None, 0):
        raise SystemExit(f"WeChat upload error {result['errcode']}: {result.get('errmsg', '')}")
    return result


def fetch_access_token(app_id: str, app_secret: str) -> str:
    query = urllib.parse.urlencode(
        {
            "grant_type": "client_credential",
            "appid": app_id,
            "secret": app_secret,
        }
    )
    result = request_json(f"https://api.weixin.qq.com/cgi-bin/token?{query}")
    token = result.get("access_token")
    if not token:
        raise SystemExit("WeChat access token missing from response.")
    return token


def upload_inline_image(access_token: str, image_path: Path) -> str:
    result = upload_file(
        f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}",
        "media",
        image_path,
    )
    if not result.get("url"):
        raise SystemExit("WeChat inline image upload succeeded without returning a url.")
    return result["url"]


def upload_cover_image(access_token: str, image_path: Path) -> str:
    result = upload_file(
        f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image",
        "media",
        image_path,
    )
    if not result.get("media_id"):
        raise SystemExit("WeChat cover upload succeeded without returning media_id.")
    return result["media_id"]


def style_tokens(style: str, palette: Dict[str, str], article_type: str) -> Dict[str, str]:
    base = {
        "accent": palette["accent"],
        "accent_soft": palette["accent_soft"],
        "accent_line": palette["accent_line"],
        "text": "#27303a",
        "subtle": "#6c7781",
        "h2": "margin: 34px 0 14px; font-size: 24px; line-height: 1.42; font-weight: 700;",
        "p": "margin: 0 0 16px; font-size: 16px; line-height: 1.85; color: #27303a;",
        "blockquote": "margin: 24px 0; padding: 14px 16px; background: {accent_soft}; border-left: 4px solid {accent_line}; color: #40515f;",
        "figure": "margin: 26px 0; text-align: center;",
        "img": "max-width: 100%; border-radius: 10px;",
        "caption": "margin-top: 8px; font-size: 12px; color: #7d8790;",
        "code": "display: block; margin: 22px 0; padding: 14px 16px; background: #111827; color: #f3f4f6; border-radius: 12px; font-size: 12px; line-height: 1.7; white-space: pre-wrap;",
        "ul": "margin: 0 0 18px; padding-left: 1.4em; color: #27303a;",
        "li": "margin: 0 0 10px; line-height: 1.8;",
        "h3": "margin: 24px 0 10px; font-size: 19px; line-height: 1.5; color: #22313f;",
    }
    if style == "bold":
        base["h2"] = (
            f"margin: 36px 0 14px; font-size: 22px; line-height: 1.45; font-weight: 700; "
            f"background: {base['accent']}; color: #ffffff; padding: 12px 16px; border-radius: 14px;"
        )
        base["blockquote"] = (
            f"margin: 24px 0; padding: 14px 16px; background: #f8f6f3; "
            f"border-left: 4px solid {base['accent']}; color: #40515f;"
        )
        base["img"] = "max-width: 100%; border-radius: 12px; border: 3px solid rgba(31,122,92,0.12);"
    elif style == "minimal-cn":
        base["p"] = "margin: 0 0 18px; font-size: 17px; line-height: 1.92; color: #2b2f2e;"
        base["h2"] = (
            f"margin: 38px 0 14px; font-size: 24px; line-height: 1.45; font-weight: 700; color: #22302d;"
            f" padding-left: 0;"
        )
        base["blockquote"] = (
            "margin: 24px 0; padding: 6px 0 6px 16px; background: transparent; "
            "border-left: 3px solid #d8d1c3; color: #575d59;"
        )
        base["img"] = "max-width: 100%; border-radius: 6px;"
        base["caption"] = "margin-top: 8px; font-size: 12px; color: #8a8a85;"
    elif style == "tech-editorial":
        base["h2"] = (
            f"margin: 36px 0 14px; font-size: 24px; line-height: 1.42; font-weight: 700; color: #17324e; "
            f"padding-bottom: 10px; border-bottom: 3px solid {base['accent']};"
        )
        base["blockquote"] = (
            "margin: 24px 0; padding: 14px 16px; background: linear-gradient(135deg, #f2f7ff 0%, #fbfdff 100%); "
            "border-left: 4px solid #7ea8e8; color: #33506b;"
        )
        base["figure"] = "margin: 28px 0; padding: 10px; text-align: center; background: #f5f8fb; border: 1px solid #e2eaf4; border-radius: 16px;"
        base["img"] = "max-width: 100%; border-radius: 10px;"
        base["caption"] = "margin-top: 8px; font-size: 12px; color: #70808f;"
    if article_type == "tutorial":
        base["ul"] = "margin: 0 0 18px; padding-left: 1.55em; color: #27303a;"
        base["li"] = "margin: 0 0 12px; line-height: 1.85;"
    return base


def render_article_html(
    body: str,
    output_dir: Path,
    style: str,
    article_type: str,
    theme: str,
    color: str,
    image_url_resolver: Callable[[str], str],
) -> str:
    palette = resolve_preview_palette(theme, color)
    tokens = style_tokens(style, palette, article_type)
    lines = body.splitlines()
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
            code = "\n".join(code_lines)
            html_parts.append(f'<pre style="{tokens["code"]}">{html.escape(code)}</pre>')
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
            html_parts.append(f'<h3 style="{tokens["h3"]}">{render_inline_text(line[4:].strip())}</h3>')
        elif line.startswith("## "):
            flush_list()
            html_parts.append(f'<h2 style="{tokens["h2"]}">{render_inline_text(line[3:].strip())}</h2>')
        elif line.startswith("# "):
            flush_list()
        elif line.startswith("> "):
            flush_list()
            html_parts.append(
                f'<blockquote style="{tokens["blockquote"]}"><p style="{tokens["p"]} margin: 0;">{render_inline_text(line[2:].strip())}</p></blockquote>'
            )
        elif re.match(r"^[-*]\s", line):
            if list_type != "ul":
                flush_list()
                html_parts.append(f'<ul style="{tokens["ul"]}">')
                list_type = "ul"
            html_parts.append(f'<li style="{tokens["li"]}">{render_inline_text(line[2:].strip())}</li>')
        elif re.match(r"^\d+\.\s", line):
            if list_type != "ol":
                flush_list()
                html_parts.append(f'<ol style="{tokens["ul"]}">')
                list_type = "ol"
            item = re.sub(r"^\d+\.\s*", "", line)
            html_parts.append(f'<li style="{tokens["li"]}">{render_inline_text(item)}</li>')
        elif re.match(r"!\[[^\]]*\]\(([^)]+)\)", line):
            flush_list()
            match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
            alt = match.group(1) if match else ""
            src = match.group(2) if match else ""
            if re.match(r"^https?://", src):
                image_src = src
            else:
                image_src = image_url_resolver(ensure_local_path(src, output_dir))
            caption_html = f'<figcaption style="{tokens["caption"]}">{html.escape(alt)}</figcaption>' if alt else ""
            html_parts.append(
                f'<figure style="{tokens["figure"]}"><img style="{tokens["img"]}" src="{html.escape(image_src)}" alt="{html.escape(alt)}" />{caption_html}</figure>'
            )
        else:
            flush_list()
            html_parts.append(f'<p style="{tokens["p"]}">{render_inline_text(line.strip())}</p>')

    flush_list()
    flush_code()
    return "".join(html_parts)


def build_preview_wrapper(title: str, summary: str, author: str, body_html: str) -> str:
    safe_author = html.escape(author or "Zero Future Tech")
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{html.escape(title)}</title></head><body style=\"margin:0;background:#f3f5f7;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB',sans-serif;\">"
        "<div style=\"max-width:760px;margin:0 auto;padding:24px 12px 48px;\">"
        "<div style=\"margin:0 auto 16px;max-width:680px;color:#7a848d;font-size:12px;\">WeChat publish preview</div>"
        "<div style=\"max-width:680px;margin:0 auto;background:#ffffff;padding:28px 22px 44px;border-radius:20px;box-shadow:0 18px 44px rgba(15,24,35,0.08);\">"
        f"<h1 style=\"margin:0;font-size:32px;line-height:1.28;color:#17212b;\">{html.escape(title)}</h1>"
        f"<p style=\"margin:14px 0 0;font-size:16px;line-height:1.8;color:#5b6670;\">{html.escape(summary)}</p>"
        f"<div style=\"margin:18px 0 28px;padding-bottom:14px;border-bottom:1px solid #edf1f3;font-size:13px;color:#7d8790;\">{safe_author}</div>"
        f"{body_html}</div></div></body></html>"
    )


def integer_setting(frontmatter: Dict[str, str], settings: Dict[str, str], key: str, default: int) -> int:
    value = frontmatter.get(key, settings.get(key, default))
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def resolve_source_url(frontmatter: Dict[str, str], metadata: dict, args: argparse.Namespace, settings: Dict[str, str]) -> str:
    if args.source_url:
        return args.source_url
    for key in ("content_source_url", "source_url"):
        if frontmatter.get(key):
            return frontmatter[key]
    return settings.get("content_source_url", "")


def main() -> None:
    args = parse_args()
    if args.method != "api":
        raise SystemExit("Standalone version currently supports only --method api.")

    metadata = load_json(args.metadata)
    frontmatter, body, output_dir = resolve_frontmatter_metadata(metadata)
    settings = load_settings(Path.cwd())

    title = args.title or metadata.get("title") or frontmatter.get("title") or "Untitled Article"
    summary = args.summary or metadata.get("summary") or frontmatter.get("summary") or ""
    author = args.author or metadata.get("author") or frontmatter.get("author") or settings.get("default_author", "")
    theme = metadata.get("theme") or frontmatter.get("wechat_theme") or settings.get("default_theme", "default")
    color = metadata.get("color") or frontmatter.get("wechat_color") or settings.get("default_color", "")
    style = metadata.get("style") or frontmatter.get("wechat_style") or "tech-editorial"
    article_type = metadata.get("article_type") or frontmatter.get("article_type") or "essay"
    source_url = resolve_source_url(frontmatter, metadata, args, settings)
    need_open_comment = integer_setting(frontmatter, settings, "need_open_comment", 1)
    only_fans_can_comment = integer_setting(frontmatter, settings, "only_fans_can_comment", 0)

    cover_candidate = args.cover or metadata.get("cover_image") or frontmatter.get("cover") or ""
    cover_image = ensure_local_path(cover_candidate, output_dir)
    if not cover_image or re.match(r"^https?://", cover_image):
        raise SystemExit("API publishing requires a local cover image path.")
    if not Path(cover_image).exists():
        raise SystemExit(f"Cover image not found: {cover_image}")

    publish_cache: Dict[str, str] = {}

    def resolve_image_url(image_path: str) -> str:
        cached = publish_cache.get(image_path)
        if cached:
            return cached
        if args.dry_run:
            simulated = f"https://example.invalid/wechat/{Path(image_path).name}"
            publish_cache[image_path] = simulated
            return simulated
        access_token = publish_cache["__access_token__"]
        uploaded = upload_inline_image(access_token, Path(image_path))
        publish_cache[image_path] = uploaded
        return uploaded

    if not args.dry_run:
        app_id = settings.get("WECHAT_APP_ID")
        app_secret = settings.get("WECHAT_APP_SECRET")
        if not app_id or not app_secret:
            raise SystemExit("WECHAT_APP_ID and WECHAT_APP_SECRET are required for API publishing.")
        publish_cache["__access_token__"] = fetch_access_token(app_id, app_secret)

    article_html = render_article_html(body, output_dir, style, article_type, theme, color, resolve_image_url)
    rendered_path = output_dir / "wechat-article.html"
    rendered_path.write_text(build_preview_wrapper(title, summary, author, article_html), encoding="utf-8")

    if args.dry_run:
        cover_media_id = "dry-run-cover-media-id"
    else:
        cover_media_id = upload_cover_image(publish_cache["__access_token__"], Path(cover_image))

    article_payload = {
        "title": title,
        "author": author,
        "digest": summary,
        "content": article_html,
        "content_source_url": source_url,
        "thumb_media_id": cover_media_id,
        "need_open_comment": need_open_comment,
        "only_fans_can_comment": only_fans_can_comment,
    }

    if args.dry_run:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "rendered_html": str(rendered_path),
                    "payload": {"articles": [article_payload]},
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    result = request_json(
        f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={publish_cache['__access_token__']}",
        {"articles": [article_payload]},
    )
    print(
        json.dumps(
            {
                "draft_media_id": result.get("media_id"),
                "rendered_html": str(rendered_path),
                "title": title,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
