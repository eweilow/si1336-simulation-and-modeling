from common import loadFile, plotData, loadRelaxationsFile, plotRelaxations, loadParametersFile

dimension, equivalentRun, realRun, desiredAccuracy, powerOfTwoMax, powerOfTwoWanted, relaxationsPerProlongation, relaxationsPerRestriction = loadParametersFile(
    "./data/1026_params_1.bin")

print(dimension, equivalentRun, realRun, desiredAccuracy, powerOfTwoMax, powerOfTwoWanted,
      relaxationsPerProlongation, relaxationsPerRestriction)

points, relaxations, accuracy, data = loadFile("./data/1026_exact_1.bin")
plotData("./plots/1026/a_exact_1.png", points, relaxations,
         accuracy, data, linearDimension=dimension, realTitle="Exact (150000 relaxations)", postfix=False)

points, relaxations, accuracy, data = loadFile("./data/1026_baseline_1.bin")
plotData("./plots/1026/a_baseline_1.png", points, relaxations,
         accuracy, data, linearDimension=dimension, realTitle="No multigrid")

points, relaxations, accuracy, data = loadFile(
    "./data/1026_premultigrid_1.bin")
plotData("./plots/1026/a_premultigrid_1.png", points, relaxations,
         accuracy, data, linearDimension=dimension, realTitle="Directly after multigrid")

points, relaxations, accuracy, data = loadFile("./data/1026_multigrid_1.bin")
plotData("./plots/1026/a_multigrid_1.png", points, relaxations,
         accuracy, data, linearDimension=dimension, realTitle="With multigrid")
