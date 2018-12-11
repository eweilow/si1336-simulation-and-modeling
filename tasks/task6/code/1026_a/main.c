#include "../common/multigrid.c"
#include <math.h>

#define LINEAR_DIMENSION 10.0
#define WANTED_ACCURACY_PERCENT 0.1

double guessPotential(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 1.0;
}

double boundaryValue(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 1;
}

double initialValue(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 0.0;
}

int main()
{

  multigrid(
      "../../data/1026_exact_1.bin",
      "../../data/1026_baseline_1.bin",
      "../../data/1026_multigrid_1.bin",
      "../../data/1026_premultigrid_1.bin",
      "../../data/1026_params_1.bin",
      LINEAR_DIMENSION,
      WANTED_ACCURACY_PERCENT / 100.0,
      6,
      4,
      1,
      1,
      &relaxGaussSeidelCheckered,
      &initialValue,
      &boundaryValue,
      &guessPotential);

  return 0;
}