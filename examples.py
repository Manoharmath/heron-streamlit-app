
import numpy as np
from typing import Tuple, List, Callable

from heron_core import Point, Segment, Polygon, Disk, SetSpec

EXAMPLE_NAMES = [
    "A) Three points (classic Fermat/Heron)",
    "B) Two points + a segment",
    "C) A point + two disks",
    "D) Polygon + moving point (animated)",
]

def _canvas(xmin=-2, xmax=6, ymin=-2, ymax=6):
    return dict(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

def ex_A(alpha: float) -> Tuple[List[SetSpec], List[float], dict]:
    # Fixed three points; weights morph slightly with alpha
    P1 = Point(np.array([0.0, 0.0]))
    P2 = Point(np.array([4.0, 0.0]))
    P3 = Point(np.array([2.0, 3.5]))
    sets = [P1, P2, P3]
    w = [1.0, 1.0, 0.8 + 0.4*alpha]  # vary one weight for visual interest
    return sets, w, _canvas()

def ex_B(alpha: float):
    # Two points and a segment that rotates slightly with alpha
    P1 = Point(np.array([0.5, 4.5]))
    P2 = Point(np.array([4.5, 4.0]))
    base_a = np.array([1.0, 0.2])
    base_b = np.array([5.0, 0.5])
    # small rotation around center
    c = (base_a + base_b) / 2
    def rot(v, th):
        R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        return (R @ (v - c)) + c
    th = (alpha - 0.5) * 0.6  # -0.3..+0.3 rad
    S = Segment(rot(base_a, th), rot(base_b, th))
    sets = [P1, P2, S]
    w = [1.0, 1.0, 1.0]
    return sets, w, _canvas()

def ex_C(alpha: float):
    # One point and two disks; radii/positions vary with alpha
    P = Point(np.array([1.0, 1.2]))
    D1 = Disk(np.array([4.0, 1.2 + 0.8*alpha]), 0.7 + 0.3*alpha)
    D2 = Disk(np.array([2.0 + 1.0*np.sin(2*np.pi*alpha), 4.5]), 0.9)
    sets = [P, D1, D2]
    w = [1.0, 0.9, 1.1]
    return sets, w, _canvas()

def ex_D(alpha: float):
    # Convex polygon + a moving point; polygon is a pentagon
    V = np.array([[0.5, 1.0],
                  [1.8, 0.2],
                  [3.8, 0.8],
                  [4.2, 2.8],
                  [1.2, 3.5]])
    Poly = Polygon(V)
    # moving point traces a circle-ish path
    r = 1.5
    center = np.array([3.5, 3.7])
    angle = 2*np.pi*alpha
    P_mov = Point(center + r*np.array([np.cos(angle), np.sin(angle)]))
    sets = [Poly, P_mov]
    w = [1.0, 1.0]
    return sets, w, _canvas()

def get_example(name: str) -> Callable[[float], Tuple[List[SetSpec], List[float], dict]]:
    mapping = {
        EXAMPLE_NAMES[0]: ex_A,
        EXAMPLE_NAMES[1]: ex_B,
        EXAMPLE_NAMES[2]: ex_C,
        EXAMPLE_NAMES[3]: ex_D,
    }
    return mapping[name]
