
import matplotlib.pyplot as plt

from task_2_1 import run

plt.figure()
steps, xvals = run(0.91, 0.5, False)
plt.plot(steps, xvals)
steps, xvals = run(0.91, 0.5, True)
plt.plot(steps, xvals)
plt.title("r = 0.91")
plt.xlabel("n")
plt.ylabel("$x_n$")
plt.figlegend(('Not rounded', 'Rounded'))
plt.savefig("./plots/2_1/r091.png", dpi=120)

plt.figure()
steps, xvals = run(0.6, 0.5, False)
plt.plot(steps, xvals)
steps, xvals = run(0.6, 0.5, True)
plt.plot(steps, xvals)
plt.title("r = 0.6")
plt.xlabel("n")
plt.ylabel("$x_n$")
plt.figlegend(('Not rounded', 'Rounded'))
plt.savefig("./plots/2_1/r06.png", dpi=120)
