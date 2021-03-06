from common import loadFile, plotData, loadRelaxationsFile, plotRelaxations

points, relaxations, accuracy, data = loadFile("./data/1010_a_1.bin")

plotData("./plots/1010/a_1.png", points, relaxations, accuracy, data)
plotData("./plots/1010/a_1_eq.png", points,
         relaxations, accuracy, data, use3d=False)


gridSizes, relaxations = loadRelaxationsFile("./data/1010_a_relaxations.bin")
plotRelaxations("./plots/1010/a_1_dependency.png", gridSizes, relaxations)
