import matplotlib.pyplot as plt

from newSim import trafficSim


def run(prob):
    averageFlowRate, times, positions, velocities, distances, vehicles, image = trafficSim(
        200, 50, 0.2, prob, 2, True)

    plt.xlabel("Position")
    plt.ylabel("Time")
    plt.title("$p$ = {0:.2f} \n {1:.2f} Hz".format(prob, averageFlowRate))
    plt.imshow(image)


plt.figure()
plt.subplot(131)
run(0.2)
plt.subplot(132)
run(0.5)
plt.subplot(133)
run(0.8)
plt.tight_layout()
plt.savefig("./plots/4_4/sim1.png")
