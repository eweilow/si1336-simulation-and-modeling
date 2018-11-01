from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


class Simulation():
    def __init__(self, integrator, dt, initialTheta, initialDTheta):
        self.dt = dt
        self.integrator = integrator
        self.initialTheta = initialTheta
        self.initialDTheta = initialDTheta

        self.__reset()

    def integrate(self):
        self.t += self.dt

        self.theta, self.dTheta, self.energy = self.integrator(
            self.dt, self.theta, self.dTheta)

    def __reset(self):
        self.t = 0.0
        self.theta = self.initialTheta
        self.dTheta = self.initialDTheta
        self.energy = 0

        self.state = {"time": [], "theta": [], "dTheta": [], "energy": []}

    def run(self, toTime, plotSteps=10000):
        totalStep = np.int_(ceil((toTime / self.dt) / plotSteps))
        print("Running a simulation with {0} steps".format(totalStep))
        while self.t < (toTime - self.dt * totalStep):
            for _ in range(totalStep):
                self.integrate()

            self.state["time"].append(self.t)
            self.state["theta"].append(self.theta)
            self.state["dTheta"].append(self.dTheta)
            self.state["energy"].append(self.energy)

        return self.state["time"], self.state["theta"], self.state[
            "dTheta"], self.state["energy"]

    def animate(self, toTime, stepsPerFrame=5):
        self.__reset()

        fig = plt.figure()
        #axis = plt.subplot(xlim=(-1.2, 1.2), ylim=(-1.2, 1.2))
        axis = plt.subplot(xlim=(0, toTime), ylim=(-np.pi, np.pi))
        pendulum_line, = axis.plot([], [], lw=4)

        def init():
            pendulum_line.set_data([], [])
            return pendulum_line,

        def frame(frameNumber):
            for _ in range(stepsPerFrame):
                self.integrate()

            x = np.array([0, np.sin(self.theta)])
            y = np.array([0, -np.cos(self.theta)])
            pendulum_line.set_data(self.state["time"], self.state["theta"])
            return pendulum_line,

        anim = animation.FuncAnimation(
            fig,
            frame,
            init_func=init,
            frames=round(toTime / self.dt) // stepsPerFrame,
            interval=1000 / 30,
            blit=True,
            repeat=False)
        plt.show()


c = 9
m = 1
g = 9.81
L = g / c


def pendulumAcceleration(theta):
    return -c * np.sin(theta)


def harmonicEnergy(theta, dTheta):
    return 0.5 * m * L**2 * dTheta**2 + 0.5 * m * g * L * theta**2


def pendulumEnergy(theta, dTheta):
    return 0.5 * m * L**2 * dTheta**2 + m * g * L * (1. - np.cos(theta))


def euler(A, E, dt, theta, dTheta):
    a = A(theta)
    theta += dTheta * dt
    dTheta += a * dt

    energy = E(theta, dTheta)
    return theta, dTheta, energy


def eulerCromer(A, E, dt, theta, dTheta):
    a = A(theta)
    dTheta += a * dt
    theta += dTheta * dt

    energy = E(theta, dTheta)
    return theta, dTheta, energy


def velocityVerlet(A, E, dt, theta, dTheta):
    a = A(theta)
    theta += dTheta * dt + 0.5 * a * dt * dt
    aNext = A(theta)
    dTheta += 0.5 * (aNext + a) * dt

    energy = E(theta, dTheta)
    return theta, dTheta, energy


def rungeKutta(A, E, dt, theta, dTheta):
    a1 = A(theta) * dt
    b1 = dTheta * dt
    a2 = A(theta + b1 / 2) * dt
    b2 = (dTheta + a1 / 2) * dt
    a3 = A(theta + b2 / 2) * dt
    b3 = (dTheta + a2 / 2) * dt
    a4 = A(theta + b3) * dt
    b4 = (dTheta + a3) * dt

    dTheta += 1 / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
    theta += 1 / 6 * (b1 + 2 * b2 + 2 * b3 + b4)

    energy = E(theta, dTheta)
    return theta, dTheta, energy


def runFor(totalRuns, currentRun, timeLimit, dt, initialTheta, initialDTheta):
    axis = plt.subplot(
        2,
        totalRuns,
        currentRun,
        xlim=(0, timeLimit),
        ylim=(-np.pi, np.pi),
        title="dt={0:.2g}, θ(0)/pi={0:.1g}, θ'(0)={1:.1g}".format(
            dt, initialTheta / np.pi, initialDTheta))
    axis2 = plt.subplot(
        2,
        totalRuns,
        totalRuns + currentRun,
        xlim=(0, timeLimit),
        ylim=(0.7, 1.3))

    def running_mean(x, N):
        # Thanks to https://stackoverflow.com/a/13732668
        return np.convolve(x, np.ones((N, )) / N)[(N - 1):]

    def runSingle(integrator):
        sim = Simulation(
            lambda dt, theta, dTheta: integrator(pendulumAcceleration, pendulumEnergy, dt, theta, dTheta),
            dt, initialTheta, initialDTheta)
        time, theta, dTheta, energy = sim.run(timeLimit)

        averageEnergy = running_mean(energy, 100)

        axis.plot(time, theta)
        axis2.plot(time[:-100], averageEnergy[:-100] / averageEnergy[0])

    runSingle(euler)
    runSingle(eulerCromer)
    runSingle(velocityVerlet)
    runSingle(rungeKutta)


runFor(6, 1, 1500, 0.1, 0.1 * np.pi, 0)
runFor(6, 2, 1500, 0.1, 0.3 * np.pi, 0)
runFor(6, 3, 1500, 0.1, 0.5 * np.pi, 0)
runFor(6, 4, 150, 0.01, 0.1 * np.pi, 0)
runFor(6, 5, 150, 0.01, 0.3 * np.pi, 0)
runFor(6, 6, 150, 0.01, 0.5 * np.pi, 0)

plt.figlegend(('Euler', 'Euler Cromer', 'Velocity Verlet', 'Runge Kutta'))
plt.show()
