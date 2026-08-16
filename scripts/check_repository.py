#!/usr/bin/env python3
"""Dependency-free policy checks for the tracked repository tree."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_SIZE = 5 * 1024 * 1024

BLOCKED_SUFFIXES = {
    ".7z",
    ".dbc",
    ".gz",
    ".html",
    ".pdf",
    ".ppt",
    ".pptx",
    ".rar",
    ".tar",
    ".zip",
}
BLOCKED_PARTS = {
    ".ipynb_checkpoints",
    "mlartifacts",
    "mlruns",
    "no_sync",
    "private",
}
TEXT_SUFFIXES = {
    ".cfg",
    ".csv",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".sql",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

SECRET_PATTERNS = {
    "Databricks token": re.compile(r"dapi[a-zA-Z0-9]{20,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "assigned credential": re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*"
        r"['\"]?(?!<FILL[ _-]?IN>|example|placeholder)[a-zA-Z0-9_./+\-]{16,}"
    ),
}

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def check_markdown_links(path: Path, text: str) -> list[str]:
    failures: list[str] = []
    for match in MARKDOWN_LINK.finditer(text):
        raw_target = match.group(1).strip()
        target = raw_target.split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        file_part = unquote(target.split("#", 1)[0])
        if file_part and not (path.parent / file_part).resolve().exists():
            failures.append(f"{path.relative_to(ROOT)}: broken link -> {target}")
    return failures


def main() -> int:
    failures: list[str] = []

    for path in tracked_files():
        relative = path.relative_to(ROOT)
        relative_parts = set(relative.parts)

        if path.suffix.lower() in BLOCKED_SUFFIXES:
            failures.append(f"{relative}: blocked binary/export type")
        if relative_parts & BLOCKED_PARTS:
            failures.append(f"{relative}: blocked generated/private path")
        if path.stat().st_size > MAX_FILE_SIZE:
            failures.append(f"{relative}: exceeds 5 MiB")

        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {
            ".gitattributes",
            ".gitignore",
            "LICENSE",
        }:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"{relative}: text file is not UTF-8")
            continue

        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{relative}: possible {label}")

        if relative != Path("scripts/check_repository.py"):
            if re.search(r"(?i)utm_|chatgpt\.com", text):
                failures.append(f"{relative}: tracking or generated-source URL")
            if re.search(r"(?i)taking our whole conversation|as an ai language model", text):
                failures.append(f"{relative}: conversational residue")
        if path.suffix.lower() == ".md":
            failures.extend(check_markdown_links(path, text))

    if failures:
        print("Repository quality checks failed:")
        for failure in sorted(set(failures)):
            print(f"- {failure}")
        return 1

    print("Repository quality checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
