import struct
import numpy as np
import matplotlib
import scipy.optimize as opt
from mpl_toolkits import mplot3d
from matplotlib import patheffects
import matplotlib.pyplot as plt


def loadFile(filename):
    with open(filename, "rb") as f:
        points, = struct.unpack("L", f.read(struct.calcsize("L")))
        relaxations, = struct.unpack("L", f.read(struct.calcsize("L")))
        accuracy, = struct.unpack("d", f.read(struct.calcsize("d")))

        data = np.zeros((points, points))
        for x in range(0, points):
            for y in range(0, points):
                p, = struct.unpack("d", f.read(struct.calcsize("d")))
                data[x, y] = p
        return points, relaxations, accuracy, data


def loadRelaxationsFile(filename):
    with open(filename, "rb") as f:
        points, = struct.unpack("L", f.read(struct.calcsize("L")))

        gridSizes = np.zeros(points)
        relaxations = np.zeros(points)

        for x in range(0, points):
            p, = struct.unpack("d", f.read(struct.calcsize("d")))
            gridSizes[x] = p
        for x in range(0, points):
            p, = struct.unpack("L", f.read(struct.calcsize("L")))
            relaxations[x] = p
        return gridSizes, relaxations


def loadParametersFile(filename):
    with open(filename, "rb") as f:
        dimension, = struct.unpack("d", f.read(struct.calcsize("d")))
        desiredAccuracy, = struct.unpack("d", f.read(struct.calcsize("d")))
        equivalentRun, = struct.unpack("d", f.read(struct.calcsize("d")))
        realRun, = struct.unpack("L", f.read(struct.calcsize("L")))
        powerOfTwoMax, = struct.unpack("L", f.read(struct.calcsize("L")))
        powerOfTwoWanted, = struct.unpack("L", f.read(struct.calcsize("L")))
        relaxationsPerProlongation, = struct.unpack(
            "L", f.read(struct.calcsize("L")))
        relaxationsPerRestriction, = struct.unpack(
            "L", f.read(struct.calcsize("L")))

        return dimension, equivalentRun, realRun, desiredAccuracy*100, 2**powerOfTwoMax, 2**powerOfTwoWanted, relaxationsPerProlongation, relaxationsPerRestriction


def optimizePlotRelaxations(gridPoints, relaxations):
    def func(x, a, b):
        return b * x**a

    optimizedParameters, pcov = opt.curve_fit(
        func, gridPoints, relaxations, method='lm', maxfev=10000)

    return func, optimizedParameters


def plotRelaxations(filename, gridSizes, relaxations):
    plt.figure()
    ax = plt.axes()
    plt.xkcd()
    matplotlib.rcParams['path.effects'] = [
        patheffects.withStroke(linewidth=0, foreground='w')]
    matplotlib.rcParams['legend.loc'] = "best"
    gridPoints = 10/gridSizes

    F, pars = optimizePlotRelaxations(gridPoints, relaxations)

    ax.loglog(gridPoints, relaxations)
    ax.loglog(gridPoints, F(gridPoints, pars[0], pars[1]), "--")
    plt.title("Relaxations for different grid sizes")
    plt.xlabel("Grid points (n)")
    plt.ylabel("Relaxations necessary")
    ax.legend(("Data from computations", "Fit curve (${1:.2f} n^{{{0:.2f}}})$".format(pars[0], pars[1])),
              loc='best')
    plt.savefig(filename, dpi=240, bbox_inches='tight')


def plotData(
    filename,
    points,
    relaxations,
    accuracy,
    data,
    use3d=True,
    linearDimension=10,
    realTitle=False,
    postfix=True
):
    matplotlib.rcParams['path.effects'] = [
        patheffects.withStroke(linewidth=0, foreground='w')]

    x, y = np.meshgrid(np.linspace(0, linearDimension, points),
                       np.linspace(0, linearDimension, points))

    title = "Accuracy: {0:.2f}%, {1} relaxations".format(
        accuracy * 100, relaxations)

    if not realTitle == False:
        if postfix:
            title = realTitle + ", " + title
        else:
            title = realTitle
    plt.figure()
    plt.xkcd()
    if use3d:
        ax = plt.axes(projection='3d')
        ax.set_title(title, pad=16)
        surf = ax.plot_surface(x, y, data, cmap='rainbow',
                               edgecolor='none', shade=True)
        ax.plot_wireframe(x, y, data, rstride=1, cstride=10, alpha=0.2)
        ax.view_init(35, 135 + 75)
        plt.xlabel("x")
        plt.ylabel("y")
        # plt.colorbar(surf)
        ax.set_zlim(np.amin(data), np.amax(data))
        plt.savefig(filename, dpi=240)
    else:
        plt.title(title)
        plt.contour(data, extent=(0, linearDimension,
                                  0, linearDimension), cmap="rainbow")
        plt.xlabel("x")
        plt.ylabel("y")
        #plt.imshow(data, extent=(0, 10, 0, 10))
        plt.colorbar()
        plt.savefig(filename, dpi=240, bbox_inches='tight')
