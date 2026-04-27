from __future__ import annotations

from statistics import mean
from typing import Dict, List, Tuple

from config import TEST_CASES_PATH
from pipeline import ArabicCarePipeline, PipelineRequest
from schemas.response_schema import EvalResult, PipelineOutput, TestCase
from utils import contains_arabic, load_json


def score_case(test_case: TestCase, output: PipelineOutput) -> EvalResult:
    notes: List[str] = []

    grammar_quality = 0.85 if len(output.final_reply.split()) > 12 else 0.60
    native_arabic_quality = 1.0 if contains_arabic(output.final_reply) else 0.25
    emotion_match = 1.0 if output.detected_emotion == test_case.expected_emotion else 0.5
    policy_correctness = 1.0 if output.policy_safe == test_case.expected_policy_safe else 0.3

    confidence_signal_ok = output.escalation_needed == test_case.expected_escalation
    if test_case.expected_refusal:
        refusal_ok = output.refusal_needed or "لا أستطيع" in output.final_reply or "غير مؤكد" in output.final_reply
    else:
        refusal_ok = not output.refusal_needed

    confidence_handling = 1.0 if confidence_signal_ok else 0.4
    refusal_handling = 1.0 if refusal_ok else 0.2

    if not confidence_signal_ok:
        notes.append("Escalation behavior did not match expectation.")
    if not refusal_ok:
        notes.append("Refusal or uncertainty handling was insufficient.")
    if output.intent != test_case.expected_intent:
        notes.append(f"Intent drift: expected {test_case.expected_intent}, got {output.intent}.")
    if output.detected_language != test_case.expected_language:
        notes.append(f"Language detection drift: expected {test_case.expected_language}, got {output.detected_language}.")

    overall = mean(
        [
            grammar_quality,
            native_arabic_quality,
            emotion_match,
            policy_correctness,
            confidence_handling,
            refusal_handling,
        ]
    )
    return EvalResult(
        case_id=test_case.case_id,
        grammar_quality=grammar_quality,
        native_arabic_quality=native_arabic_quality,
        emotion_match=emotion_match,
        policy_correctness=policy_correctness,
        confidence_handling=confidence_handling,
        refusal_handling=refusal_handling,
        overall_score=overall,
        notes=notes,
    )


def run_evaluation() -> Tuple[List[EvalResult], Dict[str, float]]:
    raw_cases = load_json(TEST_CASES_PATH)
    test_cases = [TestCase.model_validate(case) for case in raw_cases]
    pipeline = ArabicCarePipeline()
    results: List[EvalResult] = []

    for case in test_cases:
        output = pipeline.run(
            PipelineRequest(
                customer_message=case.customer_message,
                baseline_reply=case.baseline_reply,
            )
        )
        results.append(score_case(case, output))

    summary = {
        "average_overall_score": mean(result.overall_score for result in results),
        "average_policy_correctness": mean(result.policy_correctness for result in results),
        "average_emotion_match": mean(result.emotion_match for result in results),
        "average_confidence_handling": mean(result.confidence_handling for result in results),
    }
    return results, summary


if __name__ == "__main__":
    detailed_results, summary_metrics = run_evaluation()
    print("ArabicCare AI Evaluation Summary")
    for key, value in summary_metrics.items():
        print(f"{key}: {value:.2f}")
    print()
    for result in detailed_results:
        print(f"{result.case_id}: overall={result.overall_score:.2f} notes={'; '.join(result.notes) or 'OK'}")
