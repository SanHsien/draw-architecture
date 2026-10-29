#!/usr/bin/env python3
"""檢查本 fork overlay 文件之間的相對連結。

只驗 overlay 文件、docs/fork/ 與 `.cursor/rules/no-upstream-pr.mdc`。
不掃根目錄 README.md：那是上游產品契約。

    python tools/check_links.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HTML_SRC_PATTERN = re.compile(r"""(?is)<img[^>]+src=["']([^"']+)["']""")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")
SKIP_NAMES = {
    "upstream-review-report.md",
    "dependency-freshness-report.md",
}

FORK_DOCUMENTS = [
    ROOT / "FORK.md",
    ROOT / "NOTICE.md",
    ROOT / "REVIEW.md",
    ROOT / "SECURITY.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CODE_OF_CONDUCT.md",
    ROOT / "CHANGELOG.md",
    ROOT / "CHANGELOG.en.md",
    ROOT / "AGENTS.md",
    ROOT / ".cursor" / "rules" / "no-upstream-pr.mdc",
]


def iter_documents() -> list[Path]:
    documents = [path for path in FORK_DOCUMENTS if path.is_file()]
    fork_docs = ROOT / "docs" / "fork"
    if fork_docs.is_dir():
        documents.extend(sorted(fork_docs.glob("*.md")))
    return [path for path in documents if path.name not in SKIP_NAMES]


def _missing_relative(path: Path, target: str) -> str | None:
    target = target.strip().strip("<>")
    if not target or target.startswith(SKIP_PREFIXES):
        return None
    file_part = unquote(target.split("#", 1)[0])
    if not file_part:
        return None
    resolved = (path.parent / file_part).resolve()
    if not resolved.is_relative_to(ROOT):
        return f"{target} → 逃出 repo 根目錄"
    try:
        shown = resolved.relative_to(ROOT)
    except ValueError:
        shown = resolved

    current = path.parent.resolve()
    posix_path = PurePosixPath(file_part.replace("\\", "/"))
    for part in posix_path.parts:
        if part in (".", ""):
            continue
        if part == "..":
            current = current.parent
            continue
        if not current.is_dir():
            return f"{target} → 找不到 {shown}"
        try:
            entries = [entry.name for entry in current.iterdir()]
        except OSError:
            return f"{target} → 找不到 {shown}"
        if part not in entries:
            cased = [entry for entry in entries if entry.casefold() == part.casefold()]
            if cased:
                return f"{target} → 大小寫不符（磁碟真實名稱為 {cased[0]}）"
            return f"{target} → 找不到 {shown}"
        current = current / part

    return None


FENCE_PATTERN = re.compile(r"(?ms)^[ \t]*(```|~~~).*?^[ \t]*\1[^\n]*$")
TITLE_SUFFIX = re.compile(r"""\s+(?:"[^"]*"|'[^']*')\s*$""")


def check_document(path: Path) -> list[str]:
    problems: list[str] = []
    # Fenced blocks hold examples, not links; `[x](y)` in them is not a promise.
    text = FENCE_PATTERN.sub("", path.read_text(encoding="utf-8"))
    # An image is also matched by LINK_PATTERN; a separate image pattern would
    # report the same missing file twice.
    for pattern in (LINK_PATTERN, HTML_SRC_PATTERN):
        for match in pattern.finditer(text):
            target = TITLE_SUFFIX.sub("", match.group(1))
            missing = _missing_relative(path, target)
            if missing:
                problems.append(missing)
    return problems


def main() -> int:
    documents = iter_documents()
    if not documents:
        print("找不到任何 fork overlay Markdown 檔")
        return 1

    failures = 0
    for path in documents:
        problems = check_document(path)
        rel = path.relative_to(ROOT)
        if problems:
            failures += 1
            for problem in problems:
                print(f"FAIL {rel}: {problem}")
        else:
            print(f"OK   {rel}")

    print(f"\n共 {len(documents)} 份 overlay 文件，{failures} 份有缺檔。")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
