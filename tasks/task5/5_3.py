import matplotlib
from matplotlib import patheffects
import matplotlib.pyplot as plt
import numpy as np

import struct

maxStepSizes = []
means = []
cVs = []
ratios = []
temperatures = []
averageDistances = []

structFormat = struct.Struct("dddddd")
with open("./5_3/data.bin", "rb") as f:
    count, = struct.unpack("I", f.read(struct.calcsize("I")))

    for i in range(count):
        maxStepSize, temperature, mean, cV, ratio, averageDistance, = structFormat.unpack_from(
            f.read(structFormat.size))

        maxStepSizes.append(maxStepSize)
        temperatures.append(temperature)
        means.append(mean)
        cVs.append(cV)
        ratios.append(ratio)
        averageDistances.append(averageDistance)

plt.xkcd()
matplotlib.rcParams['path.effects'] = [
    patheffects.withStroke(linewidth=0, foreground='w')]


plt.figure()
plt.semilogx(temperatures, averageDistances, linewidth=1)
plt.xlabel("Temperature")
plt.ylabel("Average particle distance")
plt.savefig("./plots/5_3/acceptance.png", dpi=200, bbox_inches='tight')

plt.figure()
plt.plot(temperatures, averageDistances, linewidth=1)
plt.xlim((0.2, 1.0))
plt.xlabel("Temperature")
plt.ylabel("Average particle distance")
plt.savefig("./plots/5_3/small_range.png", dpi=200, bbox_inches='tight')
