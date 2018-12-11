#include "../common/relax.c"

double **finalGrid;
double guessPotentialAgainstExact(struct Grid *grid, unsigned long i, unsigned long j)
{
  return finalGrid[i][j];
}

struct Grid *createGrids(
    double linearDimension,
    unsigned long finalPowerOfTwo,
    double (*initialValue)(struct Grid *grid, unsigned long, unsigned long),
    double (*boundaryValue)(struct Grid *grid, unsigned long, unsigned long))
{
  struct Grid *grids;

  grids = (struct Grid *)malloc(sizeof(struct Grid) * (finalPowerOfTwo));

  for (unsigned long n = 0; n < finalPowerOfTwo; ++n)
  {
    unsigned long size = 2 << n;
    struct Grid grid = createGrid(linearDimension, size);
    setInitialValues(&grid, initialValue);
    setBoundaryConditions(&grid, boundaryValue);
    grids[n] = grid;
  }

  return grids;
}

// move from courser to finer
void doProlongate(struct Grid *from, struct Grid *into)
{
  if ((from->points - 1) * 2 != (into->points - 1))
  {
    printf("Expected to double points, didn't! (%d -> %d)\n", from->points, into->points);
    return;
  }

  into->relaxations = 0;
  for (unsigned long n = 1; n < into->points - 1; ++n)
  {
    for (unsigned long l = 1; l < into->points - 1; ++l)
    {
      unsigned long y = n % 2;
      unsigned long x = l % 2;

      unsigned int i = n / 2;
      unsigned int j = l / 2;
      if (y == x && x == 0)
      {
        into->currentGrid[n][l] = from->currentGrid[i][j];
      }
      else if (y == x && x == 1)
      {
        double topLeft = from->currentGrid[i][j];
        double bottomLeft = from->currentGrid[i + 1][j];
        double topRight = from->currentGrid[i][j + 1];
        double bottomRight = from->currentGrid[i + 1][j + 1];
        into->currentGrid[n][l] = 0.25 * (bottomRight + topRight + topLeft + bottomLeft);
      }
      else if (y == 1 && x == 0)
      {
        into->currentGrid[n][l] = 0.5 * (from->currentGrid[i][j] + from->currentGrid[i + 1][j]);
      }
      else if (x == 1 && y == 0)
      {
        into->currentGrid[n][l] = 0.5 * (from->currentGrid[i][j] + from->currentGrid[i][j + 1]);
      }
    }
  }
}

// move from finer to courser
void doRestrict(struct Grid *from, struct Grid *into)
{
  if ((from->points - 1) != (into->points - 1) * 2)
  {
    printf("Expected to halve points, didn't! (%d -> %d)\n", from->points, into->points);
    return;
  }

  into->relaxations = 0;
  for (unsigned long n = 1; n < into->points - 1; ++n)
  {
    for (unsigned long l = 1; l < into->points - 1; ++l)
    {
      unsigned long i = n * 2;
      unsigned long j = l * 2;

      double center = from->currentGrid[i][j];
      double nearestNeighbours = from->currentGrid[i + 1][j] + from->currentGrid[i - 1][j] + from->currentGrid[i][j - 1] + from->currentGrid[i][j + 1];
      double cornerNeighbours = from->currentGrid[i - 1][j - 1] + from->currentGrid[i + 1][j - 1] + from->currentGrid[i - 1][j + 1] + from->currentGrid[i + 1][j + 1];
      into->currentGrid[n][l] = (1 / 4.0) * center + (1 / 8.0) * nearestNeighbours + (1 / 16.0) * cornerNeighbours;
    }
  }
}

