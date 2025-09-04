# app.py
# Attractive Streamlit landing page with Bio + geometry animation + 4 example buttons.

import time
import numpy as np
import streamlit as st
import plotly.graph_objects as go

# ----------------- BASIC PAGE SETUP -----------------
st.set_page_config(page_title="Manohar Choudhary — Research", page_icon="🧭", layout="wide")

# ROUTING
if "page" not in st.session_state:
    st.session_state["page"] = "home"
def go(p): st.session_state["page"] = p

# ----------------- YOUR BIO (EDIT IF YOU LIKE) -----------------
PROFILE_IMG = "#"   # <- update later with a direct image URL
NAME = "Manohar Choudhary"
TITLE = "Research Scholar, Mathematics & Statistics"
AFFILIATION = "Dr. Harisingh Gour Vishwavidyalaya, Sagar"
EMAIL = "manoharfbg@gmail.com"
PHONE = "+91 9304561611"

SHORT_BIO = (
    "I’m a research scholar working on **geometric optimization** — with a focus on the "
    "**Heron, Fagnano, and Fermat–Torricelli problems** — and on algorithmic approaches in "
    "convex analysis. I design and prototype models in **Python/Matlab**, explore computational "
    "methods, and build interactive visualizations to make geometry come alive."
)

HIGHLIGHTS = [
    "Fellowship for Training of Young Scientists — **MP Young Scientist Congress 2025**",
    "First Rank (Poster): *Generalized Fagnano’s Problem* — **National Mathematics Day 2024**",
    "Best Oral Presentation — **ICRTMPCS 2023**",
]

INTERESTS = [
    "Geometric & Convex Optimization", "Convex Analysis",
    "Optimization Algorithms", "Machine Learning",
]

SKILLS = [
    "Python", "C/C++", "MATLAB", "Mathematica", "GeoGebra",
    "NumPy", "Matplotlib", "LaTeX"
]

# ----------------- SMALL STYLE HELPERS -----------------
def pill(text):
    return f"""<span style="
        display:inline-block;background:#EEF2FF;color:#4338CA;
        padding:6px 10px;border-radius:999px;margin:2px 6px 2px 0;
        font-size:12px;border:1px solid #C7D2FE;">{text}</span>"""

def badge(text):
    return f"""<div style="
        background:linear-gradient(90deg,#F8FAFC,#F1F5F9);
        border:1px solid #E5E7EB;border-radius:14px;padding:10px 12px;margin:6px 0;
        box-shadow:0 1px 2px rgba(0,0,0,.04);font-size:14px;">{text}</div>"""

def big_button(label, key, page):
    st.button(label, key=key, use_container_width=True, type="primary", on_click=go, args=(page,))

