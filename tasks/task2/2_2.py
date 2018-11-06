import matplotlib.pyplot as plt
import numpy as np
from task_2_1 import run
# need results from 2_1 first here...


def sum(r, x0, round):
    r, vals = run(r, 0.5, round)

    summed = 0
    for i in range(20, len(vals) - 1):
        summed += np.log(vals[i+1] / vals[i])
    return summed / (len(vals) - 20)


def runFor(x0, round=False):
    rvals = np.linspace(0.76, 1, 1000)
    sumvals = []
    for r in rvals:
        sumvals.append(sum(r, x0, round))

    plt.plot(rvals, sumvals)


plt.figure()
runFor(0.5, True)
runFor(0.5, False)
plt.show()
