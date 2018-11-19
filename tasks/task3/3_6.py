
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


# , Y = runRandomWalk(1000)
# lt.figure()
#lt.plot(X, Y)
# lt.savefig("./plots/3_6/randomwalk_1000.png")
#
# , Y = runRandomWalk(100)
# lt.figure()
#lt.plot(X, Y)
# lt.savefig("./plots/3_6/randomwalk_100.png")
#
#X, Y = runRandomWalk(10)
#fig, axs = plt.subplots()
#points = np.array([X, Y]).T.reshape(-1, 1, 2)
#segments = np.concatenate([points[:-1], points[1:]], axis=1)
#
#norm = plt.Normalize(0, 10)
#lc = LineCollection(segments, cmap='viridis', norm=norm)
# Set the values used for colormapping
#lc.set_array(np.array(range(0, 10)))
# lc.set_linewidth(2)
#line = axs.add_collection(lc)
#fig.colorbar(line, ax=axs)
#
# plt.savefig("./plots/3_6/randomwalk_10.png")
#

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
