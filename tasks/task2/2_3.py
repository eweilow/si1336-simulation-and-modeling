import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def integrate(x0, y0, z0):
    sigma = 10
    b = 8/3
    r = 28

    dt = 0.001

    t = 0
    X = np.array([x0, y0, z0])

    tvals = []
    xvals = []
    yvals = []
    zvals = []

    i = 0

    def rungeKutta(f, s):
        k1 = dt * f(s)
        k2 = dt * f(s + k1/2)
        k3 = dt * f(s + k2/2)
        k4 = dt * f(s + k3)

        return s + (k1 + 2*k2 + 2*k3 + k4) / 6

    def df(S):
        return np.array([
            -sigma * S[0] + sigma * S[1],
            -S[0] * S[2] + r * S[0] - S[1],
            S[0] * S[1] - b * S[2]
        ])

    def step():
        nonlocal t, X

        if i % 1000 == 0:
            tvals.append(t)
            xvals.append(X[0])
            yvals.append(X[1])
            zvals.append(X[2])

        X = rungeKutta(df, X)

        t += dt

    while t < 5:
        step()

    return tvals, xvals, yvals, zvals


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for x0 in range(-100, 101, 50):
    for y0 in range(-100, 101, 50):
        for z0 in range(-100, 101, 50):
            t, x, y, z = integrate(x0, y0, z0)

            ax.plot(x, y, z)

plt.show()
