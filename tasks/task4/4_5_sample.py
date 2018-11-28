import matplotlib.pyplot as plt
from treeSim import treeSimulation

iterate, getFireCatched, getGrid = treeSimulation(8, 0.1, 0.1)

N = 3
t = 0
plt.figure()
for i in range(N-1):
    for j in range(N+1):
        iterate()
        t += 1
        plt.subplot(N-1, N+1, i*(N+1) + j + 1)
        plt.title("t = {0}".format(t))
        plt.tight_layout()
        plt.imshow(getGrid())
        plt.clim(EMPTY, FIRE)

plt.tight_layout()
plt.savefig("./plots/4_5/sample.png", dpi=200)
