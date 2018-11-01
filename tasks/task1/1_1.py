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
            self.dt, self.theta, self.dTheta
        )

        self.state["time"].append(self.t)
        self.state["theta"].append(self.theta)
        self.state["dTheta"].append(self.dTheta)
        self.state["energy"].append(self.energy)

    def __reset(self):
        self.t = 0.0
        self.theta = self.initialTheta
        self.dTheta = self.initialDTheta
        self.energy = 0

        self.state = {
            "time": [],
            "theta": [],
            "dTheta": [],
            "energy": []
        }

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
            interval=1000/30,
            blit=True,
            repeat=False
        )
        plt.show()


c = 9
m = 1
g = 9.81
L = g/c


def pendulumAcceleration(theta):
    return -c * np.sin(theta)


def harmonicEnergy(theta, dTheta):
    return 0.5*m*L**2*dTheta**2 + 0.5*m*g*L*theta**2


def pendulumEnergy(theta, dTheta):
    return 0.5*m*L**2*dTheta**2 + m*g*L*(1.-np.cos(theta))


def euler(dt, theta, dTheta):
    a = pendulumAcceleration(theta)
    theta += dTheta * dt
    dTheta += a * dt

    energy = pendulumEnergy(theta, dTheta)
    return theta, dTheta, energy


def eulerCromer(dt, theta, dTheta):
    a = pendulumAcceleration(theta)
    dTheta += a * dt
    theta += dTheta * dt

    energy = pendulumEnergy(theta, dTheta)
    return theta, dTheta, energy


def velocityVerlet(dt, theta, dTheta):
    a = pendulumAcceleration(theta)
    theta += dTheta * dt + 0.5 * a * dt*dt
    aNext = pendulumAcceleration(theta)
    dTheta += 0.5 * (aNext + a) * dt

    energy = pendulumEnergy(theta, dTheta)
    return theta, dTheta, energy


def rungeKutta(dt, theta, dTheta):
    a1 = pendulumAcceleration(theta) * dt
    b1 = dTheta*dt
    a2 = pendulumAcceleration(theta + b1/2) * dt
    b2 = (dTheta + a1/2)*dt
    a3 = pendulumAcceleration(theta + b2/2) * dt
    b3 = (dTheta + a2/2)*dt
    a4 = pendulumAcceleration(theta + b3) * dt
    b4 = (dTheta + a3)*dt

    dTheta += 1/6 * (a1 + 2*a2 + 2*a3 + a4)
    theta += 1/6 * (b1 + 2*b2 + 2*b3 + b4)

    energy = pendulumEnergy(theta, dTheta)
    return theta, dTheta, energy


sim = Simulation(rungeKutta, 1/60, 0.5, 5)
sim.animate(50, 1)
