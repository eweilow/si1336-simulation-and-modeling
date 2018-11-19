
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import random as rnd
import math
from gradient_plot import plotGradientLine


def runRandomWalk(steps, canIntersect, preventBackfire):
    X = []
    Y = []
    indices = []

    x = 0
    y = 0

    direction = math.floor(rnd.uniform(0, 4))

    def intersectsSelf():
        for i in range(len(X)):
            if X[i] == x and Y[i] == y:
                return True
        return False

    def step():
        nonlocal x, y

        if direction == 0:
            x += 1

        if direction == 1:
            y += 1

        if direction == 2:
            x -= 1

        if direction == 3:
            y -= 1

    for i in range(steps):
        step()
        if not canIntersect and intersectsSelf():
            return None

        if preventBackfire:
            newDir = math.ceil(rnd.uniform(0, 3))
            direction = (direction - 2 + newDir) % 4
        else:
            direction = math.floor(rnd.uniform(0, 4))

        X.append(x)
        Y.append(y)
        indices.append(i)
    return (np.array(X), np.array(Y), np.array(indices))


def runUntilWorks(steps, canIntersect, preventBackfire):
    stepsRun = 1
    while True:
        val = runRandomWalk(steps, canIntersect, preventBackfire)
        if preventBackfire == False:
            return val, 1

        if val != None:
            return val, stepsRun
        stepsRun += 1


def runWithChoice(simLength, canIntersect, preventBackfire):
    x = np.int_(np.linspace(5, simLength, 5))
    y = np.int_(np.linspace(10, 1000, 10))
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    for i in range(0, len(x)):
        xval = x[i]
        for j in range(0, len(y)):
            yval = y[j]

            summedSquares = 0
            for sims in range(0, yval):
                (Xv, Yv, indices), stepsRun = runUntilWorks(
                    xval, canIntersect, preventBackfire)
                r = (Xv[0]-Xv[-1])**2 + (Yv[0]-Yv[-1])**2
                summedSquares += r / yval

            Z[j, i] = summedSquares
        # print(summedSquares)

    fig = plt.figure()
    plt.title(
        "With back-step protection" if preventBackfire else "Without back-step protection")
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z,
                    cmap='rainbow', edgecolor='none')
    ax.set_xlabel('walk length')
    ax.set_ylabel('walks run per length')
    ax.set_zlabel('$<R^2>$')
    ax.view_init(30, 135 + 90)
    plt.savefig("./plots/3_10/walklen_{0}.png".format(
                "with" if preventBackfire else "without"))


runWithChoice(50, False, True)
runWithChoice(50, True, False)
