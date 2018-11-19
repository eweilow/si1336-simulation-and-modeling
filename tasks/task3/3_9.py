
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import random as rnd
import math
from gradient_plot import plotGradientLine


def runRandomWalk(steps, preventBackfire):
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
        if intersectsSelf():
            return None

        if preventBackfire:
            newDir = math.ceil(rnd.uniform(0, 3))
            direction = (direction - 2 + newDir) % 4
        else:
            direction = math.floor(rnd.uniform(0, 4))

        X.append(x)
        Y.append(y)
        indices.append(i)
    return X, Y, np.array(indices)


def runUntilWorks(steps, preventBackfire):
    stepsRun = 1
    while True:
        val = runRandomWalk(steps, preventBackfire)
        if val != None:
            return val, stepsRun
        stepsRun += 1


print("Plotting sample solutions")
for i in range(5, 40, 5):
    plt.figure()
    plt.title("{0} steps, non intersecting".format(i))
    (X, Y, indices), stepsRun = runUntilWorks(i, True)
    print("{0} steps needed for length {1}".format(stepsRun, i))
    plotGradientLine(X, Y, indices)
    plt.savefig("./plots/3_9/randomwalk_{0}.png".format(i))


def computeMeans(start, end, step, preventBackfire):
    print("Computing mean steps necessary {0} backfire protection".format(
          "with" if preventBackfire else "without"))
    indices = []
    means = []
    stepsRunPerSuccess = []
    for i in range(start, end, step):
        N = 50
        runWalks = 0
        for n in range(N):
            _, stepsRun = runUntilWorks(i, preventBackfire)
            runWalks += stepsRun

        print("{0} walks run, {1} successes. ratio: {2}".format(
            runWalks, N, N / runWalks))
        indices.append(i)
        means.append(N / runWalks)
        stepsRunPerSuccess.append(runWalks / N)

    return indices, means, stepsRunPerSuccess


indices1, means1, counts1 = computeMeans(1, 50, 1, True)
indices2, means2, counts2 = computeMeans(1, 25, 1, False)

plt.figure()
plt.plot(indices1, means1)
plt.plot(indices2, means2)
plt.figlegend(('With back-move protection', 'Without back-move protection'))
plt.xlabel("walk length")
plt.ylabel("walk success fraction")
plt.savefig("./plots/3_9/success_fraction.png")

plt.figure()
plt.plot(indices1, counts1)
plt.plot(indices2, counts2)
plt.figlegend(('With back-move protection', 'Without back-move protection'))
plt.xlabel("walk length")
plt.ylabel("attempts per success")
plt.savefig("./plots/3_9/per_success.png")
