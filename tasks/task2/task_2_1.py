
import matplotlib.pyplot as plt


def run(r, doRound=False):
    steps = range(200)
    xvals = []
    x = 0.5

    for _ in steps:
        xvals.append(x)
        x = 4 * r * x * (1 - x)
        if doRound:
            x = round(x, 6)

    return steps, xvals


# plt.figure()
#steps, xvals = run(0.91, False)
#plt.plot(steps, xvals)
#steps, xvals = run(0.91, True)
#plt.plot(steps, xvals)
#plt.figlegend(('Not rounded', 'Rounded'))
# plt.show()
#
# plt.figure()
#steps, xvals = run(0.6, False)
#plt.plot(steps, xvals)
#steps, xvals = run(0.6, True)
#plt.plot(steps, xvals)
#plt.figlegend(('Not rounded', 'Rounded'))
# plt.show()
#
