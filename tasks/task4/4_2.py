import matplotlib.pyplot as plt

from newSim import computeForValues

plt.figure()
plt.xlabel("Density")
plt.ylabel("Flow rate per length")
D, F = computeForValues(100, 5)
plt.plot(D, F)
D, F = computeForValues(100, 10)
plt.plot(D, F)
D, F = computeForValues(100, 50)
plt.plot(D, F)
D, F = computeForValues(100, 250)
plt.plot(D, F)
D, F = computeForValues(100, 500)
plt.plot(D, F)
D, F = computeForValues(100, 1000)
plt.plot(D, F)
plt.figlegend(('L = 5', 'L = 10', 'L = 50', 'L = 250', 'L = 500', 'L = 5000'))
plt.savefig("./plots/4_2/density.png")
