
import time
from typing import Dict, Any, List, Tuple

import numpy as np
import streamlit as st

from heron_core import solve_heron, SetSpec, Point, Segment, Polygon, Disk
from examples import get_example, EXAMPLE_NAMES
from viz import make_figure

st.set_page_config(page_title="Generalized Heron Problem — CVXPY + Streamlit", layout="wide")

st.title("Generalized Heron Problem — CVXPY + ECOS")
st.caption("Interactive simulations of four examples.")

with st.sidebar:
    ex_name = st.selectbox("Choose example", EXAMPLE_NAMES, index=0)
    n_frames = st.slider("Frames for animation sweep", 5, 200, 60, 5)
    autoplay = st.checkbox("Autoplay sweep", value=False)
    sleep_ms = st.slider("Frame delay (ms)", 0, 200, 30, 10)
    show_connectors = st.checkbox("Show connector lines", value=True)
    show_sets = st.checkbox("Show sets", value=True)
    show_legend = st.checkbox("Show legend", value=False)
    st.markdown("---")
    st.write("**Weights** (per set)")

example_factory = get_example(ex_name)

# param slider for the sweep (0..1)
alpha = st.slider("Parameter α (sweep this to animate)", 0.0, 1.0, 0.25, 0.01)

# Build sets & weights for this alpha
sets, weights, canvas = example_factory(alpha)

# Optional: edit weights in the sidebar
with st.sidebar:
    for i, w in enumerate(weights):
        weights[i] = st.number_input(f"w[{i+1}]", value=float(w), step=0.1, key=f"w_{i}")

# Solve once for current alpha
sol = solve_heron(sets, weights)

# Render current frame
fig = make_figure(sets, weights, sol, canvas, show_connectors=show_connectors, show_sets=show_sets, show_legend=show_legend)
st.plotly_chart(fig, use_container_width=True)

# Autoplay sweep across alpha
if autoplay:
    ph = st.empty()
    for t in np.linspace(0, 1, n_frames):
        sets_t, weights_t, canvas_t = example_factory(float(t))
        sol_t = solve_heron(sets_t, weights_t)
        fig_t = make_figure(sets_t, weights_t, sol_t, canvas_t, show_connectors=show_connectors, show_sets=show_sets, show_legend=show_legend)
        ph.plotly_chart(fig_t, use_container_width=True)
        time.sleep(sleep_ms/1000.0)

# Show numeric solution
st.subheader("Solution Data")
col1, col2 = st.columns(2)
with col1:
    st.write("**x\*** (minimizer):", np.array(sol['x']).round(4).tolist())
    st.write("**Objective value** (∑ wᵢ‖x − yᵢ‖):", round(float(sol['obj']), 6))
with col2:
    st.write("**Closest points yᵢ on each set Cᵢ**:")
    y_table = {f"y[{i+1}]": np.array(y).round(4).tolist() for i, y in enumerate(sol['y_list'])}
    st.json(y_table)

st.markdown("---")
st.caption("Built with CVXPY (ECOS), NumPy, and Plotly in Streamlit.")
