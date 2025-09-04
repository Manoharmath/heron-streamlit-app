
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Union, Dict, Any

import numpy as np
import cvxpy as cp

# ---------- Convex set specs (all live in R^2) ----------

@dataclass
class Point:
    p: np.ndarray  # shape (2,)

@dataclass
class Segment:
    a: np.ndarray  # shape (2,)
    b: np.ndarray  # shape (2,)

@dataclass
class Polygon:
    V: np.ndarray  # shape (k, 2), convex polygon (assumed CCW and convex)

@dataclass
class Disk:
    c: np.ndarray  # center (2,)
    r: float       # radius >= 0

SetSpec = Union[Point, Segment, Polygon, Disk]

def _closest_point_vars(seti: SetSpec):
    """Return variables y_i and constraints describing membership y_i ∈ C_i for each set type."""
    if isinstance(seti, Point):
        # y is fixed = p (no variable required), but we keep a variable with equality to unify plotting
        y = cp.Variable(2)
        cons = [y == seti.p]
        return y, cons
    elif isinstance(seti, Segment):
        theta = cp.Variable(nonneg=True)
        y = seti.a + theta * (seti.b - seti.a)
        cons = [theta <= 1]
        return y, cons
    elif isinstance(seti, Polygon):
        k = seti.V.shape[0]
        lam = cp.Variable(k, nonneg=True)
        y = seti.V.T @ lam  # convex combination of vertices
        cons = [cp.sum(lam) == 1]
        return y, cons
    elif isinstance(seti, Disk):
        y = cp.Variable(2)
        cons = [cp.norm(y - seti.c, 2) <= seti.r]
        return y, cons
    else:
        raise ValueError("Unknown set type")

def solve_heron(sets: List[SetSpec], weights: List[float]) -> Dict[str, Any]:
    """
    Solve min_x ∑ w_i * dist(x, C_i) where C_i are convex sets in R^2.
    Introduce y_i ∈ C_i and t_i ≥ ‖x − y_i‖, then minimize ∑ w_i t_i.
    """
    m = len(sets)
    assert len(weights) == m

    x = cp.Variable(2)
    y_list = []
    t = cp.Variable(m, nonneg=True)
    constraints = []

    for i, seti in enumerate(sets):
        y_i, cons_i = _closest_point_vars(seti)
        y_list.append(y_i)
        constraints += cons_i
        constraints += [t[i] >= cp.norm(x - y_i, 2)]

    obj = cp.Minimize(cp.sum(cp.multiply(weights, t)))
    prob = cp.Problem(obj, constraints)
    prob.solve(solver=cp.ECOS, verbose=False)

    if prob.status not in ("optimal", "optimal_inaccurate"):
        raise RuntimeError(f"Solver status: {prob.status}")

    y_vals = [yi.value for yi in y_list]
    return {
        "x": x.value,
        "y_list": y_vals,
        "t": t.value,
        "obj": prob.value,
        "status": prob.status,
    }
