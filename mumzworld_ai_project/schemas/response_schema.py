from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class SupportedLanguage(str, Enum):
    ARABIC = "ar"
    ENGLISH = "en"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class EmotionLabel(str, Enum):
    CALM = "calm"
    FRUSTRATED = "frustrated"
    ANXIOUS = "anxious"
    ANGRY = "angry"
    SAD = "sad"
    CONFUSED = "confused"
    URGENT = "urgent"


class RetrievalDocument(BaseModel):
    source: str
    category: str
    score: float
    content: str


class EmotionIntentResult(BaseModel):
    detected_language: SupportedLanguage
    detected_emotion: EmotionLabel
    urgency_score: float = Field(ge=0.0, le=1.0)
    intent: str
    severity: Literal["low", "medium", "high", "critical"]
    uncertainty_reason: Optional[str] = None


class RewriteResult(BaseModel):
    drafted_reply: str
    rationale: str


class HumanizedReply(BaseModel):
    final_reply: str
    empathy_markers: List[str] = Field(default_factory=list)


class PolicyValidationResult(BaseModel):
    policy_safe: bool
    issues: List[str] = Field(default_factory=list)
    supported_claims: List[str] = Field(default_factory=list)
    unsupported_claims: List[str] = Field(default_factory=list)


class QAConfidenceResult(BaseModel):
    qa_score: float = Field(ge=0.0, le=1.0)
    confidence_score: float = Field(ge=0.0, le=1.0)
    escalation_needed: bool
    retry_recommended: bool
    refusal_needed: bool
    reason: str


class PipelineOutput(BaseModel):
    detected_language: SupportedLanguage
    detected_emotion: EmotionLabel
    urgency_score: float = Field(ge=0.0, le=1.0)
    intent: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    escalation_needed: bool
    policy_safe: bool
    qa_score: float = Field(ge=0.0, le=1.0)
    final_reply: str
    refusal_needed: bool = False
    retrieved_context: List[RetrievalDocument] = Field(default_factory=list)
    validation_issues: List[str] = Field(default_factory=list)
    reasoning_trace: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("final_reply")
    @classmethod
    def final_reply_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("final_reply cannot be empty")
        return value


class TestCase(BaseModel):
    case_id: str
    customer_message: str
    baseline_reply: str
    expected_language: SupportedLanguage
    expected_emotion: EmotionLabel
    expected_intent: str
    expected_policy_safe: bool
    expected_escalation: bool
    expected_refusal: bool
    notes: str


class EvalResult(BaseModel):
    case_id: str
    grammar_quality: float = Field(ge=0.0, le=1.0)
    native_arabic_quality: float = Field(ge=0.0, le=1.0)
    emotion_match: float = Field(ge=0.0, le=1.0)
    policy_correctness: float = Field(ge=0.0, le=1.0)
    confidence_handling: float = Field(ge=0.0, le=1.0)
    refusal_handling: float = Field(ge=0.0, le=1.0)
    overall_score: float = Field(ge=0.0, le=1.0)
    notes: List[str] = Field(default_factory=list)
