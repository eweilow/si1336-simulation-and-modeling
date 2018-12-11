import matplotlib.pyplot as plt

from newSim import trafficSim


def run(i):
    averageFlowRate, times, positions, velocities, distances, vehicles, image = trafficSim(
        100, 50, 0.2, 0.5, 2, True)

    plt.xlabel("Position")
    plt.ylabel("Time")
    plt.title("Simulation {0} \n {1:.2f} Hz".format(i, averageFlowRate))
    plt.imshow(image)


plt.figure()
plt.subplot(131)
run(1)
plt.subplot(132)
run(2)
plt.subplot(133)
run(3)
plt.tight_layout()
plt.savefig("./plots/4_1/sim1.png", dpi=160)
