
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


def runSavePlot(r0, a, c, m):
    plt.figure()
    plt.title(
        "1000 steps (r = {0}, a = {1}, c = {2}, m = {3})".format(r0, a, c, m))
    X, Y, indices = runRandomWalk(1000, r0, a, c, m)
    plotGradientLine(X, Y, indices)
    plt.savefig(
        "./plots/3_7/randomwalk_1000_r{0}_a{1}_c{2}_m{3}.png".format(r0, a, c, m))


runSavePlot(1, 3, 4, 128)
runSavePlot(1, 3, 4, 129)
runSavePlot(1, 3, 4, 130)

runSavePlot(1, 3, 4, 128)
runSavePlot(1, 4, 4, 128)
runSavePlot(1, 5, 4, 128)

runSavePlot(1, 3, 5, 128)
runSavePlot(1, 3, 6, 128)
runSavePlot(1, 3, 7, 128)

runSavePlot(1, 3, 4, 128)
runSavePlot(2, 3, 4, 128)
runSavePlot(3, 3, 4, 128)
