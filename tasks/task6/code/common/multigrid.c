#include "../common/relax.c"

void subdivideGrid(
    struct Grid *grid,
    double (*boundaryValue)(struct Grid *grid, unsigned long, unsigned long),
    double (*guessPotential)(struct Grid *grid, unsigned long, unsigned long))
{
  struct Grid newGrid = createGrid(grid->linearDimension, (grid->points - 1) * 2);
  setBoundaryConditions(&newGrid, boundaryValue);

  /*for (unsigned long n = 1; n < newGrid.points - 1; ++n)
  {
    for (unsigned long l = 1; l < newGrid.points - 1; ++l)
    {
      char buf[10];
      int len = sprintf(buf, "(%d,%d)", l / 2, n / 2);
      printf("%*s", 6, buf, len);
    }
    printf("\n");
  }*/

  for (unsigned long n = 1; n < newGrid.points - 1; ++n)
  {
    for (unsigned long l = 1; l < newGrid.points - 1; ++l)
    {
      unsigned long y = n % 2;
      unsigned long x = l % 2;
      /*if (y == x && x == 0)
      {
        char buf[10];
        int len = sprintf(buf, "(%d,%d)", l / 2, n / 2);
        printf("%*s", 6, buf, len);
      }
      else
      {

        printf("%*s", 6, y == x ? "x " : (y == 1 ? "| " : "- "));
      }*/

      unsigned int i = n / 2;
      unsigned int j = l / 2;
      if (y == x && x == 0)
      {
        newGrid.currentGrid[n][l] = grid->currentGrid[i][j];
      }
      else if (y == x && x == 1)
      {
        //newGrid.currentGrid[n][l] = 0.25 * (grid->currentGrid[i][j] + grid->currentGrid[i + 1][j] + grid->currentGrid[i][j] + grid->currentGrid[i][j + 1]);
        double topLeft = grid->currentGrid[i][j];
        double bottomLeft = grid->currentGrid[i + 1][j];
        double topRight = grid->currentGrid[i][j + 1];
        double bottomRight = grid->currentGrid[i + 1][j + 1];
        newGrid.currentGrid[n][l] = 0.25 * (bottomRight + topRight + topLeft + bottomLeft);
      }
      else if (y == 1 && x == 0)
      {
        newGrid.currentGrid[n][l] = 0.5 * (grid->currentGrid[i][j] + grid->currentGrid[i + 1][j]);
      }
      else if (x == 1 && y == 0)
      {
        newGrid.currentGrid[n][l] = 0.5 * (grid->currentGrid[i][j] + grid->currentGrid[i][j + 1]);
      }
    }
    //printf("\n");
  }

  freeGrid(grid);
  *grid = newGrid;
  computeAccuracy(grid, guessPotential);
}

double **finalGrid;

double guessPotentialAgainstExact(struct Grid *grid, unsigned long i, unsigned long j)
{
  return finalGrid[i][j];
}

#define RELAXATIONS_PER_SUBDIVIDE 1

void prolongate(struct Grid *from, struct Grid *into)
{
  if ((from->points - 1) * 2 != (into->points - 1))
  {
    printf("Expected to double points, didn't!");
    return;
  }
}

void multigrid(
    double linearDimension,
    double desiredAccuracy,
    void (*relaxFn)(struct Grid *grid),
    double (*initialValue)(struct Grid *grid, unsigned long, unsigned long),
    double (*boundaryValue)(struct Grid *grid, unsigned long, unsigned long),
    double (*guessPotential)(struct Grid *grid, unsigned long, unsigned long))
{
  const unsigned long finalPowerOftwo = 3;

  struct Grid finalGridBaseline = createGrid(linearDimension, 2 << finalPowerOftwo);
  setInitialValues(&finalGridBaseline, initialValue);
  setBoundaryConditions(&finalGridBaseline, boundaryValue);
  for (unsigned long n = 0; n < 150000; ++n)
  {
    relaxFn(&finalGridBaseline);
  }

  finalGrid = finalGridBaseline.currentGrid;

  struct Grid grid = createGrid(linearDimension, 2);
  setInitialValues(&grid, initialValue);
  setBoundaryConditions(&grid, boundaryValue);

  printf("\nInitial grid:");
  relaxFn(&grid);
  computeAccuracy(&grid, guessPotential);
  printGrid(&grid);

  for (unsigned long n = 1; n <= finalPowerOftwo; ++n)
  {
    subdivideGrid(&grid, boundaryValue, guessPotential);
    for (unsigned long r = 0; r < RELAXATIONS_PER_SUBDIVIDE; ++r)
    {
      relaxFn(&grid);
    }
    computeAccuracy(&grid, guessPotential);
    printf("\nSubdivided:");
    printGrid(&grid);
  }

  unsigned long steps = 0;
  while (grid.currentAccuracy > desiredAccuracy && (++steps) < 150000)
  {
    relaxFn(&grid);
    computeAccuracy(&grid, guessPotentialAgainstExact);
  }
  printf("\nGrid after multigrid:");
  printGrid(&grid);

  struct Grid gridBaseline = createGrid(linearDimension, 2 << finalPowerOftwo);
  setInitialValues(&gridBaseline, initialValue);
  setBoundaryConditions(&gridBaseline, boundaryValue);
  computeAccuracy(&gridBaseline, guessPotential);
  while (gridBaseline.currentAccuracy > desiredAccuracy)
  {
    relaxFn(&gridBaseline);
    computeAccuracy(&gridBaseline, guessPotentialAgainstExact);
  }
  printf("\nBaseline:");
  printGrid(&gridBaseline);
  /*
  unsigned long steps = 0;
  while (grid.currentAccuracy > desiredAccuracy && (++steps) <= 1500000)
  {
    relaxFn(&grid);
    computeAccuracy(&grid, guessPotential);
  }
  printGrid(&grid);

  subdivideGrid(&grid, boundaryValue, guessPotential);
  printGrid(&grid);
*/
  //subdivideGrid(&grid, boundaryValue, guessPotential);
  //printGrid(&grid);
}