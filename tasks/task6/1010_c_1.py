from common import loadFile, plotData

points, relaxations, accuracy, data = loadFile("./data/1010_c_1.bin")

plotData("./plots/1010/c_1.png", points, relaxations, accuracy, data)
plotData("./plots/1010/c_1_eq.png", points,
         relaxations, accuracy, data, use3d=False)
