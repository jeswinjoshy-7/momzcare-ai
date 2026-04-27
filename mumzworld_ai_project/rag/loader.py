from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from config import EXAMPLES_DIR, POLICIES_DIR


@dataclass
class KnowledgeDocument:
    source: str
    category: str
    content: str


def load_knowledge_documents() -> List[KnowledgeDocument]:
    docs: List[KnowledgeDocument] = []
    for root, category in ((POLICIES_DIR, "policy"), (EXAMPLES_DIR, "example")):
        for path in sorted(Path(root).glob("*.txt")):
            docs.append(
                KnowledgeDocument(
                    source=path.name,
                    category=category,
                    content=path.read_text(encoding="utf-8"),
                )
            )
    return docs
