from __future__ import annotations

from typing import List

from llm import llm_client
from prompts.emotion_prompt import EMOTION_PROMPT
from prompts.master_prompt import SYSTEM_GOVERNANCE
from schemas.response_schema import EmotionIntentResult, RetrievalDocument
from utils import detect_language_heuristic


class EmotionIntentAgent:
    def run(self, customer_message: str, retrieved_docs: List[RetrievalDocument]) -> EmotionIntentResult:
        prompt = f"{SYSTEM_GOVERNANCE}\n{EMOTION_PROMPT}"
        llm_result = llm_client.invoke_structured(
            system_prompt=prompt,
            user_payload={
                "customer_message": customer_message,
                "retrieved_docs": [doc.model_dump() for doc in retrieved_docs],
            },
            schema=EmotionIntentResult,
        )
        if llm_result:
            return llm_result

        text = customer_message.lower()
        urgency = 0.35
        emotion = "calm"
        intent = "general_support"
        severity = "low"
        uncertainty_reason = None

        if any(token in text for token in ["ridiculous", "different things", "كل مرة", "ما في حل", "every time", "three agents"]):
            urgency = 0.82
            emotion = "angry"
            severity = "high"
            intent = "escalation_request"
            uncertainty_reason = "Repeated trust failure should be reviewed by a specialist."
        elif any(token in text for token in ["missing part", "missing parts", "ناقص قطعة", "ناقص", "missing the", "box", "بدون الكرتون"]):
            urgency = 0.62
            emotion = "confused"
            severity = "high"
            intent = "policy_clarification"
            uncertainty_reason = "Missing item or incomplete evidence requires policy review."
        elif any(token in text for token in ["baby formula", "حليب", "ضروري", "مستعجل", "خلصت الكمية"]):
            urgency = 0.9
            emotion = "urgent"
            severity = "critical"
            intent = "delivery_delay"
        elif any(token in text for token in ["حفاضات", "diaper", "processing", "late", "delay", "متأخر", "تأخر"]):
            urgency = 0.75
            emotion = "anxious"
            severity = "high"
            intent = "delivery_delay"
        elif any(token in text for token in ["damaged", "broken", "مكسور", "تالف"]):
            urgency = 0.72
            emotion = "frustrated"
            severity = "high"
            intent = "damaged_item"
            if any(token in text for token in ["ما أقدر أرسل صور", "can't send photos", "cannot send photos", "no photos"]):
                uncertainty_reason = "Damage claim needs supporting evidence before resolution."
        elif any(token in text for token in ["refund", "استرجاع", "refund my money", "money back", "فلوسي", "المبلغ", "رجوع المبلغ", "cancel"]):
            urgency = 0.65
            emotion = "confused"
            severity = "medium"
            intent = "refund_request"
            if any(token in text for token in ["different things", "ridiculous", "three agents"]):
                emotion = "angry"
                severity = "high"
        elif any(token in text for token in ["angry", "worst", "سيء", "غاضب", "مستحيل", "زعلان", "ridiculous", "كل مرة", "same الكلام", "different things"]):
            urgency = 0.8
            emotion = "angry"
            severity = "high"
            intent = "escalation_request"

        if any(token in text for token in ["delivered but nothing arrived", "says delivered but nothing arrived"]):
            urgency = 0.8
            emotion = "anxious"
            severity = "high"
            intent = "general_support"
            uncertainty_reason = "Potential delivery dispute needs specialist review."

        if any(token in text for token in ["opened", "مفتوح", "tried once", "expired", "بعد الشحن", "guaranteed", "تضمنون", "بكرة"]):
            if "original packaging" in text:
                intent = "policy_clarification"
            elif any(token in text for token in ["opened", "مفتوح", "tried once"]):
                intent = "general_support"
            elif intent != "refund_request":
                intent = "policy_clarification"
            severity = "high"
            uncertainty_reason = "Eligibility or promise requires explicit policy validation."
        if any(token in text for token in ["trip tomorrow", "الرحلة بكرة", "بكرة"]) and any(
            token in text for token in ["وصل", "wrong", "wrong color", "أزرق", "أسود", "gray", "grey", "رمادي"]
        ):
            urgency = 0.86
            emotion = "urgent"
            intent = "general_support"
            severity = "high"
            uncertainty_reason = "Travel-timing complaint with wrong item needs fast human review."
        if any(token in text for token in ["refund", "استرجاع", "فلوسي", "المبلغ", "رجوع المبلغ"]) and any(
            token in text for token in ["ridiculous", "different things", "three agents"]
        ):
            intent = "refund_request"
            emotion = "angry"
            severity = "high"
            uncertainty_reason = "Refund case has repeated trust failure and needs careful handling."

        if any(token in text for token in ["بعد الشحن", "تضمنون"]):
            if intent != "refund_request":
                intent = "policy_clarification"
            emotion = "confused"
            uncertainty_reason = "Shipment-change or delivery guarantee request needs policy validation."

        if "?" in customer_message and intent == "general_support" and not uncertainty_reason:
            emotion = "confused"
            intent = "policy_clarification"
            severity = "medium"
            uncertainty_reason = "Intent inferred from limited policy-question signal."

        return EmotionIntentResult(
            detected_language=detect_language_heuristic(customer_message),
            detected_emotion=emotion,
            urgency_score=urgency,
            intent=intent,
            severity=severity,
            uncertainty_reason=uncertainty_reason,
        )
