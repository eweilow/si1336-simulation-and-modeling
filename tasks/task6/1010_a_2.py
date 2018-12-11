from common import loadFile, plotData

points, relaxations, accuracy, data = loadFile("./data/1010_a_2.bin")

plotData("./plots/1010/a_2.png", points, relaxations, accuracy, data)
