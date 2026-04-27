# TRADEOFFS

## Chosen

- Plain Python orchestration instead of LangGraph. The assessment rewards judgment and reliability more than framework novelty.
- Five strong agents instead of a large prompt or many tiny agents.
- Manually curated policy and Arabic example corpus instead of noisy scraping.
- Minimal Streamlit instead of a polished dashboard.
- Strong fallback heuristics so the project still demonstrates architecture without a live API key.

## Cut

- No live order-management integration
- No async queueing or persistence layer
- No human feedback capture loop
- No per-country policy branching
- No automatic Arabic grammar model in the evaluator

## Why

The goal was to maximize backend intelligence and reviewer clarity within take-home constraints. The removed features would make the project broader, but not materially stronger against the stated grading rubric.
