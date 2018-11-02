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
        while self.t < toTime:
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
        # axis = plt.subplot(xlim=(-1.2, 1.2), ylim=(-1.2, 1.2))
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


def harmonicAcceleration(theta):
    return -c * theta


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


def solve(A, E, initialTheta, initialDTheta, name):
    dt = 0.001
    timeLimit = 5

    title = "dt={0: .2g}, θ(0)/pi={1: .1g}, θ'(0)={2: .1g}".format(dt,
                                                                   initialTheta, initialDTheta)
    print("Solving " + title)
    sim = Simulation(
        lambda dt, theta, dTheta: velocityVerlet(
            A, E, dt, theta, dTheta),
        dt, initialTheta, initialDTheta)
    time, theta, dTheta, energy = sim.run(timeLimit)
    plt.figure()
    plt.plot(time, theta)
    plt.plot(time, dTheta)
    plt.plot(time, energy)
    plt.figlegend(('θ', 'θ\'', 'E'))
    plt.title(title, x=0.25)
    plt.savefig(name, dpi=80)


def plotPhaseSpace(A, E, timeLimit,  dt, initialTheta, initialDTheta):
    sim = Simulation(
        lambda dt, theta, dTheta: velocityVerlet(
            A, E, dt, theta, dTheta),
        dt, initialTheta, initialDTheta)
    time, theta, dTheta, energy = sim.run(timeLimit)
    plt.plot(time, theta)

    return time, theta


def compare(initialTheta, initialDTheta, name):
    dt = 0.001
    time = 25

    title = "dt={0: .2g}, θ(0)/pi={1: .1g}, θ'(0)={2: .1g}".format(dt,
                                                                   initialTheta, initialDTheta)
    print("Comparing " + title)
    plt.figure()
    plt.subplot(xlim=(0, time), ylim=(-1, 1))
    plotPhaseSpace(pendulumAcceleration, pendulumEnergy,
                   time, dt, initialTheta, initialDTheta)
    plotPhaseSpace(harmonicAcceleration, harmonicEnergy,
                   time, dt, initialTheta, initialDTheta)
    plt.title(title, x=0.25)
    plt.figlegend(('Pendulum', 'Harmonic Oscillator'))
    plt.ylabel('θ')
    plt.xlabel('t')
    plt.savefig(name, dpi=80)


def compareHarmonicNumericalToAnalytic(initialTheta, initialDTheta, name):
    dt = 0.001
    time = 1000

    title = "dt={0: .2g}, θ(0)/pi={1: .1g}, θ'(0)={2: .1g}".format(dt,
                                                                   initialTheta, initialDTheta)
    print("Comparing " + title)
    plt.figure()
    plt.subplot(xlim=(0, time), ylim=(1-0.005, 1 + 0.005))

    sim = Simulation(
        lambda dt, theta, dTheta: velocityVerlet(
            harmonicAcceleration, harmonicEnergy, dt, theta, dTheta),
        dt, initialTheta, initialDTheta)
    numericalTime, numericalTheta, dTheta, energy = sim.run(time)

    analyticSolution = np.cos(np.array(numericalTime)
                              * np.sqrt(c)) * initialTheta
    #plt.plot(numericalTime, analyticSolution)

    plt.plot(numericalTime, np.divide(
        np.abs(np.add(analyticSolution, 1.0)), np.abs(np.add(numericalTheta, 1.0))))
    plt.title(title, x=0.25)
    plt.figlegend(('(1+|Analytic|)/(1+|Numerical|)',))
    plt.xlabel('t')
    plt.savefig(name, dpi=80)


def rollingMean(A, E, name, dt, R):
    initialTheta = 0.5
    initialDTheta = 0
    timeLimit = 1000

    meanPeriod = 50

    title = "dt={0: .2g}, θ(0)/pi={1: .1g}, θ'(0)={2: .1g}".format(dt,
                                                                   initialTheta, initialDTheta)

    N = np.int_(ceil(meanPeriod / dt))
    print("Running rollingMean, N={0}, {1}".format(N, title))

    plt.figure()
    plt.subplot(xlim=(0, timeLimit - N * dt), ylim=(-R, R))

    def running_mean(x, N):
        # Thanks to https://stackoverflow.com/a/13732668
        return np.convolve(x, np.ones((N, )) / N)[(N - 1):]

    def single(integrator):
        sim = Simulation(
            lambda dt, theta, dTheta: integrator(
                pendulumAcceleration, pendulumEnergy, dt, theta, dTheta),
            dt, initialTheta * np.pi, initialDTheta * np.pi)
        time, theta, dTheta, energy = sim.run(timeLimit)
        averageEnergy = running_mean(energy, N)

        plt.plot(time[:-N],
                 np.log(averageEnergy[:-N] / averageEnergy[0]))

    single(euler)
    single(eulerCromer)
    single(velocityVerlet)
    single(rungeKutta)
    plt.ticklabel_format(style='sci', scilimits=(0, 0))
    plt.title(title, x=0.4)
    plt.figlegend(('Euler', 'Euler Cromer', 'Velocity Verlet', 'Runge Kutta'))
    plt.ylabel('log(relative energy)')
    plt.xlabel('t')
    plt.savefig(name, dpi=80)


