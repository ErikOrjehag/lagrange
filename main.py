import sympy as sp
import numpy as np

t = sp.symbols("t")

l0 = 0.5
l1 = 0.3
m0 = 0.2
m1 = 0.4

I0 = np.array([
    [0, 0, 0],
    [0, m0*l0**2/12, 0],
    [0, 0, m0*l0**2/12],
])

I1 = np.array([
    [0, 0, 0],
    [0, m1*l1**2/12, 0],
    [0, 0, m1*l1**2/12],
])

G0 = np.diag([m0, m0, I0])
G1 = np.diag([m1, m1, I1])

print("asd")