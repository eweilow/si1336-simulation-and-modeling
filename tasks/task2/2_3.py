import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random


def integrate(x0, y0, z0):
    sigma = 10
    b = 8/3
    r = 28

    dt = 0.0001

    t = 0
    X = np.array([x0, y0, z0])

    dS = np.array([0.0, 0.0, 0.0])
    partialSum = np.array([0.0, 0.0, 0.0])

    def rungeKutta(f, s):
        nonlocal partialSum, dS
        partialSum[0] = 0
        partialSum[1] = 0
        partialSum[2] = 0

        f(dS, s)
        partialSum += dS * dt
        f(dS, s + dS/2 * dt)
        partialSum += 2 * dS * dt
        f(dS, s + dS/2 * dt)
        partialSum += 2 * dS * dt
        f(dS, s + dS * dt)
        partialSum += dS * dt

        return s + partialSum / 6

    def df(array, S):
        array[0] = -sigma * S[0] + sigma * S[1]
        array[1] = -S[0] * S[2] + r * S[0] - S[1]
        array[2] = S[0] * S[1] - b * S[2]

    T = 100.0
    length = np.int_(np.floor(T / dt))
    times = np.empty((length, 1))
    points = np.empty((length, 3))

    lastOutsideRadius = 0.0
    cutIndex = 0
    for i in range(0, length):
        times[i] = t
        points[i, :] = X
        X = rungeKutta(df, X)
        cutIndex = i

        norm = np.linalg.norm(X - [0, 0, r])
        if norm > r:
            lastOutsideRadius = t

        if t - lastOutsideRadius > 1:
            break

        t += dt

    return t, X[0], X[1], X[2], times[:cutIndex], points[:cutIndex], np.linalg.norm(X - [0, 0, r])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


R = 10000
# random.seed(5)
for i in range(500):
    x0 = random.uniform(-R, R)
    y0 = random.uniform(-R, R)
    z0 = random.uniform(-R, R)
    print("Running")
    t, x, y, z, times, points, N = integrate(x0, y0, z0)

    if N > 28:
        print("Plotting")
        ax.plot(points[:, 0], points[:, 1], points[:, 2])

plt.show()
