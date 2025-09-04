
from typing import List, Dict, Any
import numpy as np
import plotly.graph_objects as go

from heron_core import SetSpec, Point, Segment, Polygon, Disk

def _plot_point(fig, p, name="point", color=None):
    fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers",
                             name=name, marker={"size":10}, showlegend=False))

def _plot_segment(fig, a, b, name="segment"):
    fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines",
                             name=name, showlegend=False))

def _plot_polygon(fig, V, name="polygon"):
    x = list(V[:,0]) + [V[0,0]]
    y = list(V[:,1]) + [V[0,1]]
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", fill="toself", opacity=0.15,
                             name=name, showlegend=False))

def _plot_disk(fig, c, r, name="disk"):
    th = np.linspace(0, 2*np.pi, 100)
    x = c[0] + r*np.cos(th)
    y = c[1] + r*np.sin(th)
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", fill="toself", opacity=0.15,
                             name=name, showlegend=False))

def make_figure(sets: List[SetSpec], weights: List[float], sol: Dict[str, Any], canvas: Dict[str, float],
                show_connectors=True, show_sets=True, show_legend=False):

    fig = go.Figure()

    # Draw sets
    if show_sets:
        for i, s in enumerate(sets):
            if isinstance(s, Point):
                _plot_point(fig, s.p, name=f"P{i+1}")
            elif isinstance(s, Segment):
                _plot_segment(fig, s.a, s.b, name=f"S{i+1}")
            elif isinstance(s, Polygon):
                _plot_polygon(fig, s.V, name=f"Poly{i+1}")
            elif isinstance(s, Disk):
                _plot_disk(fig, s.c, s.r, name=f"D{i+1}")

    # Draw solution x*
    x = np.array(sol["x"]).reshape(2,)
    fig.add_trace(go.Scatter(x=[x[0]], y=[x[1]], mode="markers",
                             name="x*", marker={"size":14, "symbol":"star"}, showlegend=True))

    # Connectors x* -> y_i (closest points)
    if show_connectors:
        for i, y in enumerate(sol["y_list"]):
            y = np.array(y).reshape(2,)
            fig.add_trace(go.Scatter(x=[x[0], y[0]], y=[x[1], y[1]],
                                     mode="lines+markers", name=f"Conn {i+1} (w={weights[i]:.2f})",
                                     marker={"size":6}, showlegend=show_legend))

    fig.update_layout(
        width=None, height=650,
        xaxis_title="x",
        yaxis_title="y",
        xaxis=dict(range=[canvas["xmin"], canvas["xmax"]], zeroline=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[canvas["ymin"], canvas["ymax"]], zeroline=False),
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h")
    )
    return fig
