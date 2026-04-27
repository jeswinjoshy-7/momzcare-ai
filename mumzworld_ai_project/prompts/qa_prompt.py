QA_PROMPT = """
Review the final reply for:
- emotional appropriateness
- native Arabic quality
- policy grounding
- uncertainty handling
- escalation need
Approve only if the message is customer-safe and operationally safe.
If quality is weak but recoverable, request one retry.
If safety is low, escalate.
"""
