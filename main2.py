import sympy as sp
import numpy as np
from dataclasses import dataclass
import typing as tp

t = sp.Symbol("t", real=True, positive=True)

@dataclass
class Link:
    p: tp.Optional['Link']
    m: float
    l: float
    I: np.ndarray # 3x3
    q: float

def create_link(p: tp.Optional[Link], m: float, l: float, q: float, inertia: str):
    if inertia == "slender-bar":
        I = np.array([
            [0.0, 0.0, 0.0],
            [0.0, m*l**2/12, 0.0],
            [0.0, 0.0, m*l**2/12],
        ])
    else:
        assert False, f"not implemented: {inertia}"
    return Link(p=p, m=m, l=l, I=I, q=q)

links = []
links.append(create_link(p=None, m=1.0, l=1.0, q=0.0, inertia="slender-bar"))
links.append(create_link(p=links[0], m=1.0, l=1.0, q=0.0, inertia="slender-bar"))

def to_q(links: tp.List[Link]):
    q = sp.Matrix([
        sp.Function(f"q{i}", real=True)(t)
        for i in range(len(links))
    ])
    assert q.shape == (len(links), 1), "nx1"
    return q

def Rz(q):
    R = sp.Matrix([
        [sp.cos(q), -sp.sin(q), 0.0],
        [sp.sin(q), sp.cos(q), 0.0],
        [0.0, 0.0, 1.0],
    ])
    return R

def inertia_matrix(links: tp.List[Link]):
    q = to_q(links)
    dq = q.diff(t)
    # TODO: Follow parent chaining and determine axis, add prismatic links
    R = [Rz(qi) for qi in np.cumsum(q)]
    # TODO: Follow parent chaining and determine axis, add prismatic links
    # w = Jw*dq
    Jw = [
        sp.Matrix([
            [0, 0],
            [0, 0],
            [1, 0],
        ]),
        sp.Matrix([
            [0, 0],
            [0, 0],
            [1, 1],
        ])
    ]
    # TODO: Follow parent chaining and determine axis, add prismatic links, add offset for CoM
    c0 = sp.Matrix([
        links[0].l/2 * sp.cos(q[0]),
        links[0].l/2 * sp.sin(q[0]),
        0.0
    ])
    c1 = sp.Matrix([
        links[0].l * sp.cos(q[0]) + links[1].l/2 * sp.cos(q[1]),
        links[0].l * sp.cos(q[0]) + links[1].l/2 * sp.sin(q[1]),
        0.0
    ])
    # dc0 = c0.diff(t)
    # dc1 = c1.diff(t)
    #Jv0 = dc0.collect(dq)
    Jv0 = c0.jacobian(q) # Vc0 = Cv0 * dq
    Jv1 = c1.jacobian(q)
    Jv = [Jv0, Jv1]

    D = sum([
        links[i].m * Jv[i].T * Jv[i] + Jw[i].T * R[i] * links[i].I * R[i].T * Jw[i]
        for i in range(len(links))
    ], sp.zeros(len(links)))

    print("ASD")
    # assert Dq.shape == (len(links), len(links)), "nxn"
    # assert Dq.T = Dq, "symetric"
    # assert Dq.is_positive_definite, "positive definite"

def kinetic_enegy(links: tp.List[Link]):
    q = to_q(links)
    dq = q.diff(t)
    Dq = inertia_matrix(links)
    K = 0.5 * dq.T * Dq * dq

kinetic_enegy(links)