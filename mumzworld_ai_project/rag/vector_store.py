from __future__ import annotations

from dataclasses import dataclass
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from config import FAISS_DIR, settings
from rag.loader import load_knowledge_documents


@dataclass
class VectorStoreBundle:
    store: FAISS
    documents: List[Document]


def build_vector_store() -> VectorStoreBundle:
    knowledge_docs = load_knowledge_documents()
    docs = [
        Document(
            page_content=doc.content,
            metadata={"source": doc.source, "category": doc.category},
        )
        for doc in knowledge_docs
    ]
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    store = FAISS.from_documents(docs, embeddings)
    FAISS_DIR.mkdir(parents=True, exist_ok=True)
    store.save_local(str(FAISS_DIR))
    return VectorStoreBundle(store=store, documents=docs)


def load_or_build_vector_store() -> VectorStoreBundle:
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    if FAISS_DIR.exists():
        store = FAISS.load_local(
            str(FAISS_DIR),
            embeddings,
            allow_dangerous_deserialization=True,
        )
        return VectorStoreBundle(store=store, documents=[])
    return build_vector_store()
