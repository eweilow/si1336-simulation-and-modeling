from common import loadFile, plotData, loadRelaxationsFile, plotRelaxations, loadParametersFile

dimension, equivalentRun, realRun, desiredAccuracy, powerOfTwoMax, powerOfTwoWanted, relaxationsPerProlongation, relaxationsPerRestriction = loadParametersFile(
    "./data/1026_params_2.bin")

print(dimension, equivalentRun, realRun, desiredAccuracy, powerOfTwoMax, powerOfTwoWanted,
      relaxationsPerProlongation, relaxationsPerRestriction)

points, relaxations, accuracy, data = loadFile("./data/1026_exact_2.bin")
plotData("./plots/1026/a_exact_2.png", points, relaxations,
         accuracy, data, linearDimension=dimension, realTitle="Exact (150000 relaxations)", postfix=False)

points, relaxations, accuracy, data = loadFile("./data/1026_baseline_2.bin")
plotData("./plots/1026/a_baseline_2.png", points, relaxations,
         accuracy, data, linearDimension=dimension, realTitle="No multigrid")

points, relaxations, accuracy, data1 = loadFile(
    "./data/1026_premultigrid_2.bin")
plotData("./plots/1026/a_premultigrid_2.png", points, relaxations,
         accuracy, data1, linearDimension=dimension, realTitle="Directly after multigrid")

points, relaxations, accuracy, data2 = loadFile("./data/1026_multigrid_2.bin")
plotData("./plots/1026/a_multigrid_2.png", points, relaxations,
         accuracy, data2, linearDimension=dimension, realTitle="With multigrid")

plotData("./plots/1026/a_multigrid_diff_2.png", points, relaxations,
         accuracy, data1 - data2, linearDimension=dimension, realTitle="Difference before and after relaxations", postfix=False)


dimension, equivalentRun, realRun, desiredAccuracy, powerOfTwoMax, powerOfTwoWanted, relaxationsPerProlongation, relaxationsPerRestriction = loadParametersFile(
    "./data/1026_params_3.bin")

print(dimension, equivalentRun, realRun, desiredAccuracy, powerOfTwoMax, powerOfTwoWanted,
      relaxationsPerProlongation, relaxationsPerRestriction)

points, relaxations, accuracy, data = loadFile("./data/1026_exact_3.bin")
plotData("./plots/1026/a_exact_3.png", points, relaxations,
         accuracy, data, linearDimension=dimension, realTitle="Exact (150000 relaxations)", postfix=False)

points, relaxations, accuracy, data = loadFile("./data/1026_baseline_3.bin")
plotData("./plots/1026/a_baseline_3.png", points, relaxations,
         accuracy, data, linearDimension=dimension, realTitle="No multigrid")

points, relaxations, accuracy, data1 = loadFile(
    "./data/1026_premultigrid_3.bin")
plotData("./plots/1026/a_premultigrid_3.png", points, relaxations,
         accuracy, data1, linearDimension=dimension, realTitle="Directly after multigrid")

points, relaxations, accuracy, data2 = loadFile("./data/1026_multigrid_3.bin")
plotData("./plots/1026/a_multigrid_3.png", points, relaxations,
         accuracy, data2, linearDimension=dimension, realTitle="With multigrid")

plotData("./plots/1026/a_multigrid_diff_3.png", points, relaxations,
         accuracy, data1 - data2, linearDimension=dimension, realTitle="Difference before and after relaxations", postfix=False)


dimension, equivalentRun, realRun, desiredAccuracy, powerOfTwoMax, powerOfTwoWanted, relaxationsPerProlongation, relaxationsPerRestriction = loadParametersFile(
    "./data/1026_params_4.bin")

print(dimension, equivalentRun, realRun, desiredAccuracy, powerOfTwoMax, powerOfTwoWanted,
      relaxationsPerProlongation, relaxationsPerRestriction)

points, relaxations, accuracy, data = loadFile("./data/1026_exact_4.bin")
plotData("./plots/1026/a_exact_4.png", points, relaxations,
         accuracy, data, linearDimension=dimension, realTitle="Exact (150000 relaxations)", postfix=False)

points, relaxations, accuracy, data = loadFile("./data/1026_baseline_4.bin")
plotData("./plots/1026/a_baseline_4.png", points, relaxations,
         accuracy, data, linearDimension=dimension, realTitle="No multigrid")

points, relaxations, accuracy, data1 = loadFile(
    "./data/1026_premultigrid_4.bin")
plotData("./plots/1026/a_premultigrid_4.png", points, relaxations,
         accuracy, data1, linearDimension=dimension, realTitle="Directly after multigrid")

points, relaxations, accuracy, data2 = loadFile("./data/1026_multigrid_4.bin")
plotData("./plots/1026/a_multigrid_4.png", points, relaxations,
         accuracy, data2, linearDimension=dimension, realTitle="With multigrid")

plotData("./plots/1026/a_multigrid_diff_4.png", points, relaxations,
         accuracy, data1 - data2, linearDimension=dimension, realTitle="Difference before and after relaxations", postfix=False)
