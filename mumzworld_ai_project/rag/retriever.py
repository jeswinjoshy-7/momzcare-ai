from __future__ import annotations

import math
from typing import List

from config import settings
from rag.loader import load_knowledge_documents
from rag.vector_store import load_or_build_vector_store
from schemas.response_schema import RetrievalDocument


class ArabicCareRetriever:
    def __init__(self) -> None:
        self.bundle = None
        self.keyword_docs = load_knowledge_documents()
        try:
            self.bundle = load_or_build_vector_store()
        except Exception:
            self.bundle = None

    def retrieve(self, query: str) -> List[RetrievalDocument]:
        if self.bundle is not None:
            results = self.bundle.store.similarity_search_with_score(
                query,
                k=settings.similarity_top_k,
            )
            return [
                RetrievalDocument(
                    source=doc.metadata.get("source", "unknown"),
                    category=doc.metadata.get("category", "unknown"),
                    score=max(0.0, 1.0 / (1.0 + float(score))),
                    content=doc.page_content,
                )
                for doc, score in results
            ]

        query_terms = {term.strip(".,!?").lower() for term in query.split() if term.strip()}
        scored_docs = []
        for doc in self.keyword_docs:
            content_terms = {term.strip(".,!?").lower() for term in doc.content.split() if term.strip()}
            overlap = len(query_terms & content_terms)
            score = overlap / max(1.0, math.sqrt(len(content_terms)))
            scored_docs.append((score, doc))

        scored_docs.sort(key=lambda item: item[0], reverse=True)
        return [
            RetrievalDocument(
                source=doc.source,
                category=doc.category,
                score=round(score, 3),
                content=doc.content,
            )
            for score, doc in scored_docs[: settings.similarity_top_k]
        ]
