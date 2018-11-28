import matplotlib.pyplot as plt
import scipy.optimize as opt
from mpl_toolkits import mplot3d
import numpy as np
from treeSim import treeSimulation

file = open("./4_5_data.txt", "r")

maxi = 0
maxj = 0
maxg = 0
ming = 1
maxf = 0
minf = 1

entries = []
for line in file.readlines():
    [i, j, g, f, alpha] = [float(s) for s in line.split(" ")]
    i = int(i)
    j = int(j)

    entries.append((i, j, alpha))

    if i > maxi:
        maxi = i
    if j > maxj:
        maxj = j
    if g > maxg:
        maxg = g
    if g < ming:
        ming = g
    if f > maxf:
        maxf = f
    if f < minf:
        minf = f
print("{0:.8f}".format(maxg))


growthProbabilities = np.linspace(ming, maxg, maxi+1)
fireProbabilities = np.linspace(minf, maxf, maxj+1)
X, Y = np.meshgrid(growthProbabilities, fireProbabilities)
X = np.transpose(X)
Y = np.transpose(Y)
Counts = np.zeros_like(X)
Z = np.zeros_like(X)

print(maxi, maxj, Counts.shape)
for (i, j, alpha) in entries:
    #print(i, j)
    Z[i, j] += alpha
    Counts[i, j] += 1

Z /= Counts

Z = np.nan_to_num(Z)
#Z = np.transpose(Z)

print(Z)
print(Counts)

plt.figure()
fig, ax = plt.subplots()
CS = ax.contour(X, Y, Z, levels=np.linspace(-2, -1.2, 10),
                vmin=-3, vmax=3, linewidths=1)
ax.clabel(CS, inline=1, fontsize=8)
ax.set_title('$\\alpha$ as function of growth and lightning strike probability')
# plt.imshow(Z)
ax.set_xlabel('Growth probability')
ax.set_ylabel('Lightning strike probability')
plt.savefig("./plots/4_5/parameters.png", dpi=200)
