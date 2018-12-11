import matplotlib.pyplot as plt
import random
import math
import numpy as np


def trafficSim(simulationLength, roadLength, density, probabilityOfDecelleration, maxVelocity, computeImage):
    def createInitialPositions():
        return random.sample(
            range(roadLength), max(1, math.floor(density * roadLength)))

    def createInitialVelocities(count):
        velocities = []
        for i in range(count):
            velocities.append(maxVelocity)
        return velocities

    def createVehicles():
        currentPositions = createInitialPositions()
        count = len(currentPositions)
        currentVelocities = createInitialVelocities(count)
        vehicles = []
        for i in range(count):
            vehicles.append([i, currentPositions[i], currentVelocities[i], 0])
        return vehicles

    ID = 0
    POS = 1
    VEL = 2
    DIST = 3

    def sortVehicles(vehicles):
        return sorted(vehicles, key=lambda vehicle: vehicle[POS])

    def computeDistances(vehicles):
        for i in range(len(vehicles) - 1):
            vehicles[i][DIST] = vehicles[i+1][POS] - vehicles[i][POS]
        vehicles[-1][DIST] = roadLength + vehicles[0][POS] - vehicles[-1][POS]

    vehicles = createVehicles()

    times = []
    positions = []
    velocities = []
    distances = []
    image = []

    currentPositions = []
    currentVelocities = []
    currentDistances = []

    def storeImageData():
        nonlocal currentDistances, currentPositions, currentVelocities
        # For plot
        currentRow = []
        for x in range(roadLength):
            currentRow.append(0)

        for vehicle in vehicles:
            times.append(i)
            currentPositions.append(vehicle[POS])
            currentVelocities.append(vehicle[VEL])
            currentDistances.append(vehicle[DIST])
            currentRow[vehicle[POS]] = vehicle[ID]+1

        positions.append(currentPositions)
        velocities.append(currentVelocities)
        distances.append(currentDistances)
        currentPositions = []
        currentVelocities = []
        currentDistances = []

        image.append(currentRow)

    averageFlowRate = 0
    averageFlowRateSamples = 0
    for i in range(simulationLength):
        vehicles = sortVehicles(vehicles)
        computeDistances(vehicles)
        # print(vehicles)

        if(computeImage):
            storeImageData()

        # First rule - accelerate vehicles not at max velocity
        for vehicle in vehicles:
            if vehicle[VEL] < maxVelocity:
                vehicle[VEL] += 1

        # Second rule - slow down vehicles too close to another
        for vehicle in vehicles:
            if vehicle[DIST]-1 < vehicle[VEL]:
                vehicle[VEL] = max(0, vehicle[DIST] - 1)

        # Third rule - randomize decelleration
        for vehicle in vehicles:
            if random.random() < probabilityOfDecelleration and vehicle[VEL] > 0:
                vehicle[VEL] -= 1

        # Fourth rule - move vehicles
        for vehicle in vehicles:
            vehicle[POS] += vehicle[VEL]

        # Boundary condition
        for vehicle in vehicles:
            while vehicle[POS] >= roadLength:
                vehicle[POS] -= roadLength

        if i > simulationLength//2:
            currentVelocity = 0
            for vehicle in vehicles:
                currentVelocity += vehicle[VEL]
            averageFlowRate += currentVelocity / roadLength
            averageFlowRateSamples += 1

    #averageFlowRateSamples = 0
    # for sliced in velocities[2*len(velocities)//3:]:
    #    flowRate = 0
    #    for velocity in sliced:
    #        flowRate += velocity
    #    flowRate /= roadLength
#
    #    averageFlowRate += flowRate
    #    averageFlowRateSamples += 1
    #    # print(vehicles)
    averageFlowRate /= averageFlowRateSamples
    return averageFlowRate, times, positions, velocities, distances, vehicles, image


def computeForValues(simulationTime, roadLength):
    print("Running for sim time {0} on road length {1}".format(
        simulationTime, roadLength))
    averageCountPerDensity = 150
    densities = np.linspace(0, 1, 50)
    flowrates = []
    for density in densities:
        print(density)
        averagePerDensity = 0
        for i in range(averageCountPerDensity):
            averageFlowRate, times, positions, velocities, distances, vehicles, image = trafficSim(
                simulationTime, roadLength, density, 0.5, 2, False)
            averagePerDensity += averageFlowRate / averageCountPerDensity
        flowrates.append(averagePerDensity)
    return densities, flowrates
