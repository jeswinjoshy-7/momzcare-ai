# MomzCare





<img width="1290" height="885" alt="Screenshot From 2026-04-28 00-57-58" src="https://github.com/user-attachments/assets/dce41ed7-513d-4987-a37b-2184f6efa252" />


MomzCareAI is a multilingual trust layer for Mumzworld-style customer support. It takes a customer complaint plus a rough support draft, retrieves relevant policy/examples, rewrites the reply into safer and more natural customer-facing language, validates the reply against policy, and escalates when confidence is low.

This project was built for a take-home assessment with these explicit constraints:

- Estimated effort: `5 hours`
- Free tools should be enough to score well
- Data must be brought or generated, not scraped from retailer sites
- Multilingual output is expected where relevant
- AI tooling and workflow must be documented transparently

This README is written to address those criteria directly.

## Transparency First

Because transparency is part of the grading criteria, this repository is intentionally explicit about:

- what was built within the `5 hour` scope and what was intentionally left out
- which parts work fully offline and which parts depend on an optional external LLM
- where the data came from
- where AI assistance was used
- what the current evaluation does and does not prove

This is not presented as a production-ready Mumzworld internal system. It is a scoped take-home submission that demonstrates product judgment, architecture choices, multilingual support thinking, and safety-oriented orchestration.

## Submission Summary

- Problem chosen: improve risky customer-support replies in a trust-sensitive e-commerce setting
- Core idea: a retrieval-grounded, multi-step orchestration layer rather than a generic chatbot
- Backend: Python pipeline exposed through FastAPI
- Frontend: separate Next.js UI
- Data source: manually written policy text, manually curated Arabic examples, and self-authored test cases
- Default scoring path: works without a paid API key by using deterministic fallback logic
- Optional enhancement: Groq-backed LLM path when `GROQ_API_KEY` is available

## Why This Problem

Mumzworld operates in a category where bad support language is costly. Many complaints involve baby essentials, damaged products, refund anxiety, or delivery stress. In these cases, the issue is not just translation accuracy. The real business risk is whether the reply:

- sounds natural in Arabic when Arabic is expected
- shows the right level of empathy
- avoids promises that policy does not support
- escalates when trust risk is high

Low-quality replies can create false promises, robotic tone, and avoidable escalations. This project focuses on that narrow but high-leverage failure mode.

## What The System Does

Input:

- customer complaint
- baseline support draft

Output:

- refined final reply
- detected emotion
- urgency score
- confidence score
- policy-safe flag
- escalation decision
- retrieved supporting context

The system is not trying to answer every support question end-to-end. It is acting as a control layer between a baseline draft and the final customer-facing message.

## Architecture

The orchestration is intentionally plain Python and inspectable.

Pipeline:

1. Retrieve relevant policy and example documents with FAISS
2. Detect language, emotion, urgency, and intent
3. Rewrite the baseline draft into a more appropriate reply
4. Humanize the wording
5. Validate the reply against retrieved policy
6. Score confidence and decide retry, refusal, or escalation
7. Return final reply plus structured assessment fields

Main implementation files:

- [pipeline.py](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/pipeline.py:1)
- [api.py](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/api.py:1)
- [agents/emotion_intent_agent.py](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/agents/emotion_intent_agent.py:1)
- [agents/rewrite_agent.py](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/agents/rewrite_agent.py:1)
- [agents/humanizer_agent.py](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/agents/humanizer_agent.py:1)
- [agents/policy_validator.py](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/agents/policy_validator.py:1)
- [agents/qa_confidence_agent.py](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/agents/qa_confidence_agent.py:1)

## Why This Architecture

### Retrieval

RAG is used to ground the reply in local documents rather than ask the model to improvise policy:

- refund policy
- return policy
- delivery policy
- escalation matrix
- approved Arabic templates
- successful Arabic support examples

This reduces hallucinated commitments and gives the validator something concrete to check against.

### Multi-step agent separation

Instead of one large prompt, the system separates concerns:

- emotion and urgency detection
- rewriting
- tone refinement
- policy validation
- confidence and escalation logic

That separation makes the system easier to inspect and makes failures easier to localize.

### Explicit uncertainty handling

The project treats uncertainty as a feature, not a bug. If confidence is low or the claim is unsupported, the system should avoid certainty, ask for review, or escalate.

## How This Meets The Selection Criteria

### 1. Estimated effort: 5 hours

The implementation was scoped to fit a short take-home, not a broad production build.

Time log:

- `1.0h` problem framing, architecture, and repo structure
- `1.4h` backend orchestration and safety logic
- `0.8h` retrieval corpus and test-case authoring
- `0.7h` evaluation harness and scoring rubric
- `0.8h` separate Next.js frontend and API split
- `0.3h` documentation and tradeoffs

