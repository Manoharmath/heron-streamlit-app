# app.py
import streamlit as st
import numpy as np
import plotly.express as px

# --------- BASIC SETUP ---------
st.set_page_config(page_title="My Heron App", page_icon="🧭", layout="wide")

# A tiny helper to remember which screen we are on
if "page" not in st.session_state:
    st.session_state["page"] = "bio"

def go(page_name: str):
    st.session_state["page"] = page_name

# --------- BIO VIEW ---------
def bio_view():
    # <<< EDIT these for your own bio >>>
    YOUR_NAME = "Your Name"
    YOUR_TITLE = "Researcher / Student"
    YOUR_EMAIL = "you@example.com"
    YOUR_SHORT_BIO = (
        "I’m researching the Generalized Heron Problem. "
        "This app hosts interactive examples built with Streamlit. "
        "I’ll add CVXPY (ECOS) simulations soon."
    )
    YOUR_PHOTO_URL = ""  # optional: paste a direct image URL

    left, right = st.columns([1, 2])
    with left:
        if YOUR_PHOTO_URL:
            st.image(YOUR_PHOTO_URL, use_container_width=True)
        else:
            st.markdown("*(Add a photo by setting `YOUR_PHOTO_URL` in app.py)*")
    with right:
        st.title(YOUR_NAME)
        st.subheader(YOUR_TITLE)
        st.write(YOUR_SHORT_BIO)
        st.markdown(f"**Contact:** {YOUR_EMAIL}")

    st.markdown("---")
    st.subheader("Examples")
    st.caption("Click a button to open an example. (Placeholders for now—paste your Colab code later.)")

    c1, c2 = st.columns(2)
    with c1:
        st.button("▶️ Example 1", use_container_width=True, on_click=go, args=("ex1",))
        st.button("▶️ Example 2", use_container_width=True, on_click=go, args=("ex2",))
    with c2:
        st.button("▶️ Example 3", use_container_width=True, on_click=go, args=("ex3",))
        st.button("▶️ Example 4", use_container_width=True, on_click=go, args=("ex4",))

    st.info(
        "Tip: Keep this simple until deployment works. "
        "When ready, we’ll add CVXPY/ECOS and your real simulations."
    )

# --------- PLACEHOLDER EXAMPLE VIEWS ---------
def back_to_bio():
    st.button("⬅️ Back to Bio", on_click=go, args=("bio",))

def ex1_view():
    st.header("Example 1")
    back_to_bio()
    st.write("This is a placeholder. Replace with your Colab code later.")
    # Tiny interactive demo so you can see something working
    n = st.slider("How many points?", 50, 500, 200, 50)
    xs = np.random.RandomState(1).randn(n)
    ys = xs**2 + np.random.RandomState(2).randn(n) * 0.3
    fig = px.scatter(x=xs, y=ys, title="Placeholder plot")
    st.plotly_chart(fig, use_container_width=True)

def ex2_view():
    st.header("Example 2")
    back_to_bio()
    st.write("Placeholder. Paste your second example here.")
    t = np.linspace(0, 2*np.pi, 200)
    fig = px.line(x=t, y=np.sin(t), title="Sine wave (placeholder)")
    st.plotly_chart(fig, use_container_width=True)

def ex3_view():
    st.header("Example 3")
    back_to_bio()
    st.write("Placeholder. Paste your third example here.")
    t = np.linspace(0, 2*np.pi, 200)
    fig = px.line(x=t, y=np.cos(2*t), title="Cosine (placeholder)")
    st.plotly_chart(fig, use_container_width=True)

def ex4_view():
    st.header("Example 4")
    back_to_bio()
    st.write("Placeholder. Paste your fourth example here.")
    # Simple scatter
    rng = np.random.default_rng(0)
    x = rng.normal(0, 1, 150)
    y = rng.normal(0, 1, 150)
    fig = px.scatter(x=x, y=y, title="Random scatter (placeholder)")
    st.plotly_chart(fig, use_container_width=True)

# --------- ROUTER ---------
page = st.session_state["page"]
if page == "bio":
    bio_view()
elif page == "ex1":
    ex1_view()
elif page == "ex2":
    ex2_view()
elif page == "ex3":
    ex3_view()
elif page == "ex4":
    ex4_view()
else:
    bio_view()
