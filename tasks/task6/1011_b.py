from common import loadFile, plotData, loadRelaxationsFile, plotRelaxations

points, relaxations, accuracy, data = loadFile("./data/1011_b_1.bin")

plotData("./plots/1011/b_1.png", points, relaxations, accuracy, data)
plotData("./plots/1011/b_1_eq.png", points,
         relaxations, accuracy, data, use3d=False)


gridSizes, relaxations = loadRelaxationsFile("./data/1011_b_relaxations.bin")
plotRelaxations("./plots/1011/b_1_dependency.png", gridSizes, relaxations)
