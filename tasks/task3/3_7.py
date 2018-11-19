
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import math
from gradient_plot import plotGradientLine


def runRandomWalk(steps, r0, a, c, m):
    currentRandomState = r0

    def customRandom():
        nonlocal currentRandomState

        currentRandomState = (a * currentRandomState + c) % m
        return currentRandomState / (m - 1)

    X = []
    Y = []
    indices = []

    x = 0
    y = 0

    for i in range(steps):
        direction = math.floor(customRandom() * 4)

        if direction == 0:
            x += 1

        if direction == 1:
            y += 1

        if direction == 2:
            x -= 1

        if direction == 3:
            y -= 1

        X.append(x)
        Y.append(y)
        indices.append(i)
    return X, Y, np.array(indices)


plt.figure()
plt.title("1000 steps")
X, Y, indices = runRandomWalk(1000, 1, 3, 4, 128)
plotGradientLine(X, Y, indices)
plt.savefig("./plots/3_7/randomwalk_1000_128.png")

plt.figure()
plt.title("1000 steps")
X, Y, indices = runRandomWalk(1000, 1, 3, 4, 129)
plotGradientLine(X, Y, indices)
plt.savefig("./plots/3_7/randomwalk_1000_129.png")

plt.figure()
plt.title("1000 steps")
X, Y, indices = runRandomWalk(1000, 1, 3, 4, 130)
plotGradientLine(X, Y, indices)
plt.savefig("./plots/3_7/randomwalk_1000_130.png")
