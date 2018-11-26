import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import scipy.optimize as opt

import sys

sys.setrecursionlimit(15000)

gridSize = 40
grid = np.zeros((gridSize, gridSize))
nextGrid = np.zeros_like(grid)

EMPTY = 0
TREE = 1
FIRE = 2

growthProbability = 0.1
lightningStrikeProbability = 0.1


spreadDirections = [[1, 0], [0, 1], [-1, 0], [0, -1]]


def spread(x, y, onType, toType):
    for direction in spreadDirections:
        nextX = (x + direction[0] + gridSize) % gridSize
        nextY = (y + direction[1] + gridSize) % gridSize

        if nextGrid[nextX, nextY] == onType:
            nextGrid[nextX, nextY] = toType
            spread(nextX, nextY, onType, toType)


def uniqueConnected(x, y, visited, ofType):
    if visited[x, y] == 1:
        return 0

    visited[x, y] = 1

    if not (grid[x, y] == ofType):
        return 0

    count = 1
    for direction in spreadDirections:
        nextX = (x + direction[0] + gridSize) % gridSize
        nextY = (y + direction[1] + gridSize) % gridSize
        count += uniqueConnected(nextX, nextY, visited, ofType)
    return count


fireCatched = []


def iterate():
    nextGrid[:, :] = grid[:, :]
    for x in range(gridSize):
        for y in range(gridSize):

            if grid[x, y] == EMPTY and rnd.random() < growthProbability:
                nextGrid[x, y] = TREE

            if grid[x, y] == TREE and rnd.random() < lightningStrikeProbability:
                nextGrid[x, y] = FIRE

            if grid[x, y] == FIRE:
                nextGrid[x, y] = EMPTY

    for x in range(gridSize):
        for y in range(gridSize):
            if nextGrid[x, y] == FIRE:
                spread(x, y, TREE, FIRE)

    grid[:, :] = nextGrid[:, :]

    visited = np.zeros_like(grid)
    for x in range(gridSize):
        for y in range(gridSize):
            uniqueGroup = uniqueConnected(x, y, visited, FIRE)
            if uniqueGroup > 0:
                fireCatched.append(uniqueGroup)


N = 3
plt.figure()
for i in range(N):
    for j in range(N):
        for n in range(10):
            iterate()
        plt.subplot(N, N, i*N + j + 1)
        plt.imshow(grid)
        plt.clim(EMPTY, FIRE)

plt.tight_layout()
plt.savefig("./plots/4_5/sample.png")

for i in range(100):
    iterate()


plt.figure()
n, bins, patches = plt.hist(fireCatched, 20)


def func(x, a):
    return n[0] * x**a


optimizeX = bins[1:]
optimizeY = n
optimizedParameters, pcov = opt.curve_fit(func, optimizeX, optimizeY)

plotx = np.linspace(np.amin(bins), np.amax(bins), 100)
#plt.plot(bins[:-1], n)
plt.plot(plotx, func(plotx, *optimizedParameters))

plt.xlabel("s")
plt.ylabel("N(s)")
plt.title("g = {1:.2f}, f = {2:.2f}, $\\alpha \\approx {0:.2f}$".format(
    optimizedParameters[0], growthProbability, lightningStrikeProbability), loc="left")
plt.figlegend(('$N s^{-\\alpha}$', 'Simulation histogram'))

plt.savefig("./plots/4_5/histogram.png")
