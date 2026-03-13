#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish a prepared WeChat article via baoyu-post-to-wechat."
    )
    parser.add_argument("metadata", help="Path to metadata.json from prepare_article.py")
    parser.add_argument(
        "--method",
        choices=["api", "browser"],
        default="api",
        help="Publishing method. Default: api",
    )
    parser.add_argument("--account", help="Optional baoyu account alias")
    parser.add_argument("--theme", help="Override theme")
    parser.add_argument("--color", help="Override color")
    parser.add_argument("--dry-run", action="store_true", help="Print command without running it")
    return parser.parse_args()


def resolve_runtime() -> List[str]:
    bun = shutil.which("bun")
    if bun:
        return [bun]
    npx = shutil.which("npx")
    if npx:
        return [npx, "-y", "bun"]
    raise SystemExit("Neither bun nor npx is available. Install bun or npm/npx first.")


def load_metadata(path_str: str) -> dict:
    path = Path(path_str).resolve()
    if not path.exists():
        raise SystemExit(f"Metadata file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    args = parse_args()
    metadata = load_metadata(args.metadata)
    baoyu_base = Path.home() / ".codex" / "skills" / "baoyu-post-to-wechat" / "scripts"
    if not baoyu_base.exists():
        raise SystemExit("baoyu-post-to-wechat is not installed in ~/.codex/skills")

    runtime = resolve_runtime()
    cleaned_markdown = metadata["cleaned_markdown"]
    title = metadata.get("title", "")
    summary = metadata.get("summary", "")
    author = metadata.get("author", "")
    cover = metadata.get("cover_image", "")
    theme = args.theme or metadata.get("theme") or "default"
    color = args.color or metadata.get("color") or ""

    if args.method == "api":
        command = runtime + [
            str(baoyu_base / "wechat-api.ts"),
            cleaned_markdown,
            "--theme",
            theme,
        ]
        if title:
            command += ["--title", title]
        if summary:
            command += ["--summary", summary]
        if author:
            command += ["--author", author]
        if cover:
            command += ["--cover", cover]
        if color:
            command += ["--color", color]
    else:
        command = runtime + [
            str(baoyu_base / "wechat-article.ts"),
            "--markdown",
            cleaned_markdown,
            "--theme",
            theme,
        ]
        if color:
            command += ["--color", color]

    if args.account:
        command += ["--account", args.account]

    if args.dry_run:
        print(json.dumps({"command": command}, ensure_ascii=False, indent=2))
        return

    result = subprocess.run(command, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
