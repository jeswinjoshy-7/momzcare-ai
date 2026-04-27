from __future__ import annotations


APP_CSS = """
<style>
    :root {
        --bg-base: #fbf0f2;
        --bg-alt: #f8e5ea;
        --bg-blush: #f4d8df;
        --surface: rgba(255, 252, 253, 0.7);
        --surface-strong: rgba(255, 250, 252, 0.9);
        --surface-border: rgba(151, 69, 90, 0.12);
        --text-main: #3f2430;
        --text-soft: #785260;
        --accent: #c85879;
        --accent-deep: #9f3d5b;
        --accent-fade: rgba(200, 88, 121, 0.12);
        --shadow: 0 22px 60px rgba(126, 58, 81, 0.12);
        --radius-lg: 30px;
        --radius-md: 22px;
        --radius-sm: 16px;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(219, 137, 161, 0.2), transparent 28%),
            radial-gradient(circle at 85% 10%, rgba(243, 188, 202, 0.45), transparent 24%),
            linear-gradient(180deg, var(--bg-base) 0%, var(--bg-alt) 52%, var(--bg-blush) 100%);
        color: var(--text-main);
        font-family: "Avenir Next", "Helvetica Neue", "Segoe UI", sans-serif;
    }

    .block-container {
        padding-top: 2.4rem;
        padding-bottom: 2.8rem;
        max-width: 1120px;
    }

    .stApp [data-testid="stHeader"] {
        background: transparent;
    }

    .stApp [data-testid="stToolbar"] {
        right: 1rem;
    }

    .hero-shell {
        padding: 1.8rem 1.9rem;
        border-radius: var(--radius-lg);
        background: linear-gradient(180deg, rgba(255, 252, 253, 0.9), rgba(252, 243, 246, 0.84));
        border: 1px solid var(--surface-border);
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }

    .hero-shell::after {
        content: "";
        position: absolute;
        inset: auto -4rem -4rem auto;
        width: 14rem;
        height: 14rem;
        background: radial-gradient(circle, rgba(200, 88, 121, 0.14), transparent 68%);
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.42rem 0.78rem;
        border-radius: 999px;
        background: var(--accent-fade);
        color: var(--accent-deep);
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .hero-title {
        margin: 0.9rem 0 0;
        font-size: 3.25rem;
        line-height: 0.98;
        color: var(--text-main);
        letter-spacing: -0.04em;
        max-width: 12ch;
    }

    .panel {
        padding: 1.15rem;
        border-radius: var(--radius-md);
        background: var(--surface);
        border: 1px solid var(--surface-border);
        box-shadow: 0 18px 45px rgba(126, 58, 81, 0.08);
        backdrop-filter: blur(16px);
    }

    .section-title {
        margin: 0;
        color: var(--text-main);
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    .metric-row {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.8rem;
        margin-top: 1rem;
    }

    .metric-card {
        padding: 0.95rem 1rem;
        border-radius: var(--radius-sm);
        background: rgba(255, 255, 255, 0.42);
        border: 1px solid rgba(151, 69, 90, 0.08);
    }

    .metric-label {
        margin: 0 0 0.3rem;
        color: var(--text-soft);
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .metric-value {
        margin: 0;
        color: var(--text-main);
        font-size: 1.18rem;
        font-weight: 700;
    }

    .reply-card {
        padding: 1.15rem 1.2rem;
        border-radius: var(--radius-md);
        background: linear-gradient(180deg, rgba(255, 254, 255, 0.8), rgba(251, 242, 246, 0.92));
        border: 1px solid rgba(151, 69, 90, 0.1);
        box-shadow: 0 18px 48px rgba(126, 58, 81, 0.08);
    }

    .reply-label {
        margin: 0 0 0.45rem;
        color: var(--text-soft);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .reply-text {
        margin: 0;
        color: var(--text-main);
        line-height: 1.85;
        font-size: 1rem;
    }

    .empty-state {
        min-height: 10rem;
        display: flex;
        align-items: center;
    }

    .stTextArea textarea {
        border-radius: 18px;
        border: 1px solid rgba(151, 69, 90, 0.12);
        background: rgba(255, 252, 253, 0.62);
        color: var(--text-main);
        padding: 1rem 1rem 1.1rem;
        box-shadow: none;
    }

    .stTextArea textarea:focus {
        border-color: rgba(200, 88, 121, 0.44);
        box-shadow: 0 0 0 1px rgba(200, 88, 121, 0.15);
    }

    .stTextArea label p {
        color: var(--text-soft);
        font-size: 0.84rem;
        font-weight: 600;
        letter-spacing: 0.01em;
    }

    .stButton > button {
        width: 100%;
        min-height: 3.1rem;
        border: none;
        border-radius: 999px;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-deep) 100%);
        color: white;
        font-size: 0.94rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        box-shadow: 0 18px 35px rgba(159, 61, 91, 0.22);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #d36485 0%, #963754 100%);
    }

    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(200, 88, 121, 0.18);
    }

    .stExpander {
        border: 1px solid var(--surface-border);
        border-radius: var(--radius-md);
        overflow: hidden;
        background: rgba(255, 250, 252, 0.72);
    }

    .context-item {
        padding: 0.95rem 0;
        border-bottom: 1px solid rgba(151, 69, 90, 0.08);
    }

    .context-item:last-child {
        border-bottom: none;
    }

    .context-meta {
        margin: 0 0 0.4rem;
        color: var(--accent-deep);
        font-size: 0.8rem;
        font-weight: 700;
    }

    .context-copy {
        margin: 0;
        color: var(--text-soft);
        line-height: 1.65;
        font-size: 0.92rem;
    }

    @media (max-width: 900px) {
        .hero-title {
            font-size: 2.5rem;
        }

        .metric-row {
            grid-template-columns: 1fr;
        }
    }
</style>
"""
