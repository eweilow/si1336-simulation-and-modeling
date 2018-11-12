from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

c = 9
m = 1
g = 9.81
L = g / c


def harmonicAcceleration(theta):
    return -c * theta


def pendulumAcceleration(theta):
    return -c * np.sin(theta)


def harmonicEnergy(theta, dTheta):
    return 0.5 * m * L**2 * dTheta**2 + 0.5 * m * g * L * theta**2


def pendulumEnergy(theta, dTheta):
    return 0.5 * m * L**2 * dTheta**2 + m * g * L * (1. - np.cos(theta))


def velocityVerlet(A, E, dt, theta, dTheta):
    a = A(theta)
    theta += dTheta * dt + 0.5 * a * dt * dt
    aNext = A(theta)
    dTheta += 0.5 * (aNext + a) * dt

    energy = E(theta, dTheta)
    return theta, dTheta, energy


def findPeriod(A, E, dt, initialTheta, initialDTheta):
    time = 0
    theta = initialTheta
    dTheta = initialDTheta

    def iterateUntilZero():
        nonlocal time, theta, dTheta
        if A(theta) == 0 and abs(dTheta) < 1e-10 and abs(theta) < 1e-10:
            return
        currentSign = sign(theta)
        while(sign(theta) == currentSign):
            time += dt
            theta, dTheta, energy = velocityVerlet(A, E, dt, theta, dTheta)

    iterateUntilZero()
    startTime = time
    iterateUntilZero()
    iterateUntilZero()
    endTime = time

    period = endTime - startTime
    return period


initialValues = np.linspace(0.001, np.pi/2, 25)
harmonicPeriods = []
pendulumPeriods = []
perturbationPeriods = []
for value in initialValues:
    harmonicPeriods.append(findPeriod(harmonicAcceleration,
                                      harmonicEnergy, 0.001, value, 0))
    pendulumPeriods.append(findPeriod(pendulumAcceleration,
                                      pendulumEnergy, 0.001, value, 0))
    perturbationPeriods.append(
        2*np.pi * np.sqrt(1/c) * (1 + value**2/16 + 11*value**4/3072) + 173*value**6/737820)

plt.figure()
plt.plot(np.divide(initialValues, np.pi), np.array(harmonicPeriods))
plt.plot(np.divide(initialValues, np.pi), np.array(pendulumPeriods))
plt.plot(np.divide(initialValues, np.pi), np.array(perturbationPeriods))
plt.figlegend(('Harmonic oscillator', 'Pendulum',
               'Perturbation series (to power 6)'))
plt.xlabel("θ(0)/pi")
plt.ylabel("T (s)")
plt.savefig("./plots/1_2/period.png", dpi=120)
