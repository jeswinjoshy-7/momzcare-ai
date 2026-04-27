from __future__ import annotations

from typing import List

from llm import llm_client
from prompts.master_prompt import SYSTEM_GOVERNANCE
from prompts.rewrite_prompt import REWRITE_PROMPT
from schemas.response_schema import EmotionIntentResult, RetrievalDocument, RewriteResult
from utils import contains_arabic


class RewriteAgent:
    def run(
        self,
        customer_message: str,
        baseline_reply: str,
        emotion_result: EmotionIntentResult,
        retrieved_docs: List[RetrievalDocument],
    ) -> RewriteResult:
        prompt = f"{SYSTEM_GOVERNANCE}\n{REWRITE_PROMPT}"
        llm_result = llm_client.invoke_structured(
            system_prompt=prompt,
            user_payload={
                "customer_message": customer_message,
                "baseline_reply": baseline_reply,
                "emotion_result": emotion_result.model_dump(),
                "retrieved_docs": [doc.model_dump() for doc in retrieved_docs],
            },
            schema=RewriteResult,
        )
        if llm_result:
            return llm_result

        policy_lines = self._extract_grounding_lines(retrieved_docs)
        drafted_reply = (
            "نفهم انزعاجك، ونراجع حالتك الآن وفق السياسات المتاحة لدينا. "
            "سنشاركك بالخطوة الصحيحة بعد التأكد من تفاصيل الطلب."
        )
        if emotion_result.intent == "delivery_delay":
            drafted_reply = (
                "أتفهم قلقك بخصوص الطلب، خصوصًا إذا كان مرتبطًا باحتياج مهم للطفل. "
                "سأوضح لك ما نستطيع تأكيده الآن حسب حالة الطلب والسياسات المتاحة، "
                "ومن ثم نحدد الخطوة الصحيحة بدون أي وعود غير مؤكدة."
            )
        elif emotion_result.intent == "damaged_item":
            drafted_reply = (
                "أعتذر عن وصول المنتج بهذه الحالة. "
                "سنراجع تفاصيل الضرر وصور المنتج إن توفرت، ثم نوجهك للإجراء المعتمد حسب السياسة."
            )
        elif emotion_result.intent == "refund_request":
            drafted_reply = (
                "أفهم رغبتك في استرجاع المبلغ. "
                "قبل تأكيد ذلك، نحتاج مطابقة حالة الطلب مع سياسة الإرجاع أو الاسترداد المعتمدة."
            )
        return RewriteResult(
            drafted_reply=f"{drafted_reply} {' '.join(policy_lines)}".strip(),
            rationale="Fallback rewrite grounded in retrieved policy snippets.",
        )

    def _extract_grounding_lines(self, retrieved_docs: List[RetrievalDocument]) -> List[str]:
        snippets: List[str] = []
        sorted_docs = sorted(retrieved_docs, key=lambda doc: (doc.category != "policy", -doc.score))
        for doc in sorted_docs:
            for line in doc.content.splitlines():
                cleaned = line.strip(" -0123456789.").strip()
                if not cleaned:
                    continue
                if cleaned.lower().startswith(("refund policy", "return policy", "delivery policy", "escalation matrix", "approved arabic", "successful arabic", "example")):
                    continue
                if cleaned.startswith(("العميل:", "الرد الجيد:")):
                    continue
                if contains_arabic(cleaned):
                    snippets.append(cleaned)
                    break
            if len(snippets) >= 2:
                break
        return snippets
