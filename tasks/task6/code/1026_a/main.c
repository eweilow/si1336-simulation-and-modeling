#include "../common/multigrid.c"

#define LINEAR_DIMENSION 10.0
#define WANTED_ACCURACY_PERCENT 1.0

double guessPotential(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 1.0;
}

double boundaryValue(struct Grid *grid, unsigned long i, unsigned long j)
{
  return i / ((double)grid->points - 1) + j / ((double)grid->points - 1);
}

double initialValue(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 0.0;
}

int main()
{

  multigrid(
      LINEAR_DIMENSION,
      WANTED_ACCURACY_PERCENT / 100.0,
      &relaxGaussSeidelCheckered,
      &initialValue,
      &boundaryValue,
      &guessPotential);

  return 0;
}