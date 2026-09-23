"""Visual styling for the TravelPulse dashboard."""

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@500;700&display=swap');
        :root { --ink: #183642; --muted: #60727a; --accent: #e07a5f; --line: #dbe4e2; --paper: #fffdf9; }
        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
        h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: 0; }
        .hero { padding: 1rem 0 1.75rem; }
        .eyebrow { color: var(--accent); font-weight: 700; text-transform: uppercase; letter-spacing: .12em; font-size: .75rem; }
        .hero h1 { font-size: clamp(2.3rem, 6vw, 4.5rem); line-height: 1; margin: .35rem 0 .75rem; }
        .hero p { color: var(--muted); font-size: 1.05rem; max-width: 40rem; }
        .card { background: var(--paper); border: 1px solid var(--line); border-radius: 8px; padding: 1.15rem; min-height: 10rem; box-shadow: 0 8px 24px rgba(24,54,66,.05); }
        .card-kicker { color: var(--accent); font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; }
        .card-title { font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 700; margin: .35rem 0 .8rem; }
        .big-value { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; }
        .detail { color: var(--muted); font-size: .9rem; line-height: 1.7; }
        .flag { max-height: 48px; max-width: 80px; object-fit: contain; margin-bottom: .5rem; }
        @media (max-width: 800px) {
            .hero { padding-bottom: 1rem; }
            .hero h1 { font-size: 2.5rem; }
            .card { min-height: auto; margin-bottom: .75rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )