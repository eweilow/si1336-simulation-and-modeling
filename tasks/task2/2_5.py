import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import scipy.signal as sp

T = 100


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

        tvals.append(t)
        xvals.append(X[0])
        yvals.append(X[1])
        zvals.append(X[2])

        X = rungeKutta(df, X)

        t += dt

    while t < T:
        step()

    return np.array(tvals), np.array(xvals), np.array(yvals), np.array(zvals)


t, x, y, z = integrate(10, 0, 0)

peaks, _ = sp.find_peaks(z)
peakTimes = t[peaks]
peakValues = z[peaks]

plt.figure()
#plt.plot(peakTimes, peakValues)
plt.xlim((1, T))
plt.ylim((-0.05, 0.05))
plt.plot(t, np.log(z / np.roll(z, 1)))
plt.show()
