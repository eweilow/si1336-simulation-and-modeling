import struct
import numpy as np
import matplotlib
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


def plotData(
    filename,
    points,
    relaxations,
    accuracy,
    data,
    use3d=True
):
    matplotlib.rcParams['path.effects'] = [
        patheffects.withStroke(linewidth=0, foreground='w')]

    x, y = np.meshgrid(np.linspace(0, 10, points),
                       np.linspace(0, 10, points))

    title = "Accuracy: {0:.2f}%, {1} relaxations".format(
        accuracy * 100, relaxations)
    plt.figure()
    plt.xkcd()
    if use3d:
        ax = plt.axes(projection='3d')
        ax.set_title(title, pad=16)
        surf = ax.plot_surface(x, y, data, cmap='rainbow',
                               edgecolor='none', shade=True)
        ax.plot_wireframe(x, y, data, rstride=1, cstride=10, alpha=0.2)
        ax.view_init(35, 135 + 75)
        # plt.colorbar(surf)
        ax.set_zlim(np.amin(data), np.amax(data))
    else:
        plt.title(title)
        plt.contour(data, extent=(0, 10, 0, 10), cmap="rainbow")
        #plt.imshow(data, extent=(0, 10, 0, 10))
        plt.colorbar()

    plt.savefig(filename, dpi=240)
