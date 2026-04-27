from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from agents.emotion_intent_agent import EmotionIntentAgent
from agents.humanizer_agent import HumanizerAgent
from agents.policy_validator import PolicyValidatorAgent
from agents.qa_confidence_agent import QAConfidenceAgent
from agents.rewrite_agent import RewriteAgent
from schemas.response_schema import PipelineOutput
from utils import normalize_text
from rag.retriever import ArabicCareRetriever


@dataclass
class PipelineRequest:
    customer_message: str
    baseline_reply: str


class ArabicCarePipeline:
    def __init__(self) -> None:
        self.retriever = ArabicCareRetriever()
        self.emotion_agent = EmotionIntentAgent()
        self.rewrite_agent = RewriteAgent()
        self.humanizer_agent = HumanizerAgent()
        self.policy_validator = PolicyValidatorAgent()
        self.qa_agent = QAConfidenceAgent()

    def run(self, request: PipelineRequest) -> PipelineOutput:
        retrieved_docs = self.retriever.retrieve(request.customer_message)
        emotion_result = self.emotion_agent.run(request.customer_message, retrieved_docs)
        rewrite_result = self.rewrite_agent.run(
            request.customer_message,
            request.baseline_reply,
            emotion_result,
            retrieved_docs,
        )
        humanized_result, policy_result, qa_result = self._evaluate_reply(
            request.customer_message,
            emotion_result,
            rewrite_result,
            retrieved_docs,
        )

        if qa_result.retry_recommended:
            retry_baseline = (
                f"{rewrite_result.drafted_reply} "
                "ركز على الوضوح، واذكر الحاجة إلى المراجعة بدل أي وعد غير مؤكد."
            )
            retry_rewrite = self.rewrite_agent.run(
                request.customer_message,
                retry_baseline,
                emotion_result,
                retrieved_docs,
            )
            humanized_result, policy_result, qa_result = self._evaluate_reply(
                request.customer_message,
                emotion_result,
                retry_rewrite,
                retrieved_docs,
            )
            rewrite_result = retry_rewrite

        final_reply = humanized_result.final_reply
        if qa_result.retry_recommended:
            final_reply = (
                "أفهم سبب استفسارك، لكن حتى أعطيك ردًا دقيقًا وآمنًا نحتاج مراجعة تفصيل إضافي في الطلب. "
                "سأراجع أولًا المعلومات الناقصة ثم أوضح لك الخطوة الصحيحة المعتمدة."
            )
        if qa_result.escalation_needed:
            final_reply = (
                f"{final_reply} "
                "سأقوم أيضًا بتصعيد الحالة إلى أحد المختصين لدينا لضمان مراجعتها بشكل أدق وعدم إعطائك أي معلومة غير مؤكدة."
            ).strip()
        if qa_result.refusal_needed and "لا أستطيع" not in final_reply:
            final_reply = (
                f"{final_reply} "
                "في هذه المرحلة لا أستطيع تأكيد إجراء نهائي قبل مراجعة البيانات الداعمة."
            ).strip()

        trace: Dict[str, object] = {
            "retrieval_count": len(retrieved_docs),
            "emotion_result": emotion_result.model_dump(),
            "rewrite_result": rewrite_result.model_dump(),
            "policy_result": policy_result.model_dump(),
            "qa_result": qa_result.model_dump(),
        }
        return PipelineOutput(
            detected_language=emotion_result.detected_language,
            detected_emotion=emotion_result.detected_emotion,
            urgency_score=emotion_result.urgency_score,
            intent=emotion_result.intent,
            confidence_score=qa_result.confidence_score,
            escalation_needed=qa_result.escalation_needed,
            policy_safe=policy_result.policy_safe,
            qa_score=qa_result.qa_score,
            final_reply=normalize_text(final_reply),
            refusal_needed=qa_result.refusal_needed,
            retrieved_context=retrieved_docs,
            validation_issues=policy_result.issues,
            reasoning_trace=trace,
        )

    def _evaluate_reply(
        self,
        customer_message: str,
        emotion_result,
        rewrite_result,
        retrieved_docs: list,
    ):
        humanized_result = self.humanizer_agent.run(
            customer_message,
            emotion_result,
            rewrite_result,
        )
        policy_result = self.policy_validator.run(humanized_result.final_reply, retrieved_docs)
        qa_result = self.qa_agent.run(
            customer_message,
            emotion_result,
            humanized_result,
            policy_result,
        )
        return humanized_result, policy_result, qa_result
