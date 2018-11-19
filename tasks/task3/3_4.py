import numpy as np
import matplotlib.pyplot as plt


def readfile(name):
    f = open(name)

    i = 0
    vals = []
    for line in f:
        i += 1
        if i > 1000000:
            break
        lineData = line.rstrip().lstrip().split(" ")
        left = int(lineData[0])
        right = int(lineData[1])

        vals.append(left)
    f.close()
    return vals


def readmany():
    return readfile("./data/3_1/80_data.txt")


def readsingle():
    return readfile("./data/3_1/80_initial_data.txt")


vals = np.array(readmany())
singlevals = np.array(readsingle())
print("Processing...")


def mean(vals, squared=False):
    if squared:
        vals = np.square(vals)
    return np.sum(vals) / len(vals)


def getSquareFluctuations(vals, fromRange=0, toRange=1):
    fromIndex = np.int(len(vals) * fromRange)
    toIndex = np.int(len(vals) * toRange)
    print("from {0} to {1}".format(fromIndex, toIndex))
    indices = np.int_(
        np.ceil(np.linspace(len(vals)*fromRange, len(vals)*toRange, num=250)))

    squareFluctuations = []
    for index in indices:
        slice = vals[fromIndex:index]
        squareFluctuations.append(
            mean(slice, True) - mean(slice, False)**2)
    return indices, squareFluctuations


plt.figure()

singleIndices, singleSimFluctuation = getSquareFluctuations(
    singlevals, 0, 1)
lengthSingle = np.amax(singleIndices)
plt.plot(singleIndices, singleSimFluctuation)

singleIndices, singleSimFluctuation = getSquareFluctuations(
    singlevals, 1/4, 1)
plt.plot(singleIndices, singleSimFluctuation)

singleIndices, singleSimFluctuation = getSquareFluctuations(
    singlevals, 2/4, 1)
plt.plot(singleIndices, singleSimFluctuation)

singleIndices, singleSimFluctuation = getSquareFluctuations(
    singlevals, 3/4, 1)
plt.plot(singleIndices, singleSimFluctuation)

plt.plot([0, lengthSingle], [20, 20], linestyle='--')

plt.figlegend(('[0, 1]', '[0.25, 1]', '[0.5, 1]',
               '[0.75, 1]', '$\Delta n^2$ = 20'))
plt.title(
    '$\Delta n^2$ on range, single simulation (80 particles)', loc="left")
plt.xlabel('step')
plt.ylabel('$\Delta n^2$')
plt.savefig("./plots/3_4/single.png", dpi=160)

manyIndices, manySimsFluctuations = getSquareFluctuations(vals)
singleIndices, singleSimFluctuation = getSquareFluctuations(singlevals)

plt.figure()
plt.plot(manyIndices, manySimsFluctuations)
plt.plot([0, np.amax(manyIndices)], [20, 20], linestyle='--')
plt.title('Many simulations (80 particles)', loc="left")
plt.figlegend(('Computed $\Delta n^2$', '$\Delta n^2$ = 20'))
plt.xlabel('step')
plt.ylabel('$\Delta n^2$')
plt.savefig("./plots/3_4/many.png", dpi=160)


plt.figure()

plt.plot(manyIndices / np.max(manyIndices), manySimsFluctuations)
plt.plot(singleIndices / np.max(singleIndices), singleSimFluctuation)
plt.title('Comparing (80 particles)', loc="left")
plt.xlabel('normalized x')
plt.ylabel('$\Delta n^2$')
plt.figlegend(('Many simulations ({0})'.format(
    np.amax(manyIndices)), 'Single simulation ({0} steps)'.format(
    np.amax(singleIndices))))
plt.savefig("./plots/3_4/comparison.png", dpi=160)
