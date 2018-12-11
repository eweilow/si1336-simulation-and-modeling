#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "../mtwist/mtwist.c"

#define WANTED_POINTS 2000000
#define INITIAL_SKIP 25000
#define INITIAL_MEAN_SAMPLE 250000
#define MEAN_STEPS 25000
#define MEAN_INCR (WANTED_POINTS - INITIAL_MEAN_SAMPLE) / MEAN_STEPS
#define RND(a, b) ((mt_ldrand()) * ((double)b - (double)a) + (double)a)

double function(double x)
{
  return x;
}

double distribution(double x)
{
  if (x < 0.0)
  {
    return 0.0;
  }
  return exp(-x);
}

void execute(double *values, double *points, double *partialMeans, double *partialDeviations)
{
#pragma acc parallel loop present(values, points)
  for (unsigned long long i = 0; i < WANTED_POINTS; i++)
  {
    values[i] = function(points[i]);
  }

  for (unsigned long long i = 1; i <= MEAN_STEPS; i++)
  {
    unsigned long long to = min(WANTED_POINTS, INITIAL_MEAN_SAMPLE + i * MEAN_INCR);

    double toDouble = (double)(to - INITIAL_SKIP);
    double mean = 0.0;
    double deviation = 0.0;
#pragma acc parallel loop present(values) copyin(toDouble) reduction(+                   \
                                                                     : mean) reduction(+ \
                                                                                       : deviation)
    for (unsigned long long j = INITIAL_SKIP; j < to; j++)
    {
      double v = values[j] / toDouble;
      mean += v;
      deviation += values[j] * v;
    }
    partialMeans[i - 1] = mean;
    partialDeviations[i - 1] = sqrt((deviation - mean * mean) / toDouble);
  }
}

void runSimulations(char *filename, double delta)
{
  unsigned long long head = 0;
  double *points = (double *)malloc(sizeof(double) * WANTED_POINTS);
  points[head] = 0.01;

  unsigned long long partialSumHead = 0;
  double *values = (double *)malloc(sizeof(double) * WANTED_POINTS);
  double *partialMeans = (double *)malloc(sizeof(double) * MEAN_STEPS);
  double *partialDeviations = (double *)malloc(sizeof(double) * MEAN_STEPS);

  printf("Generating points\n");
  while ((head + 1) < WANTED_POINTS)
  {
    double next = points[head] + RND(-delta, delta);

    if ((distribution(next) / distribution(points[head])) >= RND(0, 1))
    {
      points[head + 1] = next;
      //printf("%d, %f\n", head, next);
    }
    else
    {
      points[head + 1] = points[head];
    }
    ++head;
  }
  printf("Executing summation\n");
#pragma acc data copyout(values [0:WANTED_POINTS]) copyin(points [0:WANTED_POINTS])
  execute(values, points, partialMeans, partialDeviations);

  printf("Analyzing result\n");
  double analyzedMean = 0.0;
  double analyzedSigma = 0.0;
  for (unsigned long long i = 0; i < WANTED_POINTS; i++)
  {
    analyzedMean += values[i] / (double)(WANTED_POINTS);
    analyzedSigma += values[i] * values[i] / (double)(WANTED_POINTS);
  }
  analyzedSigma -= analyzedMean * analyzedMean;
  analyzedSigma = sqrt(analyzedSigma);
  analyzedSigma /= sqrt((double)(WANTED_POINTS));
  printf("mean: %f vs %f\n", analyzedMean, partialMeans[MEAN_STEPS - 1]);
  printf("delta: %f vs %f\n", analyzedSigma, partialDeviations[MEAN_STEPS - 1]);

  FILE *ptr;
  ptr = fopen(filename, "wb");
  unsigned long long count = MEAN_STEPS;
  fwrite(&count, sizeof(unsigned long long), 1, ptr);
  unsigned long long step = MEAN_INCR;
  fwrite(&step, sizeof(unsigned long long), 1, ptr);
  unsigned long long skip = INITIAL_MEAN_SAMPLE;
  fwrite(&skip, sizeof(unsigned long long), 1, ptr);
  fwrite(partialMeans, sizeof(double), MEAN_STEPS, ptr);
  fwrite(partialDeviations, sizeof(double), MEAN_STEPS, ptr);
  fclose(ptr);
  /*for (unsigned long long i = 0; i < MEAN_STEPS; i++)
  {
    printf("%d: mean %f, delta %f\n", (i + 1) * MEAN_INCR, partialMeans[i], partialDeviations[i]);
  }*/

  free(points);
  free(values);
  free(partialMeans);
  free(partialDeviations);
}

int main()
{
  runSimulations("data_0dot2.bin", 0.2);
  runSimulations("data_0dot8.bin", 0.8);
  runSimulations("data_1dot6.bin", 1.6);
  runSimulations("data_6dot4.bin", 6.4);
  return 0;
}