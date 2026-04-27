# EVALS

## Rubric

Each case is scored on six dimensions from `0.0` to `1.0`:

- `grammar_quality`: does the final reply read like a full customer-support response rather than fragments
- `native_arabic_quality`: does the answer contain natural Arabic output when the trust layer is expected to produce Arabic
- `emotion_match`: did the system detect the expected emotional tone
- `policy_correctness`: did the system avoid unsupported promises and stay grounded
- `confidence_handling`: did it escalate when the case or confidence profile required it
- `refusal_handling`: did it explicitly avoid certainty in unsupported scenarios

`overall_score` is the mean of the six metrics.

## Test Mix

- urgent essential-item delays
- damaged product complaints
- refund disputes
- missing parts
- return eligibility ambiguity
- incomplete evidence
- repeated-frustration escalation
- one refusal-heavy unsupported case

## Before vs After

Baseline replies in `test_cases.json` intentionally include robotic or unsafe drafts like:

- `We can refund you immediately.`
- `Delivery will happen in 2 hours.`
- `Yes, guaranteed tomorrow.`

ArabicCare AI improves these by:

- removing unsupported promises
- switching to native Arabic trust-preserving phrasing
- surfacing uncertainty
- escalating when the business risk is high

## Honest Limitations

- The fallback heuristic path is deterministic and safe, but less linguistically rich than the Groq-backed path.
- The current evaluator is rubric-based rather than human-annotated, so it is better at checking policy behavior than nuanced style quality.
- Real production deployment would need live OMS and courier signals before making delivery-specific statements.

## Run

```bash
python -m evals.evaluator
```
