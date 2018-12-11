#include "../common/relax.c"
#include "../common/iterate.c"

#define LINEAR_DIMENSION 10.0
#define POINTS 10
#define WANTED_ACCURACY_PERCENT 1.0

double boundaryValue(struct Grid *grid, unsigned long i, unsigned long j)
{
  if (i == 0 || i == (grid->points - 1))
  {
    return 10.0;
  }
  return 5.0;
}

double boundaryValue2(struct Grid *grid, unsigned long i, unsigned long j)
{
  if (i == 0)
  {
    return 0.0;
  }
  return 10.0;
}

double initialValue(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 7.5;
  //return 0.9 * guessPotential(grid, i, j);
}

int main()
{
  runRelaxationsAgainstHighPrecision("../../data/1010_c_1.bin",
                                     LINEAR_DIMENSION, POINTS,
                                     WANTED_ACCURACY_PERCENT / 100.0,
                                     &relax,
                                     &initialValue, &boundaryValue);

  runRelaxationsAgainstHighPrecision("../../data/1010_c_2.bin",
                                     LINEAR_DIMENSION, POINTS,
                                     WANTED_ACCURACY_PERCENT / 100.0,
                                     &relax,
                                     &initialValue, &boundaryValue2);

  return 0;
}