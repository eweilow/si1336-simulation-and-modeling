import matplotlib.pyplot as plt

from trafficSimulation import createTrafficSimulation

(runSimulation, averageSimulations, roadStretch,
 cars) = createTrafficSimulation(roadStretch=250, cars=50, velocityDecreaseProbability=0.2)

F, D = averageSimulations(750)
plt.figure()
plt.xlabel("Density")
plt.ylabel("Flow rate")
plt.scatter(D, F, s=2)
plt.savefig("./plots/4_1/flowrate.png")

positions, velocities, timeSteps, carStates, flowRates, densities, timeRange = runSimulation()
plt.figure()
plt.xlim((0, roadStretch))
plt.xlabel("Position")
plt.ylabel("Time")
for i in range(cars):
    (P, V) = carStates[i]
    plt.plot(P[:timeRange], timeSteps[:timeRange])
plt.savefig("./plots/4_1/solution.png")