# ----------------- GEOMETRY ANIMATION FIGURE -----------------
def geometry_fig(t: float) -> go.Figure:
    """
    Simple geometry: a convex pentagon and a point moving on a circle.
    Draw connector from x* (moving point) to its nearest polygon vertex (for aesthetics).
    This is purely visual (no solver) — smooth and reliable on Streamlit Cloud.
    """
    # Pentagon vertices (convex, CCW-ish)
    V = np.array([[0.5, 1.0],[1.8, 0.2],[3.6, 0.8],[4.1, 2.6],[1.2, 3.4]])
    # Moving point on a circle
    r, c = 1.4, np.array([3.5, 3.6])
    x = c + r * np.array([np.cos(2*np.pi*t), np.sin(2*np.pi*t)])

    # Find nearest vertex (Euclidean)
    dists = np.linalg.norm(V - x, axis=1)
    k = int(np.argmin(dists))

    # Build figure
    fig = go.Figure()

    # Polygon (filled)
    V_closed = np.vstack([V, V[0]])
    fig.add_trace(go.Scatter(
        x=V_closed[:,0], y=V_closed[:,1], mode="lines", fill="toself",
        name="Polygon", opacity=0.18, hoverinfo="skip"
    ))

    # Vertices
    fig.add_trace(go.Scatter(
        x=V[:,0], y=V[:,1], mode="markers+text",
        text=[f"v{i+1}" for i in range(len(V))],
        textposition="top center", marker=dict(size=8),
        name="Vertices"
    ))

    # Moving point (x*)
    fig.add_trace(go.Scatter(
        x=[x[0]], y=[x[1]], mode="markers", name="x*",
        marker=dict(size=14, symbol="star")
    ))

    # Connector to nearest vertex
    fig.add_trace(go.Scatter(
        x=[x[0], V[k,0]], y=[x[1], V[k,1]], mode="lines+markers",
        name=f"Nearest: v{k+1}", marker=dict(size=6)
    ))

    fig.update_layout(
        width=None, height=420, margin=dict(l=10,r=10,t=10,b=10),
        xaxis=dict(range=[-0.5, 5.0], zeroline=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-0.2, 4.4], zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig

# ----------------- HOME (LANDING) -----------------
def home():
    # HERO
    left, right = st.columns([1, 2])
    with left:
        if PROFILE_IMG and PROFILE_IMG != "#":
            st.image(PROFILE_IMG, use_container_width=True)
        else:
            st.markdown(
                """
                <div style="
                    height:220px;border:2px dashed #E5E7EB;border-radius:16px;
                    display:flex;align-items:center;justify-content:center;color:#6B7280;">
                    Add your photo — set PROFILE_IMG="#your_link" in app.py
                </div>
                """,
                unsafe_allow_html=True
            )
    with right:
        st.markdown(f"<h1 style='margin-bottom:0'>{NAME}</h1>", unsafe_allow_html=True)
        st.markdown(f"**{TITLE}**  ·  {AFFILIATION}")
        st.markdown(
            f"<div style='font-size:16px;line-height:1.6;margin-top:8px'>{SHORT_BIO}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='margin-top:10px'>{pill('Email: ' + EMAIL)} {pill('Phone: ' + PHONE)}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # HIGHLIGHTS
    st.subheader("Highlights")
    cols = st.columns(3)
    for i, h in enumerate(HIGHLIGHTS):
        with cols[i % 3]:
            st.markdown(badge(h), unsafe_allow_html=True)

    # INTERESTS / SKILLS
    st.markdown("### Interests")
    st.markdown(" ".join(pill(x) for x in INTERESTS), unsafe_allow_html=True)
    st.markdown("### Skills")
    st.markdown(" ".join(pill(x) for x in SKILLS), unsafe_allow_html=True)

    # ANIMATION CONTROLS
    st.markdown("---")
    st.subheader("Geometry animation")
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        t = st.slider("t (0 → 1)", 0.0, 1.0, 0.25, 0.01)
    with c2:
        autoplay = st.toggle("Autoplay", value=False)
    with c3:
        delay = st.number_input("Delay (ms)", value=40, step=5, min_value=0, max_value=200)

    # Draw
    ph = st.empty()
    fig = geometry_fig(t)
    ph.plotly_chart(fig, use_container_width=True)

    # Autoplay loop
    if autoplay:
        for tt in np.linspace(0, 1, 80):
            ph.plotly_chart(geometry_fig(float(tt)), use_container_width=True)
            time.sleep(delay/1000.0)

    st.markdown("---")

    # EXAMPLE BUTTONS
    st.subheader("Examples")
    st.caption("Click a button — you can paste your Colab code into each page later.")
    cA, cB = st.columns(2)
    with cA:
        big_button("▶️ Example 1", key="ex1", page="ex1")
        big_button("▶️ Example 2", key="ex2", page="ex2")
    with cB:
        big_button("▶️ Example 3", key="ex3", page="ex3")
        big_button("▶️ Example 4", key="ex4", page="ex4")

    st.info("When you’re ready, we’ll add CVXPY + ECOS to these example pages.")

# ----------------- PLACEHOLDER PAGES -----------------
def back():
    st.button("⬅️ Back to Home", on_click=go, args=("home",), use_container_width=False)

def placeholder_example(title: str):
    st.header(title)
    back()
    st.write(
        "This is a placeholder. Paste your Colab code here. "
        "Keep plots with Plotly for a fast, interactive feel."
    )
    # Tiny demo plot (random points)
    rng = np.random.default_rng(0)
    x = rng.normal(0, 1, 150)
    y = rng.normal(0, 1, 150)
    fig = go.Figure(data=[go.Scatter(x=x, y=y, mode="markers")])
    fig.update_layout(height=420, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

def ex1(): placeholder_example("Example 1")
def ex2(): placeholder_example("Example 2")
def ex3(): placeholder_example("Example 3")
def ex4(): placeholder_example("Example 4")

# ----------------- ROUTER -----------------
page = st.session_state["page"]
if page == "home":
    home()
elif page == "ex1":
    ex1()
elif page == "ex2":
    ex2()
elif page == "ex3":
    ex3()
elif page == "ex4":
    ex4()
else:
    home()
