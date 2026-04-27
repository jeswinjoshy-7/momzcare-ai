from __future__ import annotations

from typing import List

from llm import llm_client
from prompts.master_prompt import SYSTEM_GOVERNANCE
from prompts.policy_prompt import POLICY_PROMPT
from schemas.response_schema import PolicyValidationResult, RetrievalDocument


class PolicyValidatorAgent:
    UNSUPPORTED_PATTERNS = [
        "refund will be processed today",
        "100% refund guaranteed",
        "سنرجع المبلغ اليوم",
        "نضمن لك التوصيل اليوم",
        "replacement is approved",
    ]

    def run(self, drafted_reply: str, retrieved_docs: List[RetrievalDocument]) -> PolicyValidationResult:
        prompt = f"{SYSTEM_GOVERNANCE}\n{POLICY_PROMPT}"
        llm_result = llm_client.invoke_structured(
            system_prompt=prompt,
            user_payload={
                "drafted_reply": drafted_reply,
                "retrieved_docs": [doc.model_dump() for doc in retrieved_docs],
            },
            schema=PolicyValidationResult,
        )
        if llm_result:
            return llm_result

        issues: List[str] = []
        unsupported_claims: List[str] = []
        lowered = drafted_reply.lower()
        for pattern in self.UNSUPPORTED_PATTERNS:
            if pattern in lowered:
                issues.append(f"Unsupported commitment detected: {pattern}")
                unsupported_claims.append(pattern)

        policy_safe = not issues and bool(retrieved_docs)
        if not retrieved_docs:
            issues.append("No retrieved policy context available.")
            policy_safe = False

        supported_claims = [
            "Reply references policy review instead of promising unsupported outcomes."
        ]
        return PolicyValidationResult(
            policy_safe=policy_safe,
            issues=issues,
            supported_claims=supported_claims,
            unsupported_claims=unsupported_claims,
        )
