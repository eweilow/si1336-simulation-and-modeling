
import matplotlib.pyplot as plt

from task_2_1 import run

plt.figure()
steps, xvals = run(0.91, 0.5, False)
plt.plot(steps, xvals)
steps, xvals = run(0.91, 0.5, True)
plt.plot(steps, xvals)
plt.figlegend(('Not rounded', 'Rounded'))
plt.show()

plt.figure()
steps, xvals = run(0.6, 0.5, False)
plt.plot(steps, xvals)
steps, xvals = run(0.6, 0.5, True)
plt.plot(steps, xvals)
plt.figlegend(('Not rounded', 'Rounded'))
plt.show()
