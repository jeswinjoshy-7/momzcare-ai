# Evaluation Report

## Assessment Framework

Each test case was evaluated across six key dimensions, with scores ranging from 0.0 to 1.0:

### 1. Grammar Quality

Measures whether the final response reads like a complete and professional customer support message rather than fragmented or incomplete text.

### 2. Native Arabic Quality

Evaluates whether the Arabic responses sound natural, fluent, and appropriate for native Arabic-speaking customers.

### 3. Emotion Match

Checks whether the system correctly identified and responded to the customer’s emotional tone, such as frustration, urgency, confusion, or anxiety.

### 4. Policy Correctness

Ensures that the system did not make unsupported promises and remained fully aligned with company policy and operational constraints.

### 5. Confidence Handling

Assesses whether the system appropriately escalated uncertain or high-risk cases instead of making assumptions.

### 6. Refusal Handling

Verifies that the system clearly avoided false certainty in unsupported scenarios by using safe responses such as requesting more information, declining guarantees, or escalating to human support.

### Overall Score

The overall score for each case was calculated as the average of these six dimensions.

---

## Performance Summary (Offline Fallback Mode)

The following results represent the system’s performance using deterministic fallback logic, which is triggered when API rate limits are reached or when no API key is available.

### Average Results

| Metric              | Score |
| ------------------- | ----: |
| Overall Score       |  0.96 |
| Policy Correctness  |  1.00 |
| Emotion Match       |  0.90 |
| Confidence Handling |  1.00 |

These results demonstrate strong reliability in policy-safe responses and escalation behavior, even without relying on the LLM-backed generation path.

---

## Detailed Test Results

A total of 20 evaluation cases were tested.

### High-Performance Cases

These cases achieved strong performance with correct refusals, escalations, and policy-safe handling.

| Case ID | Scenario                                | Score | Observation        |
| ------- | --------------------------------------- | ----: | ------------------ |
| TC01    | Urgent baby formula delay (Arabic)      |  0.97 | Handled correctly  |
| TC06    | Opened item return request (English)    |  0.97 | Correct refusal    |
| TC09    | Delivery guarantee request (Arabic)     |  0.97 | Correct refusal    |
| TC11    | Damaged item without box (English)      |  0.97 | Proper escalation  |
| TC14    | Damaged item without photos (Arabic)    |  0.97 | Proper escalation  |
| TC17    | Repeated customer frustration (English) |  0.97 | Correct escalation |

### Cases with Minor Emotional Drift

These cases remained policy-safe but showed slight mismatches in emotional tone detection.

| Case ID | Scenario                          | Score | Observation            |
| ------- | --------------------------------- | ----: | ---------------------- |
| TC05    | Refund query (Arabic)             |  0.89 | Minor emotion mismatch |
| TC07    | Wrong color received (Arabic)     |  0.89 | Minor emotion mismatch |
| TC13    | Return window exception (English) |  0.89 | Minor emotion mismatch |
| TC20    | Size exchange ambiguity (English) |  0.89 | Minor emotion mismatch |

The full evaluation log for all 20 cases is available in the evaluator output file located at `evals/evaluator.py`.

---

## Performance Analysis

## Key Strengths

### Complete Policy Safety

The system achieved 100% policy correctness across all test cases.

It never made false promises such as guaranteed refunds, delivery guarantees, or unsupported return approvals. This is the most critical achievement because maintaining customer trust and policy compliance is the primary objective of the trust layer.

### Strong Refusal and Escalation Logic

In all mandatory refusal scenarios, including cases such as opened-item returns, delivery guarantees, and out-of-policy exception requests, the system responded correctly by either:

* refusing unsupported actions,
* requesting additional information, or
* escalating the issue to a human support agent.

This demonstrates reliable confidence handling and safe decision boundaries.

### Stable Bilingual Response Handling

The system consistently switched between English and Arabic based on the customer’s input language. Arabic responses remained understandable and operationally safe throughout testing.

---

## Identified Limitations

### Emotion Detection Nuance

The most common issue observed was slight emotional misclassification.

For example, customer messages expressing confusion were sometimes interpreted as neutral or anxious. While this did not affect policy correctness, it slightly reduced customer experience quality and lowered the emotion match score in several cases.

### Limited Linguistic Richness in Arabic Fallback Responses

The deterministic Arabic fallback templates were functionally correct but more repetitive and less natural compared to responses generated through the Groq-backed LLM path.

This affects conversational quality rather than policy safety.

### Evaluator Bias Toward Surface Signals

The current evaluator gives strong weight to response length and the presence of Arabic text, which may not fully capture subtle robotic phrasing or human-like conversational quality.

As a result, some responses may score well technically while still sounding slightly templated to real users.

---

## Adversarial Case Validation

### Case TC14: Damaged Item Without Photos

This case was particularly important because it tested whether the system would incorrectly approve a refund without sufficient evidence.

The system handled this case correctly by refusing immediate approval and requesting the missing photos before proceeding.

This prevented a potential policy violation and demonstrated that the trust layer remains reliable even in higher-risk customer scenarios.

---

## Final Conclusion

The offline fallback system performed strongly, achieving an average score of 0.96 while maintaining perfect policy correctness and reliable escalation behavior.

Its strongest capability is safe decision-making under uncertainty, ensuring that unsupported promises are never made and risky cases are escalated appropriately.

The main improvement area is emotional nuance, particularly in distinguishing customer confusion, frustration, and anxiety with greater precision.

Overall, the system successfully fulfills its primary objective as a customer support trust layer: protecting policy integrity while maintaining helpful and professional customer communication.
