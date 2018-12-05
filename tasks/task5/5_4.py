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
plt.xkcd()
plt.plot(temperatures, cVs, linewidth=1)
plt.xlim((0.2, 1.0))
plt.ylim((0, 75))
plt.xlabel("Temperature")
plt.ylabel("Heat capacity")
plt.savefig("./plots/5_4/heat.png", dpi=200, bbox_inches='tight')

plt.figure()
plt.xkcd()
plt.plot(temperatures, means, linewidth=1)
plt.xlim((0.2, 1.0))
plt.ylim((-50, -25))
plt.xlabel("Temperature")
plt.ylabel("Energy")
plt.savefig("./plots/5_4/energy.png", dpi=200, bbox_inches='tight')
