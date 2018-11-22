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


def getAverages(vals, fromRange=0, toRange=1):
    fromIndex = np.int(len(vals) * fromRange)
    toIndex = np.int(len(vals) * toRange)
    print("from {0} to {1}".format(fromIndex, toIndex))
    indices = np.int_(
        np.ceil(np.linspace(len(vals)*fromRange, len(vals)*toRange, num=250)))

    averages = []
    for index in indices:
        slice = vals[fromIndex:index]
        averages.append(
            mean(slice, False))
    return indices, averages


plt.figure()

singleIndices, singleSimAverage = getAverages(
    singlevals, 0, 1)
plt.plot(singleIndices / np.max(singleIndices), singleSimAverage)

singleIndices, singleSimAverage = getAverages(
    singlevals, 1/4, 1)
plt.plot(singleIndices / np.max(singleIndices), singleSimAverage)

singleIndices, singleSimAverage = getAverages(
    singlevals, 2/4, 1)
plt.plot(singleIndices / np.max(singleIndices), singleSimAverage)

singleIndices, singleSimAverage = getAverages(
    singlevals, 3/4, 1)
plt.plot(singleIndices / np.max(singleIndices), singleSimAverage)

plt.plot([0, 1], [40, 40], linestyle='--')

plt.figlegend(('[0, 1]', '[0.25, 1]', '[0.5, 1]',
               '[0.75, 1]', '$<n>$ = 40'))
plt.title(
    '$<n>$ on range, single simulation (80 particles)', loc="left")
plt.xlabel('normalized step')
plt.ylabel('$<n>$')
plt.savefig("./plots/3_5/single.png", dpi=160)

manyIndices, manySimsAverages = getAverages(vals)
singleIndices, singleSimAverage = getAverages(singlevals)

plt.figure()
plt.plot(manyIndices / np.max(manyIndices), manySimsAverages)
plt.plot([0, 1], [40, 40], linestyle='--')
plt.title('Many simulations (80 particles)', loc="left")
plt.figlegend(('Computed $<n>$', '$<n>$ = 40'))
plt.xlabel('normalized step')
plt.ylabel('$<n>$')
plt.savefig("./plots/3_5/many.png", dpi=160)


plt.figure()

plt.plot(manyIndices / np.max(manyIndices), manySimsAverages)
plt.plot(singleIndices / np.max(singleIndices), singleSimAverage)
plt.title('Comparing (80 particles)', loc="left")
plt.xlabel('normalized x')
plt.ylabel('$<n>$')
plt.figlegend(('Many simulations', 'Single simulation'))
plt.savefig("./plots/3_5/comparison.png", dpi=160)
