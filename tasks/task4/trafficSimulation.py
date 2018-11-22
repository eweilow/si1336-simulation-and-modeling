import numpy as np
import random


def createTrafficSimulation(
    # Simulation settings
    initialSpacing=1,
    initialVelocity=0,
    maxVelocity=2,
    velocityDecreaseProbability=0.5,

    # Simulation size
    simulationSteps=1000,
    cars=50,
    roadStretch=50
):

    def runSimulation():
        # State
        positions = []
        velocities = []

        carStates = []
        timeSteps = np.zeros(simulationSteps)
        flowRates = np.zeros(simulationSteps)
        densities = np.zeros(simulationSteps)

        for i in range(cars):
            positions.append(i*initialSpacing)
            velocities.append(initialVelocity)
            carStates.append((np.zeros(simulationSteps),
                              np.zeros(simulationSteps)))

        timeRange = 0
        for simulation in range(simulationSteps):
            allOutside = True
            allInsideStartingBoundary = False
            for i in range(cars):
                if positions[i] <= roadStretch:
                    allOutside = False
                if positions[i] <= cars * initialSpacing:
                    allInsideStartingBoundary = True
            if allOutside:
                break

            timeRange += 1

            flowRateSum = 0
            carsInBoundary = 0
            for i in range(cars):
                if positions[i] <= roadStretch:
                    carsInBoundary += 1
                    flowRateSum += velocities[i]

            if not allInsideStartingBoundary:
                currentFlowRate = flowRateSum / roadStretch
                currentDensity = carsInBoundary / roadStretch
                flowRates[simulation] = currentFlowRate
                densities[simulation] = currentDensity

            timeSteps[simulation] = simulation
            for i in range(cars):
                (P, V) = carStates[i]
                P[simulation] = positions[i]
                V[simulation] = velocities[i]

            for i in range(cars):
                if velocities[i] < maxVelocity:
                    velocities[i] += 1
            for i in range(cars-1):
                distanceToNext = positions[i+1] - positions[i]
                if(velocities[i] >= distanceToNext):
                    velocities[i] = distanceToNext - 1

            for i in range(cars):
                if random.random() < velocityDecreaseProbability:
                    if velocities[i] > 0:
                        velocities[i] -= 1

            for i in range(cars):
                positions[i] += velocities[i]
        return positions, velocities, timeSteps, carStates, flowRates, densities, timeRange

    def averageSimulations(count):
        summedFlowRates = np.zeros(simulationSteps)
        summedDensities = np.zeros(simulationSteps)
        for i in range(count):
            positions, velocities, timeSteps, carStates, flowRates, densities, timeRange = runSimulation()
            summedFlowRates += flowRates
            summedDensities += densities

        summedFlowRates /= count
        summedDensities /= count
        return summedFlowRates, summedDensities

    return (
        runSimulation,
        averageSimulations,
        roadStretch,
        cars
    )
