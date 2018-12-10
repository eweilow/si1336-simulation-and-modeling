#include "../common/relax.c"

#define DATA_NAME "../../data/1010_a.bin"
#define LINEAR_DIMENSION 10.0
#define POINTS 10
#define WANTED_ACCURACY_PERCENT 1.0

double guessPotential(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 10.0;
}

double boundaryValue(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 10.0;
}

double initialValue(struct Grid *grid, unsigned long i, unsigned long j)
{
  if (i == grid->points / 2 && i == j)
  {
    return 4.0;
  }
  return 0.0;
  //return 0.9 * guessPotential(grid, i, j);
}

int main()
{
  runRelaxationsUntilAccuracy(
      "../../data/1010_b_1.bin",
      LINEAR_DIMENSION,
      POINTS,
      WANTED_ACCURACY_PERCENT / 100.0,
      &relax,
      &initialValue,
      &boundaryValue,
      &guessPotential,
      NULL);

  return 0;
}