void multigrid(
    double linearDimension,
    double desiredAccuracy,
    unsigned long POWER_OF_TWO_MAX,
    unsigned long WANTED_POWER_OF_TWO,
    unsigned long RELAXATIONS_PER_PROLONGATION,
    unsigned long RELAXATIONS_PER_RESTRICTION,
    void (*relaxFn)(struct Grid *grid),
    double (*initialValue)(struct Grid *grid, unsigned long, unsigned long),
    double (*boundaryValue)(struct Grid *grid, unsigned long, unsigned long),
    double (*guessPotential)(struct Grid *grid, unsigned long, unsigned long))
{
  struct Grid *grids = createGrids(linearDimension, POWER_OF_TWO_MAX, initialValue, boundaryValue);
  //for (unsigned long n = 0; n < POWER_OF_TWO; ++n)
  //{
  //  printGrid(grids + n);
  //}

  unsigned long realRelaxationsRun = 0;
  double equivalentRelaxationsRun = 0.0;
  relaxFn(grids);
  equivalentRelaxationsRun += 1.0;

  for (unsigned long n = 0; n < POWER_OF_TWO_MAX - 1; ++n)
  {
    doProlongate(grids + n, grids + n + 1);
    equivalentRelaxationsRun /= 4.0;

    for (unsigned long i = 0; i < RELAXATIONS_PER_PROLONGATION; ++i)
    {
      relaxFn(grids + n + 1);
      equivalentRelaxationsRun += 1.0;
      realRelaxationsRun += 1;
    }
    //printGrid(grids + n);
  }
  for (unsigned long n = POWER_OF_TWO_MAX - 1; n >= WANTED_POWER_OF_TWO - 1; --n)
  {
    doRestrict(grids + n, grids + n - 1);
    equivalentRelaxationsRun *= 4.0;
    for (unsigned long i = 0; i < RELAXATIONS_PER_RESTRICTION; ++i)
    {
      relaxFn(grids + n - 1);
      equivalentRelaxationsRun += 1.0;
      realRelaxationsRun += 1;
    }
  }

  printf("\nRun %.4f equivalent relaxations (%d real)\n", equivalentRelaxationsRun, realRelaxationsRun);

  /* Necessary to compute accuracy */
  struct Grid finalGridForAccuracy = createGrid(linearDimension, 2 << (WANTED_POWER_OF_TWO - 1));
  setInitialValues(&finalGridForAccuracy, initialValue);
  setBoundaryConditions(&finalGridForAccuracy, boundaryValue);
  copyNextIntoCurrentGrid(&finalGridForAccuracy, (grids + (WANTED_POWER_OF_TWO - 1))->currentGrid, finalGridForAccuracy.currentGrid);
  for (unsigned long n = 0; n < 150000; ++n)
  {
    relaxFn(&finalGridForAccuracy);
  }
  finalGrid = finalGridForAccuracy.currentGrid;

  printf("\nGrid directly after multigrid method");
  computeAccuracy(grids + WANTED_POWER_OF_TWO - 1, guessPotentialAgainstExact);
  printGrid(grids + WANTED_POWER_OF_TWO - 1);

  printf("\nGrid for accuracy calculation");
  printGrid(&finalGridForAccuracy);

  /* Compute a baseline to compare with */
  struct Grid baselineGrid = createGrid(linearDimension, 2 << (WANTED_POWER_OF_TWO - 1));
  setInitialValues(&baselineGrid, initialValue);
  setBoundaryConditions(&baselineGrid, boundaryValue);
  computeAccuracy(&baselineGrid, guessPotential);
  do
  {
    relaxFn(&baselineGrid);
    computeAccuracy(&baselineGrid, guessPotentialAgainstExact);
  } while (baselineGrid.currentAccuracy > desiredAccuracy);
  printf("\nBaseline grid, without multigrid method");
  printGrid(&baselineGrid);
  //printAccuracy(&baselineGrid, guessPotentialAgainstExact);

  /* Compute the relaxed grid with initial values from prolongation/restriction */
  struct Grid grid = *(grids + (WANTED_POWER_OF_TWO - 1));
  grid.relaxations = 0;
  unsigned long steps = 0;
  do
  {
    relaxFn(&grid);
    computeAccuracy(&grid, guessPotentialAgainstExact);
  } while (grid.currentAccuracy > desiredAccuracy && (++steps) <= 1500000);
  printf("\nGrid solved after multigrid method");
  printGrid(&grid);
}