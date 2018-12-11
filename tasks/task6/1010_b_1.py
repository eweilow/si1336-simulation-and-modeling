from common import loadFile, plotData

points, relaxations, accuracy, data = loadFile("./data/1010_b_1.bin")

plotData("./plots/1010/b_1.png", points, relaxations, accuracy, data)
