from __future__ import annotations

from llm import llm_client
from prompts.humanizer_prompt import HUMANIZER_PROMPT
from prompts.master_prompt import SYSTEM_GOVERNANCE
from schemas.response_schema import EmotionIntentResult, HumanizedReply, RewriteResult


class HumanizerAgent:
    def run(
        self,
        customer_message: str,
        emotion_result: EmotionIntentResult,
        rewrite_result: RewriteResult,
    ) -> HumanizedReply:
        prompt = f"{SYSTEM_GOVERNANCE}\n{HUMANIZER_PROMPT}"
        llm_result = llm_client.invoke_structured(
            system_prompt=prompt,
            user_payload={
                "customer_message": customer_message,
                "emotion_result": emotion_result.model_dump(),
                "rewrite_result": rewrite_result.model_dump(),
            },
            schema=HumanizedReply,
        )
        if llm_result:
            return llm_result

        empathy_prefix = "أقدّر تمامًا سبب انزعاجك،"
        if emotion_result.detected_emotion in {"anxious", "urgent"}:
            empathy_prefix = "أفهم قلقك جدًا، خاصة إذا كان الطلب مرتبطًا باحتياج عاجل للطفل،"
        elif emotion_result.detected_emotion == "angry":
            empathy_prefix = "من حقك تنزعج من هذا الموقف،"
        final_reply = f"{empathy_prefix} {rewrite_result.drafted_reply}"
        return HumanizedReply(
            final_reply=final_reply,
            empathy_markers=["acknowledgement", "reassurance", emotion_result.detected_emotion],
        )
