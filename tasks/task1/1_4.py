from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import scipy.signal as sp
from scipy.optimize import curve_fit


def velocityVerlet(A, dt, x, dx):
    a = A(x, dx)
    x += dx * dt + 0.5 * a * dt * dt
    aNext = A(x, dx)
    dx += 0.5 * (aNext + a) * dt

    return x, dx


def run(gamma):
    dt = 0.001
    sqrtgOverl = 3
    g = 9.81
    L = sqrtgOverl**2 / g

    x = np.pi / 2
    dx = 0

    gamma = 1
    t = 0

    def acc(x, dx):
        return -sqrtgOverl**2 * np.sin(x) - gamma * dx

    def E(x, dx):
        return g * L * (1. - np.cos(x)) + 0.5 * L**2 * dx**2

    times = []
    xvals = []
    dxvals = []
    energies = []

    def step():
        nonlocal x, dx, t, times, xvals, energies
        times.append(t)
        xvals.append(x)
        dxvals.append(dx)
        energies.append(E(x, dx))

        t += dt

        x, dx = velocityVerlet(acc, dt, x, dx)

    while t < 15:
        step()

    return (gamma, times, xvals, dxvals, energies)


(gamma, times, xvals, dxvals, energies) = run(1)

plt.figure()
plt.plot(dxvals, xvals)
plt.xlabel("θ'(t)")
plt.ylabel("θ(t)")
plt.savefig("./plots/1_4/study.png", dpi=120)
