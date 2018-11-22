import matplotlib.pyplot as plt
import numpy as np
from task_2_1 import run
# need results from 2_1 first here...


def sum(r, x0, round):
    r, vals = run(r, x0, round)

    summed = 0
    for i in range(20, len(vals) - 1):
        summed += np.log(vals[i+1] / vals[i])
    return summed / (len(vals) - 20)


def runFor(x0, round=False):
    rvals = np.linspace(0.6, 1, 1000)
    sumvals = []
    for r in rvals:
        sumvals.append(sum(r, x0, round))

    plt.plot(rvals, sumvals)


plt.figure()
runFor(0.5, False)
runFor(0.5, True)
plt.figlegend(('Not rounded', 'Rounded'))
plt.xlabel("r")
plt.ylabel("$\lambda$")
plt.savefig("./plots/2_2/study.png")

legendLabels = []
plt.figure(figsize=[8, 3])
for x0 in np.linspace(0, 1, 50):
    runFor(x0, False)
    legendLabels.append("$x_0 = {0:.2f}$".format(x0))
plt.xlabel("r")
plt.ylabel("$\lambda$")
plt.figlegend(legendLabels, ncol=3)
plt.subplots_adjust(left=0.15, right=0.5, top=0.9, bottom=0.1)
plt.savefig("./plots/2_2/dependence.png", dpi=200, bbox_inches="tight")
