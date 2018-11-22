import matplotlib.pyplot as plt
import random
import math
import numpy as np


def trafficSim(simulationLength, roadLength, density, probabilityOfDecelleration, maxVelocity):
    def createInitialPositions():
        return random.sample(
            range(roadLength), math.floor(density * roadLength))

    def createInitialVelocities(count):
        velocities = []
        for i in range(count):
            velocities.append(maxVelocity)
        return velocities

    def createVehicles():
        positions = createInitialPositions()
        count = len(positions)
        velocities = createInitialVelocities(count)
        vehicles = []
        for i in range(count):
            vehicles.append([i, positions[i], velocities[i], 0])
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
    image = []

    def storeImageData():
        # For plot
        currentRow = []
        for x in range(roadLength):
            currentRow.append(0)

        for vehicle in vehicles:
            times.append(i)
            positions.append(vehicle[POS])
            currentRow[vehicle[POS]] = vehicle[ID]+1
        image.append(currentRow)

    for i in range(simulationLength):
        vehicles = sortVehicles(vehicles)
        computeDistances(vehicles)
        # print(vehicles)

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

        # print(vehicles)
    return times, positions, vehicles, image


times, positions, vehicles, image = trafficSim(100, 50, 0.8, 0.5, 2)

plt.figure()
plt.xlabel("Position")
plt.ylabel("Time")
plt.imshow(image)
plt.show()
