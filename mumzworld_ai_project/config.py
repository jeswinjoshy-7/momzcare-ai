from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
POLICIES_DIR = DATA_DIR / "policies"
EXAMPLES_DIR = DATA_DIR / "examples"
TEST_CASES_PATH = DATA_DIR / "test_cases.json"
FAISS_DIR = BASE_DIR / ".faiss_index"


@dataclass(frozen=True)
class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    similarity_top_k: int = int(os.getenv("SIMILARITY_TOP_K", "4"))
    qa_retry_threshold: float = float(os.getenv("QA_RETRY_THRESHOLD", "0.65"))
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.60"))
    escalation_threshold: float = float(os.getenv("ESCALATION_THRESHOLD", "0.55"))


settings = Settings()
