import matplotlib
from matplotlib import patheffects
import matplotlib.pyplot as plt
import numpy as np

import struct

maxStepSizes = []
means = []
cVs = []
ratios = []

structFormat = struct.Struct("dddd")
with open("./5_2/data.bin", "rb") as f:
    count, = struct.unpack("I", f.read(struct.calcsize("I")))

    for i in range(count):
        maxStepSize, mean, cV, ratio, = structFormat.unpack_from(
            f.read(structFormat.size))

        maxStepSizes.append(maxStepSize)
        means.append(mean)
        cVs.append(cV)
        ratios.append(ratio)

plt.xkcd()
matplotlib.rcParams['path.effects'] = [
    patheffects.withStroke(linewidth=0, foreground='w')]


plt.figure()
plt.semilogx([min(maxStepSizes), max(maxStepSizes)],
             [ratios[-1], ratios[-1]], "--")
plt.semilogx(maxStepSizes, ratios, linewidth=1)
plt.xlabel("Step size")
plt.ylabel("Acceptance ratio")
plt.savefig("./plots/5_2/acceptance.png", dpi=200, bbox_inches='tight')

plt.figure()
plt.semilogx(maxStepSizes, means, linewidth=1)
plt.xlabel("Step size")
plt.ylabel("<E>")
plt.savefig("./plots/5_2/convergence.png", dpi=200, bbox_inches='tight')

plt.figure()
plt.semilogx([min(maxStepSizes), max(maxStepSizes)],
             [10, 10], "--")
plt.semilogx(maxStepSizes, cVs, linewidth=1)
plt.ylim((0, 40))
plt.xlabel("Step size")
plt.ylabel("cV")
plt.savefig("./plots/5_2/cV.png", dpi=200, bbox_inches='tight')
