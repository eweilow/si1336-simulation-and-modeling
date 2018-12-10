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
  return 0.9 * guessPotential(grid, i, j);
}

int main()
{
  runRelaxationsUntilAccuracy(
      "../../data/1010_a_1.bin",
      LINEAR_DIMENSION,
      POINTS,
      WANTED_ACCURACY_PERCENT / 100.0,
      &relax,
      &initialValue,
      &boundaryValue,
      &guessPotential,
      NULL);

  runRelaxationsUntilAccuracy(
      "../../data/1010_a_2.bin",
      LINEAR_DIMENSION,
      POINTS * 2,
      WANTED_ACCURACY_PERCENT / 100.0,
      &relax,
      &initialValue,
      &boundaryValue,
      &guessPotential,
      NULL);

  return 0;
}