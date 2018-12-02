
import matplotlib.pyplot as plt

n = 20

Lx = 5.6
Ly = 5.6

x = []
y = []
for i in range(0, n):
    x.append((Lx/5*((i % 5) + 0.5*(int(i/5)))) % Lx)
    y.append((Lx/5*0.87*(int(i/5))) % Ly)
    print("{0:.2f} {1:.2f}".format(x[i], y[i]))

plt.scatter(x, y)
plt.show()
