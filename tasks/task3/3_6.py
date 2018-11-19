
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import math
from gradient_plot import plotGradientLine


def runRandomWalk(steps):
    X = []
    Y = []
    indices = []

    x = 0
    y = 0

    for i in range(steps):
        direction = math.floor(rnd.uniform(0, 4))

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
X, Y, indices = runRandomWalk(1000)
plotGradientLine(X, Y, indices)
plt.savefig("./plots/3_6/randomwalk_1000.png")

plt.figure()
plt.title("100 steps")
X, Y, indices = runRandomWalk(100)
plotGradientLine(X, Y, indices)
plt.savefig("./plots/3_6/randomwalk_100.png")

plt.figure()
plt.title("10 steps")
X, Y, indices = runRandomWalk(10)
plotGradientLine(X, Y, indices)
plt.savefig("./plots/3_6/randomwalk_10.png")
