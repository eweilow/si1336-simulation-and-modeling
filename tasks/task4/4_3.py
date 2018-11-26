import matplotlib.pyplot as plt

from newSim import trafficSim


def run(vmax):
    averageFlowRate, times, positions, velocities, distances, vehicles, image = trafficSim(
        200, 50, 0.2, 0.5, vmax, True)

    plt.xlabel("Position")
    plt.ylabel("Time")
    plt.title("$v_{{max}}$ = {0} \n {1:.2f} Hz".format(vmax, averageFlowRate))
    plt.imshow(image)


plt.figure()
plt.subplot(131)
run(1)
plt.subplot(132)
run(2)
plt.subplot(133)
run(5)
plt.tight_layout()
plt.savefig("./plots/4_3/sim1.png")
