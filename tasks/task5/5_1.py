from matplotlib import patheffects
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import struct

skipValue = 0
stepsArrays = []
meansArrays = []
deltasArrays = []
names = ["./5_1/data_0dot2.bin",
         "./5_1/data_0dot8.bin", "./5_1/data_1dot6.bin", "./5_1/data_6dot4.bin"]
legendNames = ["$\delta = 0.2$", "$\delta = 0.8$",
               "$\delta = 1.6$", "$\delta = 6.4$"]

for filename in names:
    with open(filename, "rb") as f:
        count, = struct.unpack("Q", f.read(struct.calcsize("Q")))
        step, = struct.unpack("Q", f.read(struct.calcsize("Q")))
        skip, = struct.unpack("Q", f.read(struct.calcsize("Q")))
        skipValue = skip

        steps = []
        means = []
        deltas = []
        for n in range(count):
            steps.append(step * n + skip)
            mean, = struct.unpack("d", f.read(struct.calcsize("d")))
            means.append(mean)
        for n in range(count):
            delta, = struct.unpack("d", f.read(struct.calcsize("d")))
            deltas.append(delta)

        stepsArrays.append(steps)
        meansArrays.append(means)
        deltasArrays.append(deltas)

plt.xkcd()
matplotlib.rcParams['path.effects'] = [
    patheffects.withStroke(linewidth=0, foreground='w')]

maxRange = 0
plt.figure(0)
for i in range(len(legendNames)):
    maxRange = max(max(stepsArrays[i]), maxRange)
    plt.plot(stepsArrays[i], meansArrays[i], linewidth=1, label=legendNames[i])
plt.title("Plot of <f>", loc='left')
plt.xlim((0, maxRange))
plt.ylim((0.8, 1.2))
plt.plot((0, maxRange), (1, 1), 'g--')
plt.xlabel("$x_i$")
plt.ylabel("<f>")
plt.xticks(np.linspace(0, maxRange+70, 5))
plt.figlegend()
plt.savefig("./plots/5_1/mean.png", dpi=240, bbox_inches='tight')

plt.figure(1)
for i in range(len(legendNames)):
    plt.plot(stepsArrays[i], deltasArrays[i],
             linewidth=1, label=legendNames[i])

plt.xlim((0, maxRange))
plt.title("Plot of $\Delta$", loc='left')
plt.xlabel("$x_i$")
plt.ylabel("$\Delta$")
plt.xticks(np.linspace(0, maxRange+70, 5))
plt.plot((0, maxRange), (0, 0), 'g--')
plt.figlegend()
plt.savefig("./plots/5_1/delta.png", dpi=240, bbox_inches='tight')

plt.figure(2)
for i in range(len(legendNames)):
    plt.plot(stepsArrays[i],              np.abs(
        np.array(meansArrays[i]) - np.ones_like(meansArrays[i])), linewidth=1, label=legendNames[i])
plt.ylim((-0.01, 0.15))

plt.xlim((0, maxRange))
plt.title("Difference to real answer", loc='left')
plt.xlabel("$x_i$")
plt.ylabel("$|<f> - 1|$")
plt.xticks(np.linspace(0, maxRange+70, 5))
plt.plot((0, maxRange), (0, 0), 'g--')
plt.figlegend()
plt.savefig("./plots/5_1/difference.png", dpi=240, bbox_inches='tight')

plt.figure(3)
plt.title("$\Delta$ against actual difference", loc='left')
plt.xlim((0, maxRange / 2))
plt.xlabel("$x_i$")
plt.xticks(np.linspace(0, maxRange+70, 5))
plt.ylabel("$|<f> - 1|$ - $\Delta$")
for i in range(len(legendNames)):
    plt.plot(stepsArrays[i], np.abs(
        np.array(meansArrays[i]) - np.ones_like(meansArrays[i])) - np.array(deltasArrays[i]), linewidth=1, label=legendNames[i])
plt.figlegend()
plt.savefig("./plots/5_1/diff.png", dpi=240, bbox_inches='tight')
