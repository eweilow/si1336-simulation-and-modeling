import numpy as np
import random as rnd

import sys

sys.setrecursionlimit(15000)


def treeSimulation(gridSize, growthProbability, lightningStrikeProbability):
    grid = np.zeros((gridSize, gridSize))
    nextGrid = np.zeros_like(grid)

    EMPTY = 0
    TREE = 1
    FIRE = 2

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

    N = 0

    def iterate():
        nonlocal N
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
                if uniqueGroup > 0 and N > 10:
                    fireCatched.append(uniqueGroup)
        N += 1

    def getFireCatched():
        return fireCatched

    def getGrid():
        return grid

    return iterate, getFireCatched, getGrid
