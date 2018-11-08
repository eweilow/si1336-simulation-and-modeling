import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def integrate(x0, y0, z0):
    sigma = 10
    b = 8/3
    r = 28

    dt = 0.0001

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

    while t < 25:
        step()

    return np.array(tvals), np.array(xvals), np.array(yvals), np.array(zvals)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

t0, x0, y0, z0 = integrate(25, 0, 0)
t1, x1, y1, z1 = integrate(25 + 0.01, 0, 0)

ax.plot(x0, y0, z0)
ax.plot(x1, y1, z1)
plt.figlegend(('$x_0 = 25$', '$x_0 = 25.01$'))

dx = x0 - x1
dy = y0 - y1
dz = z0 - z1
plt.savefig("./plots/2_4/solution.png")

plt.figure()
r = np.sqrt(dx**2 + dy**2 + dz**2)
plt.plot(r, t0)
plt.ylabel("t")
plt.xlabel(
    "$\sqrt{(x_0(t) - x_1(t))^2 + (y_0(t) - y_1(t))^2 + (z_0(t) - z_1(t))^2}$")
plt.savefig("./plots/2_4/difference.png")
