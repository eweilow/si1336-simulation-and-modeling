#include "../common/multigrid.c"
#include <math.h>

#define LINEAR_DIMENSION 10.0
#define WANTED_ACCURACY_PERCENT 0.1

double guessPotential(struct Grid *grid, unsigned long i, unsigned long j)
{
  return 1.0;
}

#define PI 3.141592
double boundaryValue(struct Grid *grid, unsigned long i, unsigned long j)
{
  double x = i / ((double)grid->points - 1);
  double y = j / ((double)grid->points - 1);
  return 5.0 + cos(x * PI * 2) + sin(y * PI * 2);
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
      6,
      4,
      2,
      2,
      &relaxGaussSeidelCheckered,
      &initialValue,
      &boundaryValue,
      &guessPotential);

  return 0;
}