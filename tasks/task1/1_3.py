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
    omega_0 = 3
    t = 0
    x = 1
    dx = 0

    def acc(x, dx):
        return -omega_0**2 * x - gamma * dx

    def E(x, dx):
        return 0.5 * omega_0**2 * x**2 + 0.5 * dx**2

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


pairs = []
pairs.append(run(0.5))
pairs.append(run(1))
pairs.append(run(2))
pairs.append(run(3))


def envelope(times, signal):
    try:
        peaks, _ = sp.find_peaks(signal)
        peakTimes = times[peaks]

        peakValues = signal[peaks]
        peakTimes = np.insert(peakTimes, 0, 0)
        peakValues = np.insert(peakValues, 0, signal[0])

        #plt.plot(peakTimes, peakValues, "x")

        def func(x, a, b):
            return a*np.exp(-b*x)

        (a, b), _ = curve_fit(func, peakTimes, peakValues, [1, 0.1])
        #plt.plot(times, func(times, a, b))

        relaxationTime = 1/b  # -b*x = -1 => x = 1/b
        return func(times, a, b), relaxationTime
    except:
        return times*0, 0


def output(selector, useEnvelope, ylabel, name):
    plt.figure()
    plt.xlim((0, 15))

    labels = []
    for (gamma, times, xvals, dxvals, energies) in pairs:
        labels.append("γ = {0:.1g}".format(gamma))
        if(useEnvelope):
            labels.append("γ = {0:.1g}".format(gamma))

    for pair in pairs:
        times = np.array(pair[1])
        data = np.array(selector(pair))
        plt.plot(times, data)

        if(useEnvelope):
            envelopeData, relaxationTime = envelope(times, data)
            plt.plot(times, envelopeData)

    plt.xlabel("t")
    plt.ylabel(ylabel)
    plt.figlegend(labels)
    plt.savefig(name, dpi=80)


output(
    lambda item: item[2], True, "θ(t)", "./plots/1_3/dampened_x.png")
output(lambda item: item[3], False, "θ'(t)", "./plots/1_3/dampened_dx.png")
output(lambda item: item[4], False, "E(t)", "./plots/1_3/dampened_E.png")


def study():
    gammaVals = np.linspace(0.1, 10, 50)

    relaxationTimes = []
    minVals = []

    plt.figure()
    for gamma in gammaVals:
        (_, times, xvals, dxvals, energies) = run(gamma)
        times = np.array(times)
        xvals = np.array(xvals)
        envelopedData, relaxationTime = envelope(times, xvals)

        plt.plot(times, xvals)
        plt.plot(times, envelopedData)
        relaxationTimes.append(np.amin(relaxationTime))
        minVals.append(np.min(xvals))
    plt.savefig("./plots/1_3/study_data.png", dpi=80)

    plt.figure()
    plt.plot(gammaVals, np.array(relaxationTimes))
    plt.ylabel("Relaxation time")
    plt.xlabel("γ")
    plt.savefig("./plots/1_3/study.png", dpi=120)

    plt.figure()
    plt.plot(gammaVals, np.array(minVals))
    plt.ylabel("min(x)")
    plt.xlabel("γ")
    plt.savefig("./plots/1_3/study_2.png", dpi=120)


study()
