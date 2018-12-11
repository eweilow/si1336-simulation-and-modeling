#include "../common/multigrid.c"
#include <math.h>

#define PI 3.141592
#define LINEAR_DIMENSION PI * 2
#define WANTED_ACCURACY_PERCENT 0.1

double guessPotential(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 1.0;
}

double boundaryValue(struct Grid *grid, unsigned long i, unsigned long j)
{
  double x = i / ((double)grid->points - 1) * LINEAR_DIMENSION;
  double y = j / ((double)grid->points - 1) * LINEAR_DIMENSION;
  return 5.0 + cos(x) + sin(y);
}

double initialValue(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 0.0;
}

int main()
{

  multigrid(
      "../../data/1026_exact_2.bin",
      "../../data/1026_baseline_2.bin",
      "../../data/1026_multigrid_2.bin",
      "../../data/1026_premultigrid_2.bin",
      "../../data/1026_params_2.bin",
      LINEAR_DIMENSION,
      WANTED_ACCURACY_PERCENT / 100.0,
      4,
      4,
      5,
      5,
      &relaxGaussSeidelCheckered,
      &initialValue,
      &boundaryValue,
      &guessPotential);

  multigrid(
      "../../data/1026_exact_3.bin",
      "../../data/1026_baseline_3.bin",
      "../../data/1026_multigrid_3.bin",
      "../../data/1026_premultigrid_3.bin",
      "../../data/1026_params_3.bin",
      LINEAR_DIMENSION,
      WANTED_ACCURACY_PERCENT / 100.0,
      4,
      4,
      5,
      0,
      &relaxGaussSeidelCheckered,
      &initialValue,
      &boundaryValue,
      &guessPotential);

  multigrid(
      "../../data/1026_exact_4.bin",
      "../../data/1026_baseline_4.bin",
      "../../data/1026_multigrid_4.bin",
      "../../data/1026_premultigrid_4.bin",
      "../../data/1026_params_4.bin",
      LINEAR_DIMENSION,
      WANTED_ACCURACY_PERCENT / 100.0,
      8,
      4,
      5,
      0,
      &relaxGaussSeidelCheckered,
      &initialValue,
      &boundaryValue,
      &guessPotential);
  return 0;
}