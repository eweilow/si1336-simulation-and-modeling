from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import scipy.signal as sp
from scipy.optimize import curve_fit

omega_0 = 3


def A(x):
    return -omega_0**2 * x


def KE(x, dx):
    return 0.5 * dx**2


def PE(x, dx):
    return 0.5 * omega_0**2 * x**2


def velocityVerlet(A, dt, x, dx):
    a = A(x)
    x += dx * dt + 0.5 * a * dt * dt
    aNext = A(x)
    dx += 0.5 * (aNext + a) * dt

    return x, dx


def leapfrog(A, dt, x, dx):
    dxn = dx + A(x) * dt
    x = x + dxn * dt

    return x, dxn


def run(gamma, integrator):
    dt = 0.25

    x = np.pi / 2
    dx = 0

    gamma = 1
    t = 0

    times = []
    xvals = []
    dxvals = []
    kenergies = []
    penergies = []

    def step():
        nonlocal x, dx, t, times, xvals, kenergies, penergies
        times.append(t)
        xvals.append(x)
        dxvals.append(dx)
        kenergies.append(KE(x, dx))
        penergies.append(PE(x, dx))

        t += dt

        x, dx = integrator(A, dt, x, dx)

    while t < 1500:
        step()

    return (gamma, times, xvals, dxvals, kenergies, penergies)


def plotRunningMean(times, E):
    def running_mean(x):
        currentSum = 0
        samples = 0

        arr = np.multiply(x, 0)

        for val in x:
            currentSum += val
            arr[samples] = currentSum / (samples + 1)
            samples += 1
        return arr

    plt.plot(times, running_mean(running_mean(E)))


plt.figure()
(gamma, times, xvals, dxvals, kenergies, penergies) = run(1, leapfrog)
leapfrogTimes = times
leapfrogX = xvals
leapfrogdX = dxvals
plotRunningMean(times, np.add(kenergies, penergies))

(gamma, times, xvals, dxvals, kenergies, penergies) = run(1, velocityVerlet)
verletTimes = times
verletX = xvals
verletdX = dxvals
plotRunningMean(times, np.add(kenergies, penergies))

plt.plot([0, 1500], [omega_0**2 * 0.5 * (np.pi / 2)
                     ** 2, omega_0**2 * 0.5 * (np.pi / 2)**2])

plt.xlabel("t")
plt.ylabel("E")
plt.title("Average of energy over time")
plt.figlegend(('Leapfrog', 'Velocity Verlet', 'Analytic solution'))
plt.savefig("./plots/1_5/study.png", dpi=120)

plt.figure()

analyticMotion = np.pi / 2 * np.cos(np.multiply(omega_0, leapfrogTimes))
analyticdMotion = -omega_0 * np.pi / 2 * \
    np.sin(np.multiply(omega_0, leapfrogTimes))
plt.plot(leapfrogX, leapfrogdX)
plt.plot(verletX, verletdX)
plt.plot(analyticMotion, analyticdMotion)
plt.xlabel("θ'(t)")
plt.ylabel("θ(t)")
plt.figlegend(('Leapfrog', 'Velocity Verlet', 'Analytic solution'))
plt.savefig("./plots/1_5/study2.png", dpi=120)
