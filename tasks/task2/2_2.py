import matplotlib.pyplot as plt
import numpy as np
from task_2_1 import run
# need results from 2_1 first here...


def sum(r):
    r, vals = run(0.8, False)

    summed = 0
    for i in range(20, len(vals) - 1):
        print(vals[i])
        summed += np.log(vals[i+1] / vals[i])
    return summed / (len(vals) - 20)


print(sum(0.8))
