
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


def plotGradientLine(X, Y, indices):
    points = np.array([X, Y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    cmap = plt.get_cmap('rainbow')
    lc = LineCollection(segments, cmap=cmap,
                        norm=plt.Normalize(indices[0], indices[len(indices)-1]))
    lc.set_array(indices)
    lc.set_linewidth(2)

    line = plt.gca().add_collection(lc)
    plt.xlim(np.min(X)-5, np.max(X)+5)
    plt.ylim(np.min(Y)-5, np.max(Y)+5)
    plt.colorbar(line, ax=plt.gca())
