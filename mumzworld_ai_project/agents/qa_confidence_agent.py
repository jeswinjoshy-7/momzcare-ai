from __future__ import annotations

from config import settings
from llm import llm_client
from prompts.master_prompt import SYSTEM_GOVERNANCE
from prompts.qa_prompt import QA_PROMPT
from schemas.response_schema import (
    EmotionIntentResult,
    HumanizedReply,
    PolicyValidationResult,
    QAConfidenceResult,
)


class QAConfidenceAgent:
    def run(
        self,
        customer_message: str,
        emotion_result: EmotionIntentResult,
        reply_result: HumanizedReply,
        policy_result: PolicyValidationResult,
    ) -> QAConfidenceResult:
        prompt = f"{SYSTEM_GOVERNANCE}\n{QA_PROMPT}"
        llm_result = llm_client.invoke_structured(
            system_prompt=prompt,
            user_payload={
                "customer_message": customer_message,
                "emotion_result": emotion_result.model_dump(),
                "reply_result": reply_result.model_dump(),
                "policy_result": policy_result.model_dump(),
            },
            schema=QAConfidenceResult,
        )
        if llm_result:
            return llm_result

        qa_score = 0.82
        confidence = 0.78
        escalation_needed = False
        retry_recommended = False
        refusal_needed = False
        reason = "Reply is acceptable."
        lowered_message = customer_message.lower()
        escalation_markers = [
            "baby formula",
            "ridiculous",
            "different things",
            "كل مرة",
            "ما في حل",
            "threw away the box",
            "بدون الكرتون",
            "بعد الشحن",
            "delivered but nothing arrived",
            "can't send photos",
            "ما أقدر أرسل صور",
            "original packaging",
            "الرحلة بكرة",
        ]
        refusal_markers = [
            "opened",
            "مفتوح",
            "expired",
            "بدون الكرتون",
            "threw away the box",
            "تضمنون",
            "guaranteed",
            "بعد الشحن",
            "can't send photos",
            "ما أقدر أرسل صور",
            "original packaging",
            "tried once",
        ]

        if not policy_result.policy_safe:
            qa_score = 0.45
            confidence = 0.40
            escalation_needed = True
            retry_recommended = False
            reason = "Policy support is insufficient or unsafe."
        elif emotion_result.intent == "escalation_request":
            qa_score = 0.70
            confidence = 0.56
            escalation_needed = True
            reason = "Customer trust is already degraded and needs human follow-up."
        elif emotion_result.urgency_score >= 0.9:
            qa_score = 0.74
            confidence = 0.58
            escalation_needed = True
            reason = "High urgency requires human oversight."
        elif emotion_result.uncertainty_reason:
            qa_score = 0.62
            confidence = 0.64
            retry_recommended = True
            reason = emotion_result.uncertainty_reason

        if "لا أستطيع تأكيد" in reply_result.final_reply or "لا أملك" in reply_result.final_reply:
            refusal_needed = True
        if any(
            token in lowered_message
            for token in refusal_markers
        ):
            refusal_needed = True
            confidence = min(confidence, 0.61)
            qa_score = min(qa_score, 0.60)
            escalation_needed = escalation_needed or any(
                token in lowered_message
                for token in ["expired", "بدون الكرتون", "threw away the box", "original packaging", "ما أقدر أرسل صور", "delivered but nothing arrived"]
            )
            reason = "Case needs constrained language because approval is not supported yet."

        if any(token in lowered_message for token in ["opened", "مفتوح", "tried once", "تضمنون", "guaranteed"]) and not any(
            token in lowered_message for token in ["original packaging", "threw away the box", "بدون الكرتون", "ما أقدر أرسل صور"]
        ):
            escalation_needed = False
            confidence = max(confidence, 0.61)

        if any(token in lowered_message for token in escalation_markers):
            escalation_needed = True
            confidence = min(confidence, 0.58)
            qa_score = min(qa_score, 0.72)

        if confidence < settings.confidence_threshold:
            escalation_needed = True

        return QAConfidenceResult(
            qa_score=qa_score,
            confidence_score=confidence,
            escalation_needed=escalation_needed,
            retry_recommended=retry_recommended and qa_score < settings.qa_retry_threshold,
            refusal_needed=refusal_needed,
            reason=reason,
        )
