# Generalized Heron Problem — Streamlit Demo

This app shows interactive simulations/animations for four examples
of the Generalized Heron problem using CVXPY with the ECOS solver.

## Quick start
```bash
# 1) create venv (optional but recommended)
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# 2) install deps
pip install -r requirements.txt

# 3) run
streamlit run app.py
```

## Notes
- All examples are 2D for visualization.
- Animation is done by sweeping a parameter `alpha` (0→1) that moves one of the sets.
- Plots are built with Plotly; Streamlit renders them interactively.
