import matplotlib.pyplot as plt
import scipy.optimize as opt
from mpl_toolkits import mplot3d
import numpy as np
from treeSim import treeSimulation


def optimize(g, f, name=False, save=False):
    iterate, getFireCatched, getGrid = treeSimulation(40, g, f)

    for i in range(5):
        iterate()

    n, bins = np.histogram(getFireCatched(), 25)

    def func(x, a, b):
        return b * x**a

    optimizeX = 0.5 * (bins[1:] + bins[:-1])
    optimizeY = n

    try:
        optimizedParameters, pcov = opt.curve_fit(
            func, optimizeX, optimizeY, method='lm', maxfev=10000)
    except:
        optimizedParameters, pcov = opt.curve_fit(
            func, optimizeX, optimizeY, method='lm', maxfev=1000000)

    plotx = np.linspace(np.amin(bins), np.amax(bins), 100)

    if save:
        plt.figure()
        plt.hist(getFireCatched(), 25)
        plt.plot(plotx, func(
            plotx, optimizedParameters[0], optimizedParameters[1]))

        plt.xlabel("s")
        plt.ylabel("N(s)")
        plt.xlim((np.amin(bins), np.amax(bins)))
        plt.ylim((0, np.amax(n)))
        plt.title("g = {1:.2f}, f = {2:.2f},\n$\\alpha \\approx {0:.2f}$, $N \\approx {3:.0f}$".format(
            optimizedParameters[0], g, f, optimizedParameters[1]), loc="left")
        plt.figlegend(('$N s^{-\\alpha}$', 'Simulation histogram'))

        plt.savefig("./plots/4_5/" + name, dpi=160)

    return optimizedParameters[0]


optimize(0.1, 0.1, "histogram.png", True)

nvals = 10
growthProbabilities = np.linspace(0.1, 0.5, nvals)
fireProbabilities = np.linspace(0.1, 0.5, nvals)

X, Y = np.meshgrid(growthProbabilities, fireProbabilities)
Z = np.zeros_like(X)

N = 1

for i in range(0, len(growthProbabilities)):
    for j in range(0, len(fireProbabilities)):
        for n in range(N):
            g = growthProbabilities[i]
            f = fireProbabilities[j]
            alpha = optimize(g, f)
            Z[i, j] += alpha / N
            print("{0:.2f} {1:.2f} {2:.2f}".format(g, f, alpha))

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z,
                cmap='rainbow', edgecolor='none')
ax.set_xlabel('Growth probability')
ax.set_ylabel('Lightning strike probability')
ax.set_zlabel('$\\alpha$')
ax.view_init(45, 135 + 90 + 180)
plt.savefig("./plots/4_5/parameters.png", dpi=200)
