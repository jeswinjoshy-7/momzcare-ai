"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

const initialState = {
  customer_message: "",
  baseline_reply: "",
};

export default function HomePage() {
  const [form, setForm] = useState(initialState);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!form.customer_message.trim()) {
      setError("Customer complaint is required.");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE}/process`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        throw new Error("Request failed.");
      }

      const payload = await response.json();
      setResult(payload);
    } catch (submitError) {
      setError("Unable to reach the backend.");
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <div className="brand-mark" aria-label="MomzCare mother and child logo">
          <svg viewBox="0 0 180 120" role="img" aria-hidden="true">
            <defs>
              <linearGradient id="brandGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#d96d8f" />
                <stop offset="100%" stopColor="#9f3d5b" />
              </linearGradient>
            </defs>
            <circle cx="74" cy="30" r="12" fill="url(#brandGradient)" opacity="0.95" />
            <circle cx="101" cy="51" r="8" fill="url(#brandGradient)" opacity="0.78" />
            <path
              d="M54 92c6-28 21-45 41-45 18 0 31 12 40 31"
              fill="none"
              stroke="url(#brandGradient)"
              strokeWidth="11"
              strokeLinecap="round"
            />
            <path
              d="M78 47c-4 19-15 30-31 38"
              fill="none"
              stroke="url(#brandGradient)"
              strokeWidth="9"
              strokeLinecap="round"
              opacity="0.9"
            />
            <path
              d="M98 60c7 7 13 16 17 27"
              fill="none"
              stroke="url(#brandGradient)"
              strokeWidth="8"
              strokeLinecap="round"
              opacity="0.72"
            />
          </svg>
          <span>MomzCare</span>
        </div>
      </section>

      <section className="workspace-grid">
        <form className="panel" onSubmit={handleSubmit}>
          <div className="panel-head">
            <span>Input</span>
          </div>

          <label className="field">
            <span>Customer complaint</span>
            <textarea
              value={form.customer_message}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  customer_message: event.target.value,
                }))
              }
              placeholder="اكتبي أو اكتب رسالة العميل هنا..."
              rows={10}
            />
          </label>

          <label className="field">
            <span>Baseline support draft</span>
            <textarea
              value={form.baseline_reply}
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  baseline_reply: event.target.value,
                }))
              }
              placeholder="Paste the current support reply..."
              rows={7}
            />
          </label>

          <button className="action-button" type="submit" disabled={isLoading}>
            {isLoading ? "Refining..." : "Refine Reply"}
          </button>

          {error ? <p className="status error">{error}</p> : null}
        </form>

        <section className="panel output-panel">
          <div className="panel-head">
            <span>Output</span>
          </div>

          {result ? (
            <>
              <div className="metric-grid">
                <Metric label="Emotion" value={result.detected_emotion} />
                <Metric label="Urgency" value={formatNumber(result.urgency_score)} />
                <Metric label="Confidence" value={formatNumber(result.confidence_score)} />
                <Metric label="Escalation" value={result.escalation_needed ? "Yes" : "No"} />
                <Metric label="Policy" value={result.policy_safe ? "Safe" : "Review"} />
                <Metric label="Intent" value={result.intent} />
              </div>

              <article className="reply-card">
                <span className="eyebrow">Final Arabic reply</span>
                <p>{result.final_reply}</p>
              </article>

              <details className="context-card">
                <summary>Retrieved context</summary>
                <div className="context-list">
                  {result.retrieved_context?.map((doc, index) => (
                    <article className="context-item" key={`${doc.source}-${index}`}>
                      <p className="context-meta">
                        {doc.source} · {doc.category} · {formatNumber(doc.score)}
                      </p>
                      <p>{doc.content}</p>
                    </article>
                  ))}
                </div>
              </details>
            </>
          ) : (
            <article className="reply-card empty">
              <p>Refined reply appears here.</p>
            </article>
          )}
        </section>
      </section>
    </main>
  );
}

function Metric({ label, value }) {
  return (
    <article className="metric-card">
      <span className="eyebrow">{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function formatNumber(value) {
  if (typeof value !== "number") {
    return value;
  }

  return value.toFixed(2);
}
