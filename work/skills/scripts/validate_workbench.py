"""Deterministic checks for a bid workbench directory."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

TAGS = (
    "[已确认]",
    "[合理拟定]",
    "[待补充]",
    "[待确认]",
    "[禁止直接使用]",
)

EXPECTED_SYMBOL_COUNTS = {"▲": 12, "●": 10, "█": 3}
CONTENT_FILES = ("30_投标文件提纲.md", "31_方案初稿", "32_服务应答表初稿.md")


def _content_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue
        if line.startswith("|") or line.startswith("---"):
            continue
        lines.append(line)
    return lines


def _check_content_tags(project_dir: Path) -> list[str]:
    errors: list[str] = []
    candidates: list[Path] = []
    for item in CONTENT_FILES:
        path = project_dir / item
        if path.is_file():
            candidates.append(path)
        elif path.is_dir():
            candidates.extend(sorted(path.rglob("*.md")))

    for path in candidates:
        for number, line in enumerate(
            _content_lines(path.read_text(encoding="utf-8")), start=1
        ):
            if not any(tag in line for tag in TAGS):
                errors.append(f"{path.name}:{number} 缺少内容标记")
    return errors


def _check_mixed_tables(project_dir: Path) -> list[str]:
    path = project_dir / "02_废标项清单.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    has_score_heading = bool(re.search(r"(?m)^#+\s*评分", text))
    has_score_table = "分值" in text or "得分" in text
    if has_score_heading or has_score_table:
        return ["02_废标项清单.md 存在废标项与评分项混表"]
    return []


def _check_symbol_counts(project_dir: Path) -> list[str]:
    paths = [project_dir / "01_要求矩阵.md", project_dir / "03_评分点清单.md"]
    text = "\n".join(
        path.read_text(encoding="utf-8") for path in paths if path.exists()
    )
    errors: list[str] = []
    for symbol, expected in EXPECTED_SYMBOL_COUNTS.items():
        match = re.search(rf"{re.escape(symbol)}\s*=\s*(\d+)", text)
        if not match:
            errors.append(f"缺少符号计数声明：{symbol} 应为 {expected}")
        elif int(match.group(1)) != expected:
            errors.append(
                f"符号计数不一致：{symbol} 声明为 {match.group(1)}，应为 {expected}"
            )
    return errors


def validate(project_dir: Path) -> dict[str, Any]:
    """Return deterministic validation errors, warnings, and simple statistics."""
    project_dir = Path(project_dir)
    errors = []
    errors.extend(_check_content_tags(project_dir))
    errors.extend(_check_mixed_tables(project_dir))
    errors.extend(_check_symbol_counts(project_dir))
    markdown_files = list(project_dir.rglob("*.md"))
    return {
        "errors": errors,
        "warnings": [],
        "stats": {
            "markdown_files": len(markdown_files),
            "content_tags": sum(
                sum(text.count(tag) for tag in TAGS)
                for path in markdown_files
                for text in [path.read_text(encoding="utf-8")]
            ),
        },
    }


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.project_dir), ensure_ascii=False, indent=2))
