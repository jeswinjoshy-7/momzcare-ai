

# Project Documentation

## Project Overview

### MomzCareAI





<img width="1290" height="885" alt="Screenshot From 2026-04-28 00-57-58" src="https://github.com/user-attachments/assets/dce41ed7-513d-4987-a37b-2184f6efa252" />




MomzCareAI is a multilingual trust layer designed for Mumzworld-style customer support operations. Its purpose is to improve the safety, quality, and reliability of customer support replies before they reach the customer.

Instead of functioning as a general chatbot, the system acts as an intelligent control layer between a customer complaint and the final customer-facing response.

It accepts a customer complaint along with a rough baseline support draft, retrieves relevant policy documents and approved examples, rewrites the reply into safer and more natural language, validates the response against business policy, and escalates cases when confidence is low.

The primary goal is not only better language generation, but safer decision-making in trust-sensitive support scenarios.

---

## Project Scope and Assessment Constraints

#Project Demo 


https://drive.google.com/file/d/1OV40u-Ha0kl9WlXrRXzEzy4MfZtpFyLL/view?usp=sharing -- please click  this link

This project was developed as part of a take-home technical assessment with the following explicit constraints:

* Estimated implementation time: 5 hours
* Free tools should be sufficient for strong evaluation
* Data must be generated or manually created, not scraped from retailer websites
* Multilingual support is expected where relevant
* AI tools and workflow must be documented transparently

The implementation was intentionally scoped around these constraints rather than attempting to simulate a full enterprise production system.

This submission focuses on architecture judgment, multilingual support strategy, trust-layer reliability, and operational safety.

---

## Transparency-First Approach

Transparency was treated as a core evaluation requirement.

This repository is intentionally explicit about:

* what was built within the five-hour scope
* what was intentionally excluded
* which components work fully offline
* which parts depend on optional external LLM access
* where the data originated
* how AI assistance was used
* what the evaluation results do and do not prove

This project is not presented as an internal production-ready Mumzworld platform. It is a focused take-home submission designed to demonstrate strong engineering judgment and safe system design.

---

## Submission Summary

### Core Project Highlights

* Problem chosen: improving risky customer-support replies in a trust-sensitive e-commerce environment
* Core idea: retrieval-grounded trust-layer orchestration instead of a generic chatbot
* Backend: Python pipeline exposed through FastAPI
* Frontend: separate Next.js interface
* Data source: manually written policy documents, curated Arabic examples, and self-authored test cases
* Default scoring path: works fully without a paid API key using deterministic fallback logic
* Optional enhancement: Groq-backed LLM path when API access is available

This ensures the project remains functional and evaluable even without external paid infrastructure.

---

## Why This Problem Was Chosen

Mumzworld operates in a category where poor customer support responses create immediate trust risk.

Complaints often involve:

* delayed baby essentials
* damaged strollers
* refund concerns
* urgent delivery anxiety
* missing orders
* return policy frustration

These are not simple customer service interactions—they are high-emotion situations where parents are already under stress.

In these cases, the business risk is not only translation quality. The real issue is whether the reply:

* sounds natural in Arabic when Arabic is expected
* shows the correct emotional empathy
* avoids unsupported promises
* respects refund and return policy boundaries
* escalates appropriately when uncertainty exists

Generic chatbots often fail here by sounding robotic or by hallucinating guarantees they should never make.

This project focuses specifically on solving that high-risk failure mode.

---

## What the System Does

## Input

The system accepts:

* customer complaint
* baseline support draft

The baseline draft may be incomplete, overly generic, emotionally weak, or policy-unsafe.

---

## Output

The system produces:

* refined final reply
* detected emotion
* urgency score
* confidence score
* policy-safe validation flag
* escalation decision
* retrieved supporting policy context

The goal is not full customer support automation.

The system acts as a safety and quality control layer between an initial draft and the final response sent to the customer.

---

## System Architecture

The orchestration layer is intentionally simple, transparent, and fully inspectable using plain Python.

### Processing Pipeline

### Step 1: Retrieval

Relevant policy documents and approved examples are retrieved using FAISS vector search.

---

### Step 2: Context Understanding

The system detects:

* language
* emotion
* urgency
* customer intent

---

### Step 3: Rewrite Layer

The baseline draft is rewritten into a more contextually appropriate support response.

---

### Step 4: Humanization

The wording is refined to sound more natural, empathetic, and customer-facing.

---

### Step 5: Policy Validation

The generated response is checked against retrieved policies to prevent unsupported commitments.

---

### Step 6: Confidence Assessment

The QA agent scores confidence and determines whether the case should proceed, be refined, refused, or escalated.

---

### Step 7: Final Structured Output

The system returns both:

* the final reply
* structured operational metadata for internal review

This architecture prioritizes explainability over black-box generation.

---

<img width="536" height="876" alt="Screenshot 2026-04-28 091037" src="https://github.com/user-attachments/assets/39a7d8d5-4b8c-4df6-aa5d-cca6cef602fc" />



## Why This Architecture Was Selected

## Retrieval-Augmented Generation (RAG)

Instead of allowing the language model to invent refund policies or return rules from memory, the system uses retrieval-grounded validation.

Policy sources include:

* refund policy
* return policy
* delivery policy
* escalation matrix
* approved Arabic templates
* successful Arabic support examples

This reduces hallucination risk and gives the policy validator a concrete reference point.

The objective is not just fluent replies, but policy-safe replies.

---

## Multi-Agent Separation

Rather than using one large prompt, the system separates responsibilities into specialized agents:

* Emotion and Intent Agent
* Rewrite Agent
* Humanizer Agent
* Policy Validator
* QA Confidence Agent

This makes the system easier to debug, inspect, and improve.

Failures can be isolated to specific stages rather than hidden inside one large prompt.

This also improves operational reliability.

---

## Explicit Uncertainty Handling

Uncertainty is treated as a system feature, not a failure.

If confidence is low or policy support is weak, the system should:

* avoid certainty
* request additional information
* refuse unsupported actions
* escalate to human support

Safe refusal is prioritized over confident guessing.

This is critical for customer trust.

---

## How the Project Meets Assessment Criteria

## 1. Five-Hour Scope

The implementation was intentionally scoped to fit the assessment time constraint.

### Time Breakdown

| Task                                     |      Time |
| ---------------------------------------- | --------: |
| Problem framing and architecture         | 1.0 hours |
| Backend orchestration and safety logic   | 1.4 hours |
| Retrieval corpus and test case authoring | 0.8 hours |
| Evaluation harness and scoring rubric    | 0.7 hours |
| Next.js frontend and API separation      | 0.8 hours |
| Documentation and tradeoff analysis      | 0.3 hours |

### Total Time

5.0 hours

This reflects deliberate prioritization rather than broad feature expansion.

---

## 2. Free Tools Are Sufficient

The project was intentionally designed to function without requiring a paid API key.

### Free Default Path

* FAISS retrieval
* Sentence Transformers embeddings
* deterministic fallback logic
* local FastAPI backend
* local Next.js frontend
* local evaluation harness

### Optional Enhanced Path

Groq integration is available through `langchain-groq` when a valid API key is provided.

Important note:

The LLM path is an enhancement, not a hidden dependency.

The full architecture, demo flow, and evaluation can run successfully without paid access.

This was validated through offline testing.

---

## 3. Data Was Generated, Not Scraped

No retailer websites were scraped.

All repository knowledge sources were manually authored for this project.

These include:

* synthetic policy documents
* curated Arabic support templates
* successful Arabic support examples
* multilingual test cases

The dataset is representative rather than proprietary.

It was created specifically to test:

* policy reasoning
* Arabic tone quality
* escalation decisions
* refusal handling

This keeps the project compliant with assessment expectations.

---

## 4. Multilingual Support

The system supports:

* Arabic complaints
* English complaints
* mixed Arabic-English complaints

Language detection determines the rewriting path.

The strongest focus is Arabic customer support quality because that represents the highest trust-layer value in this use case.

This should not be interpreted as full enterprise localization coverage across every support scenario.

---

## 5. AI Workflow Transparency

AI assistance was used openly and intentionally.

### AI Tools Used

* Codex / GitHub Copilot for code generation and implementation acceleration
* Gemini CLI for orchestration support, structure refinement, and documentation review

### AI-Assisted Areas

* backend scaffolding
* pipeline implementation
* prompt engineering
* Next.js UI structure
* documentation refinement

### Human-Controlled Areas

* problem framing
* architecture selection
* safety strategy
* fallback behavior
* synthetic dataset design
* evaluation rubric
* final review and tradeoff decisions

AI accelerated execution, but did not replace product judgment.

---

## Technology Stack

## Backend

* Python
* FastAPI
* LangChain
* FAISS
* Sentence Transformers
* Pydantic
* python-dotenv

---

## Frontend

* Next.js
* React

---

## Optional LLM Provider

* Llama 3 via Groq

The default configured model is `llama-3.3-70b-versatile`.

---

## Evaluation Results

The evaluation system uses a rubric-based assessment rather than human annotation.

### Latest Offline Result

| Metric                      | Score |
| --------------------------- | ----: |
| Average Overall Score       |  0.96 |
| Average Policy Correctness  |  1.00 |
| Average Emotion Match       |  0.90 |
| Average Confidence Handling |  1.00 |

### Test Set Size

20 synthetic evaluation cases

### What Is Evaluated

* grammar quality
* native Arabic quality
* emotion matching
* policy correctness
* confidence handling
* refusal handling

These scores demonstrate strong policy safety and escalation reliability.

They should not be overstated as proof of production-grade customer support performance.

---

## Honest Limitations

Several deliberate limitations remain:

* policy files are representative, not real internal Mumzworld policies
* offline fallback is safer but less expressive than the LLM-backed path
* evaluation is rubric-based rather than human-annotated
* multilingual behavior is narrower than full enterprise localization
* live order integration is not included
* persistent memory is not included
* human-in-the-loop review dashboards are not included

These are known scope boundaries rather than overlooked gaps.

---

## Final Design Philosophy

The strongest signal of this project is that it does not confuse “using an LLM” with “solving the business problem.”

The real value lies in:

* trust-layer architecture
* policy-grounded validation
* safe refusal handling
* multilingual empathy
* transparent escalation logic

The system is designed to protect customer trust, not simply generate responses.

That is the core engineering decision behind MomzCareAI.