Total: `5.0h`

### 2. Free tools are enough to score well

This project is intentionally usable without a paid API key.

Free/default path:

- FAISS for retrieval
- sentence-transformers embeddings
- deterministic fallback logic in each agent when no LLM is configured
- local evaluation harness
- local FastAPI backend
- local Next.js frontend

Optional paid/enhanced path:

- Groq via `langchain-groq` when `GROQ_API_KEY` is set

Important transparency note:

- The code supports an LLM-enhanced path, but the project is designed so that the core architecture, demo flow, and evaluation can still run without paying for API access.
- In this environment, the offline evaluation succeeded after clearing `GROQ_API_KEY`, which confirms the no-paid-key path is real rather than theoretical.
- If `GROQ_API_KEY` is present in the environment but network access is blocked, the evaluator may still attempt the remote Groq path first and fail. For a reproducible offline run, use `GROQ_API_KEY= python -m evals.evaluator`.

### 3. Bring or generate your own data

No retailer sites were scraped.

All repository knowledge sources are local and authored for this project:

- [data/policies/refund_policy.txt](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/data/policies/refund_policy.txt:1)
- [data/policies/return_policy.txt](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/data/policies/return_policy.txt:1)
- [data/policies/delivery_policy.txt](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/data/policies/delivery_policy.txt:1)
- [data/policies/escalation_matrix.txt](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/data/policies/escalation_matrix.txt:1)
- [data/examples/approved_arabic_templates.txt](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/data/examples/approved_arabic_templates.txt:1)
- [data/examples/successful_arabic_support_examples.txt](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/data/examples/successful_arabic_support_examples.txt:1)
- [data/test_cases.json](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/data/test_cases.json:1)

Data design choices:

- policy files are concise and synthetic, meant to simulate approved business rules
- Arabic examples are curated to guide tone and phrasing
- test cases cover Arabic, English, and mixed-language complaints
- unsafe baseline drafts are intentionally included so the system has something meaningful to correct

Transparency note on data:

- the dataset is synthetic and representative, not proprietary operational data
- the policy files are not claimed to be real Mumzworld internal documents
- the examples are designed to test reasoning, tone, and safety behavior within take-home scope

### 4. Multilingual output where relevant

The system is designed to support:

- Arabic complaints
- English complaints
- mixed Arabic-English complaints

The pipeline detects language and routes rewriting accordingly. The evaluation set currently includes:

- Arabic cases
- English cases
- mixed-language cases

See [data/test_cases.json](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/data/test_cases.json:1) for examples such as:

- Arabic urgent essential-item complaints
- English damaged-item complaints
- mixed-language wrong-item urgent complaints

Practical note:

- The project is strongest when transforming support communication into high-quality Arabic or Arabic-aware support tone.
- It still accepts English and mixed input, but the trust-layer focus is especially centered on Arabic customer support quality.
- This should not be interpreted as full production-grade parity across every bilingual support scenario.

### 5. AI tools and workflow transparency

AI assistance was used in this project. The intent here is to be explicit, not vague.

AI-assisted work:

- early code scaffolding
- prompt drafting
- initial UI iteration
- some documentation phrasing

Human-authored/reviewed work:

- problem framing and scope choice
- architecture decomposition
- safety rules and fallback strategy
- synthetic policy/data design
- evaluation rubric design
- final repo shaping and tradeoff decisions

What AI did not replace:

- judgment about what to build in 5 hours
- the decision to optimize for trust-layer reliability over chatbot breadth
- the choice to support a no-paid-key path
- the decision to keep the system inspectable rather than framework-heavy

### Concrete AI workflow used in this submission

1. Problem framing was chosen manually.
   The decision to focus on Arabic support trust, not general support automation, was a human product decision.

2. Initial implementation was accelerated with AI assistance.
   AI was used to speed up routine engineering tasks such as scaffolding modules, drafting prompts, and iterating on UI structure.

3. Safety behavior was then reviewed and tightened manually.
   Fallback logic, escalation behavior, refusal behavior, repository structure, and evaluation framing were not accepted blindly.

4. Synthetic data was authored for the task.
   Policy text, Arabic examples, and test cases were created specifically for this submission and kept local to the repository.

5. Documentation was rewritten for accuracy.
   The final README and run instructions were edited to match the current FastAPI + Next.js architecture and the real offline behavior.

### Interview-safe transparency summary

If asked directly how AI was used, the accurate short answer is:

“AI was used as an accelerator for coding, prompt drafting, and documentation iteration. The problem framing, scope choice, architecture, synthetic dataset design, safety behavior, and final review were still actively directed and checked by me.”

## Current Stack

Backend:

- Python
- FastAPI
- LangChain
- FAISS
- sentence-transformers
- Pydantic
- python-dotenv

Frontend:

- Next.js
- React

Optional LLM provider:

- Groq with `llama-3.3-70b-versatile` by default when configured

## Repository Layout

```text
.
├── agents/             # Specialized pipeline steps
├── data/               # Policies, Arabic examples, test cases
├── evals/              # Evaluation harness
├── prompts/            # Agent prompts and governance prompt
├── rag/                # Retrieval loading and vector store logic
├── schemas/            # Pydantic request/response schemas
├── web/                # Separate Next.js frontend
├── api.py              # FastAPI entrypoint
├── pipeline.py         # Main orchestration
├── EVALS.md            # Evaluation rubric
└── TRADEOFFS.md        # Deliberate scope cuts
```

## Running The Project

### Backend

```bash
cd mumzworld_ai_project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

Backend URL:

- `http://127.0.0.1:8000`

Health check:

- `GET /health`

Main endpoint:

- `POST /process`

Example request:

```json
{
  "customer_message": "طلبي متأخر وفيه حليب أطفال، أحتاجه اليوم.",
  "baseline_reply": "Your order may arrive soon. Please wait."
}
```

### Frontend

In a separate terminal:

```bash
cd mumzworld_ai_project/web
npm install
npm run dev
```

Frontend URL:

- `http://127.0.0.1:3000`

Optional frontend env file:

```bash
cp .env.local.example .env.local
```

Default value:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### Optional Groq setup

If you want to enable the LLM-backed path:

```bash
cp .env.example .env
```

Then set:

```bash
GROQ_API_KEY=...
```

If `GROQ_API_KEY` is absent, the system falls back to deterministic local logic.

## Evaluation

Run:

```bash
GROQ_API_KEY= python -m evals.evaluator
```

Why the command clears `GROQ_API_KEY`:

- it forces the offline fallback path
- it makes the run reproducible without external network access
- it demonstrates the project can be evaluated without a paid API

Latest offline result in this environment:

- `average_overall_score: 0.96`
- `average_policy_correctness: 1.00`
- `average_emotion_match: 0.90`
- `average_confidence_handling: 1.00`

Test set size:

- `20` synthetic cases in [data/test_cases.json](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/data/test_cases.json:1)

What the eval is checking:

- grammar quality
- native Arabic quality
- emotion matching
- policy correctness
- confidence handling
- refusal handling

More detail:

- [EVALS.md](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/EVALS.md:1)

Important evaluation caveat:

- these scores come from the project’s own rubric-based evaluator, not from human annotators or live customer outcomes
- they are useful for demonstrating policy-safety behavior and fallback quality
- they should not be overstated as proof of production-ready support quality

## Design Decisions

Chosen deliberately:

- plain Python orchestration instead of a heavier agent framework
- retrieval plus structured validation instead of a free-form chatbot
- strong fallback behavior instead of API-only dependency
- self-authored corpus instead of scraped data
- separate web frontend rather than a notebook/demo-only interface

Not implemented in this take-home scope:

- live order-management integration
- country-specific policy branching
- persistent case storage
- human feedback loop
- real courier or payment-status signals

More detail:

- [TRADEOFFS.md](/home/jeswin/Downloads/momzproject/mumzworld_ai_project/TRADEOFFS.md:1)

## Honest Limitations

- The synthetic policies are representative, not real Mumzworld internal rules.
- The offline fallback path is safer and more deterministic, but less expressive than the Groq-backed path.
- The evaluation rubric is useful for behavior checks, but it is still rubric-based rather than human-annotated.
- The multilingual behavior is intentionally narrower than a full production localization system.
- The old Streamlit prototype files still exist in `frontend/`, but the active UI is the separate Next.js app in `web/`.

## Reviewer Notes

The most important factual claims in this repository are:

- no retailer sites were scraped
- the corpus and test set were generated for this take-home
- the project can be run and evaluated without a paid API key
- the optional Groq path is an enhancement, not a hidden dependency
- AI assistance was used, and that usage is being stated explicitly rather than hidden
- the system is intentionally scoped for a take-home, not overstated as production-complete

## Why This Is A Strong Selection Submission

This project is aligned with the likely intent of the assessment:

- it solves a concrete and relevant support problem
- it is opinionated rather than generic
- it demonstrates architecture judgment under time constraint
- it works without requiring paid access
- it uses self-generated data responsibly
- it handles Arabic and multilingual support context
- it documents AI assistance transparently
- it includes evaluation, tradeoffs, and limitations instead of only a polished demo

If I were reviewing this submission, the strongest signal would be that it does not confuse “uses an LLM” with “solves the business problem.” The core submission is the trust-layer design, not the UI or the model brand.
