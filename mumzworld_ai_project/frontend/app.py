from __future__ import annotations

import streamlit as st

from frontend.styles import APP_CSS
from pipeline import ArabicCarePipeline, PipelineRequest


def render_app() -> None:
    st.set_page_config(page_title="ArabicCare AI", page_icon="◌", layout="wide")
    st.markdown(APP_CSS, unsafe_allow_html=True)

    _render_hero()
    _render_workspace()


def _render_hero() -> None:
    st.markdown(
        """
        <section class="hero-shell">
            <span class="hero-badge">MomsCare</span>
            <h1 class="hero-title">Refined support replies.</h1>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_workspace() -> None:
    input_col, output_col = st.columns([1.05, 0.95], gap="large")

    with input_col:
        st.markdown(
            """
            <section class="panel">
                <h2 class="section-title">Input</h2>
            </section>
            """,
            unsafe_allow_html=True,
        )

        customer_message = st.text_area(
            "Customer complaint",
            height=220,
            placeholder="اكتبي أو اكتب رسالة العميل هنا...",
        )
        baseline_reply = st.text_area(
            "Baseline support draft",
            height=160,
            placeholder="Paste the current support reply or a rough draft...",
        )
        submitted = st.button("Refine Reply", type="primary")

    result = None
    if submitted:
        if not customer_message.strip():
            st.error("Customer complaint is required.")
        else:
            pipeline = ArabicCarePipeline()
            result = pipeline.run(
                PipelineRequest(
                    customer_message=customer_message,
                    baseline_reply=baseline_reply or "We are checking your request.",
                )
            )

    with output_col:
        st.markdown(
            """
            <section class="panel">
                <h2 class="section-title">Output</h2>
            </section>
            """,
            unsafe_allow_html=True,
        )

        if result is None:
            st.markdown(
                """
                <section class="reply-card empty-state">
                    <p class="reply-text">Refined reply appears here.</p>
                </section>
                """,
                unsafe_allow_html=True,
            )
            return

        _render_metrics(result)
        _render_final_reply(result.final_reply)
        _render_context(result)


def _render_metrics(result) -> None:
    escalation = "Yes" if result.escalation_needed else "No"
    policy_safe = "Safe" if result.policy_safe else "Review"

    st.markdown(
        f"""
        <div class="metric-row">
            <section class="metric-card">
                <p class="metric-label">Emotion</p>
                <p class="metric-value">{result.detected_emotion}</p>
            </section>
            <section class="metric-card">
                <p class="metric-label">Urgency</p>
                <p class="metric-value">{result.urgency_score:.2f}</p>
            </section>
            <section class="metric-card">
                <p class="metric-label">Confidence</p>
                <p class="metric-value">{result.confidence_score:.2f}</p>
            </section>
            <section class="metric-card">
                <p class="metric-label">Escalation</p>
                <p class="metric-value">{escalation}</p>
            </section>
            <section class="metric-card">
                <p class="metric-label">Policy</p>
                <p class="metric-value">{policy_safe}</p>
            </section>
            <section class="metric-card">
                <p class="metric-label">Intent</p>
                <p class="metric-value">{result.intent}</p>
            </section>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_final_reply(final_reply: str) -> None:
    st.markdown(
        f"""
        <section class="reply-card" style="margin-top: 1rem;">
            <p class="reply-label">Final Arabic reply</p>
            <p class="reply-text">{final_reply}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_context(result) -> None:
    with st.expander("Retrieved context", expanded=False):
        for doc in result.retrieved_context:
            st.markdown(
                f"""
                <section class="context-item">
                    <p class="context-meta">{doc.source} • {doc.category} • score {doc.score:.2f}</p>
                    <p class="context-copy">{doc.content}</p>
                </section>
                """,
                unsafe_allow_html=True,
            )
