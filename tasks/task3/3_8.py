
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import random as rnd
import math
from gradient_plot import plotGradientLine


def runRandomWalk(steps):
    X = np.zeros((1, steps))
    Y = np.zeros((1, steps))
    indices = np.zeros((1, steps))

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

        X[0, i] = x
        Y[0, i] = y
        indices[0, i] = i
    return X, Y, indices


x = np.int_(np.linspace(10, 1000, 15))
y = np.int_(np.linspace(10, 1000, 15))
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)

for i in range(0, len(x)):
    xval = x[i]
    for j in range(0, len(y)):
        yval = y[j]

        summedSquares = 0
        for sims in range(0, yval):
            Xv, Yv, indices = runRandomWalk(xval)
            r = (Xv[0, 0]-Xv[0, -1])**2 + (Yv[0, 0]-Yv[0, -1])**2
            summedSquares += r / yval

        Z[j, i] = summedSquares
    # print(summedSquares)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z,
                cmap='rainbow', edgecolor='none')
ax.set_xlabel('walk length')
ax.set_ylabel('walks run per length')
ax.set_zlabel('$<R^2>$')
ax.view_init(30, 135 + 90)
plt.savefig("./plots/3_8/walklen.png")
