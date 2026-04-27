from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable, List


ARABIC_PATTERN = re.compile(r"[\u0600-\u06FF]")


def contains_arabic(text: str) -> bool:
    return bool(ARABIC_PATTERN.search(text))


def detect_language_heuristic(text: str) -> str:
    has_arabic = contains_arabic(text)
    has_latin = bool(re.search(r"[A-Za-z]", text))
    if has_arabic and has_latin:
        return "mixed"
    if has_arabic:
        return "ar"
    if has_latin:
        return "en"
    return "unknown"


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def read_text_files(paths: Iterable[Path]) -> List[str]:
    return [path.read_text(encoding="utf-8") for path in paths]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