solve(pendulumAcceleration, pendulumEnergy, 0.1, 0, "sol_pendulum_1.png")
solve(pendulumAcceleration, pendulumEnergy, 0.3, 0, "sol_pendulum_2.png")
solve(pendulumAcceleration, pendulumEnergy, 0.5, 0, "sol_pendulum_3.png")

solve(harmonicAcceleration, harmonicEnergy, 0.1, 0, "sol_harmonic_1.png")
solve(harmonicAcceleration, harmonicEnergy, 0.3, 0, "sol_harmonic_2.png")
solve(harmonicAcceleration, harmonicEnergy, 0.5, 0, "sol_harmonic_3.png")

compare(0.1, 0, "comparison_1.png")
compare(0.3, 0, "comparison_2.png")
compare(0.5, 0, "comparison_3.png")

compareHarmonicNumericalToAnalytic(0.1, 0, "comparison_numanalytic_1.png")
compareHarmonicNumericalToAnalytic(0.3, 0, "comparison_numanalytic_2.png")
compareHarmonicNumericalToAnalytic(0.5, 0, "comparison_numanalytic_3.png")

rollingMean(pendulumAcceleration, pendulumEnergy,
            "rollingMean_1.png", 0.1, 0.025)
# rollingMean(pendulumAcceleration, pendulumEnergy,
#            "rollingMean_2.png", 0.01, 0.000005)
# rollingMean(pendulumAcceleration, pendulumEnergy,
#            "rollingMean_3.png", 0.001, 0.000001)

rollingMean(harmonicAcceleration, harmonicEnergy,
            "rollingMean_harmonic_1.png", 0.1, 0.025)
# rollingMean(harmonicAcceleration, harmonicEnergy,
#            "rollingMean_harmonic_2.png", 0.01, 0.000005)
# rollingMean(harmonicAcceleration, harmonicEnergy,
#            "rollingMean_harmonic_3.png", 0.001, 0.000001)

# def runFor(totalRuns, currentRun, timeLimit, dt, initialTheta, initialDTheta):
#     axis = plt.subplot(
#         2,
#         totalRuns,
#         currentRun,
#         xlim=(0, timeLimit),
#         ylim=(-np.pi, np.pi),
#         title="dt={0:.2g}, θ(0)/pi={0:.1g}, θ'(0)={1:.1g}".format(
#             dt, initialTheta / np.pi, initialDTheta))
#     axis2 = plt.subplot(
#         2,
#         totalRuns,
#         totalRuns + currentRun,
#         xlim=(0, timeLimit),
#         ylim=(0.7, 1.3))
#
#     def running_mean(x, N):
#         # Thanks to https://stackoverflow.com/a/13732668
#         return np.convolve(x, np.ones((N, )) / N)[(N - 1):]
#
#     def runSingle(integrator):
#         sim = Simulation(
#             lambda dt, theta, dTheta: integrator(
#                 pendulumAcceleration, pendulumEnergy, dt, theta, dTheta),
#             dt, initialTheta, initialDTheta)
#         time, theta, dTheta, energy = sim.run(timeLimit)
#
#         averageEnergy = running_mean(energy, 100)
#
#         axis.plot(time, theta)
#         axis2.plot(time[:-100], averageEnergy[:-100] / averageEnergy[0])
#
#     runSingle(euler)
#     runSingle(eulerCromer)
#     runSingle(velocityVerlet)
#     runSingle(rungeKutta)
#
#
# runFor(6, 1, 1500, 0.1, 0.1 * np.pi, 0)
# runFor(6, 2, 1500, 0.1, 0.3 * np.pi, 0)
# runFor(6, 3, 1500, 0.1, 0.5 * np.pi, 0)
# runFor(6, 4, 150, 0.01, 0.1 * np.pi, 0)
# runFor(6, 5, 150, 0.01, 0.3 * np.pi, 0)
# runFor(6, 6, 150, 0.01, 0.5 * np.pi, 0)
#
# plt.figlegend(('Euler', 'Euler Cromer', 'Velocity Verlet', 'Runge Kutta'))
# plt.show()
