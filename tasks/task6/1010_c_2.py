from common import loadFile, plotData

points, relaxations, accuracy, data = loadFile("./data/1010_c_2.bin")

plotData("./plots/1010/c_2.png", points, relaxations, accuracy, data)
