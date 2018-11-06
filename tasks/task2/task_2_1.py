
import matplotlib.pyplot as plt


def run(r, x0, doRound=False):
    steps = range(200)
    xvals = []
    x = x0

    for _ in steps:
        xvals.append(x)
        x = 4 * r * x * (1 - x)
        if doRound:
            x = round(x, 6)

    return steps, xvals
