#include "../common/relax.c"

#define DATA_NAME "../../data/1011_b.bin"
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
      "../../data/1011_b_1.bin",
      LINEAR_DIMENSION,
      POINTS,
      WANTED_ACCURACY_PERCENT / 100.0,
      &relaxGaussSeidelCheckered,
      &initialValue,
      &boundaryValue,
      &guessPotential,
      NULL);

  runRelaxationsUntilAccuracy(
      "../../data/1011_b_2.bin",
      LINEAR_DIMENSION,
      POINTS * 2,
      WANTED_ACCURACY_PERCENT / 100.0,
      &relaxGaussSeidelCheckered,
      &initialValue,
      &boundaryValue,
      &guessPotential,
      NULL);

  const double fromLogarithm = 5;
  const double toLogarithm = 100;
  const unsigned long steps = toLogarithm / fromLogarithm;

  double *gridSizes = (double *)malloc(sizeof(double) * steps);
  unsigned long *relaxations = (unsigned long *)malloc(sizeof(unsigned long) * steps);

  for (unsigned long n = 0; n < steps; n++)
  {
    double logarithm = fromLogarithm + n * (toLogarithm - fromLogarithm) / (steps - 1);
    unsigned long value = (unsigned long)logarithm;

    gridSizes[n] = LINEAR_DIMENSION / (double)value;
    relaxations[n] = runRelaxationsUntilAccuracy(NULL, LINEAR_DIMENSION, value, WANTED_ACCURACY_PERCENT / 100.0, &relaxGaussSeidelCheckered, &initialValue, &boundaryValue, &guessPotential, NULL);

    printf("%f %d: %d\n", logarithm, value, relaxations[n]);
  }

  FILE *f = fopen("../../data/1011_b_relaxations.bin", "wb");
  fwrite(&steps, sizeof(unsigned long), 1, f);
  fwrite(gridSizes, sizeof(double), steps, f);
  fwrite(relaxations, sizeof(unsigned long), steps, f);
  fclose(f);

  return 0;
}