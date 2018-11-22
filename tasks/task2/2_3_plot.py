import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random

f = open("./data.txt", "r")

indices = []
radii = []
for line in f.readlines():
    (i, x0, y0, z0, r) = line.rstrip().split(" ")
    x0 = float(x0)
    y0 = float(y0)
    z0 = float(z0)
    r = float(r)
    indices.append(len(indices))
    radii.append(r)

plt.figure()
plt.hist(radii, 25, rwidth=0.75)
plt.ylabel("count")
plt.xlabel("average of $\sqrt{x^2 + y^2 + z^2}$ over $0 < t < 100$")
plt.savefig("./plots/2_3/histo.png", dpi=120)
