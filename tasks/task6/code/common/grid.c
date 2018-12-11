#include <stdlib.h>
#include <stdio.h>
#include <math.h>

struct Grid
{
  double delta;
  double linearDimension;
  unsigned long points;

  unsigned long relaxations;

  double currentAccuracy;

  double **initialGrid;
  double **currentGrid;
  double **nextGrid;
};

double **allocateGridPoints(unsigned long points)
{
  double **data = (double **)malloc(points * sizeof(double *));

  for (unsigned long row = 0; row < points; ++row)
  {
    data[row] = (double *)malloc(points * sizeof(double));
  }

  return data;
}

void freeGridPoints(double **data, unsigned long points)
{
  for (unsigned long row = 0; row < points; ++row)
  {
    free(data[row]);
  }

  free(data);
}

void freeGrid(struct Grid *grid)
{
  freeGridPoints(grid->currentGrid, grid->points);
  freeGridPoints(grid->initialGrid, grid->points);
}

struct Grid createGrid(double linearDimension, unsigned long points)
{
  struct Grid grid;

  grid.delta = linearDimension / points;
  grid.linearDimension = linearDimension;
  grid.points = points + 1;

  grid.currentAccuracy = 0.0;
  grid.initialGrid = allocateGridPoints(points + 1);
  grid.currentGrid = allocateGridPoints(points + 1);
  grid.nextGrid = allocateGridPoints(points + 1);

  grid.relaxations = 0;

  return grid;
}

void setInitialValues(struct Grid *grid, double (*f)(struct Grid *grid, unsigned long, unsigned long))
{
  for (unsigned long i = 1; i < grid->points - 1; ++i)
  {
    for (unsigned long j = 1; j < grid->points - 1; ++j)
    {
      double v = f(grid, i, j);
      grid->initialGrid[i][j] = v;
      grid->currentGrid[i][j] = v;
    }
  }
}

void setBoundaryConditions(struct Grid *grid, double (*f)(struct Grid *grid, unsigned long, unsigned long))
{
  for (unsigned long i = 0; i < grid->points; ++i)
  {
    grid->initialGrid[0][i] = f(grid, 0, i);
    grid->initialGrid[grid->points - 1][i] = f(grid, grid->points - 1, i);
    grid->initialGrid[i][0] = f(grid, i, 0);
    grid->initialGrid[i][grid->points - 1] = f(grid, i, grid->points - 1);

    grid->currentGrid[0][i] = grid->initialGrid[0][i];
    grid->currentGrid[grid->points - 1][i] = grid->initialGrid[grid->points - 1][i];
    grid->currentGrid[i][0] = grid->initialGrid[i][0];
    grid->currentGrid[i][grid->points - 1] = grid->initialGrid[i][grid->points - 1];
  }
}

void copyNextIntoCurrentGrid(struct Grid *grid, double **from, double **to)
{
  // Don't care about boundaries
  for (unsigned long i = 1; i < grid->points - 1; ++i)
  {
    for (unsigned long j = 1; j < grid->points - 1; ++j)
    {
      to[i][j] = from[i][j];
    }
  }
}

double getAccuracy(double expected, double actual)
{
  return fabs(actual - expected) / expected;
}

void printGrid(struct Grid *grid)
{
  printf("\nAccuracy = %.4f%%, relaxations = %d, p = %d\n", grid->currentAccuracy * 100.0, grid->relaxations, grid->points);

  if (grid->points > 23)
  {
    printf("<grid truncated due to size>\n");
    return;
  }
  for (unsigned long i = 0; i < grid->points; ++i)
  {
    for (unsigned long j = 0; j < grid->points; ++j)
    {
      printf("%*.2f", 8, grid->currentGrid[i][j]);
    }
    printf("\n");
  }
}

void computeAccuracy(struct Grid *grid, double (*f)(struct Grid *grid, unsigned long, unsigned long))
{
  double accuracy = 0;
  for (unsigned long i = 1; i < grid->points - 1; ++i)
  {
    for (unsigned long j = 1; j < grid->points - 1; ++j)
    {
      double expected = f(grid, i, j);
      double error = getAccuracy(expected, grid->currentGrid[i][j]);
      accuracy = max(accuracy, error);
    }
  }
  grid->currentAccuracy = accuracy;
}

void storeGridInFile(FILE *file, struct Grid *grid)
{
  unsigned long points = grid->points;
  unsigned long relaxations = grid->relaxations;
  double currentAccuracy = grid->currentAccuracy;
  fwrite(&points, sizeof(unsigned long), 1, file);
  fwrite(&relaxations, sizeof(unsigned long), 1, file);
  fwrite(&currentAccuracy, sizeof(double), 1, file);

  for (unsigned long row = 0; row < grid->points; ++row)
  {
    fwrite(grid->currentGrid[row], sizeof(double), grid->points, file);
  }
}