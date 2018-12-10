double **desiredGrid;
double maxValue;

double guessPotential(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 1000.0;
}

double guessPotentialAgainstExact(struct Grid *grid, unsigned long i, unsigned long j)
{
  return desiredGrid[i][j];
}

void runRelaxationsAgainstHighPrecision(char *name,
                                        double linearDimension,
                                        unsigned long points,
                                        double wantedPrecision,
                                        void (*relaxFn)(struct Grid *grid),
                                        double (*initialValue)(struct Grid *grid, unsigned long, unsigned long),
                                        double (*boundaryValue)(struct Grid *grid, unsigned long, unsigned long))
{
  desiredGrid = allocateGridPoints(points);

  runRelaxationsUntilAccuracy(
      NULL,
      linearDimension,
      points,
      wantedPrecision,
      relaxFn,
      initialValue,
      boundaryValue,
      &guessPotential,
      desiredGrid);

  runRelaxationsUntilAccuracy(
      "../../data/1010_c_1.bin",
      linearDimension,
      points,
      wantedPrecision,
      relaxFn,
      initialValue,
      boundaryValue,
      &guessPotentialAgainstExact,
      NULL);

  freeGridPoints(desiredGrid, points);
}