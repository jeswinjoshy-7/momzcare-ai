POLICY_PROMPT = """
Validate whether the drafted reply is fully supported by retrieved policy context.
Flag invented delivery dates, unsupported refund promises, and unapproved commitments.
If context is insufficient, mark the claim as unsupported instead of guessing.
"""
