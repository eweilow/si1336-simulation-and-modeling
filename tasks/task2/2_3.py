import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random


sigma = 10
b = 8/3
r = 28


def integrate(x0, y0, z0):
    dt = 0.00008

    t = 0
    X = np.array([x0, y0, z0])

    dS = np.array([0.0, 0.0, 0.0])
    partialSum = np.array([0.0, 0.0, 0.0])

    def rungeKutta(f, s):
        nonlocal partialSum, dS

        f(dS, s)
        partialSum = dS * dt
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

    T = 150.0
    length = np.int_(np.floor(T / dt))
    # times = np.empty((length, 1))
    # points = np.empty((length, 3))

    average = 0
    R = [0, 0, r]

    runningAverage = np.empty((length, 1))
    for i in range(0, length):
        # times[i] = t
        # points[i, :] = X
        X = rungeKutta(df, X)
        t += dt

        average += np.linalg.norm(X - R) / length
        #runningAverage[i] = average / (i + 1)

    # , times, points
    return t, np.array(X[0]), np.array(X[1]), np.array(X[2]), average


def process(x0, y0, z0):
    return integrate(x0, y0, z0)
    # t, x, y, z, times, points = integrate(x0, y0, z0)
    length = len(times)

    R = [0, 0, r]
    average = 0

    runningAverage = np.empty((length, 1))
    norms = np.empty((length, 1))

    for i in range(0, length):
        norms[i] = np.linalg.norm(points[i] - R)
        average += norms[i]
        runningAverage[i] = average / (i + 1)

        return t, x, y, z, runningAverage
        # return t, x, y, z, times, points, runningAverage, norms


fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')


R = 10000

#N = 100
#averages = np.empty((N, 1))
#indices = np.empty((N, 1))

f = open("data.txt", "a+")
i = 0
while True:
    #indices[i] = i
    i += 1

    x0 = random.uniform(-R, R)
    y0 = random.uniform(-R, R)
    z0 = random.uniform(-R, R)
    # t, x, y, z, times, points, runningAverage, norms = process(
    #    x0, y0, z0)

    t, x, y, z, runningAverage = process(
        x0, y0, z0)

    #averages[i] = runningAverage

    s = "{0} {1} {2} {3} {4}".format(i+1, x0, y0, z0, runningAverage)
    print(s)
    f.write(s + "\n")
    f.flush()
    # if runningAverage[-1] > r:
    # print("Plotting")
    # plt.plot(times, runningAverage)

    # plt.plot(times, norms)

    # if not isInside:
    # ax.plot(points[:, 0], points[:, 1], points[:, 2])

plt.plot(indices, averages)
plt.show()
