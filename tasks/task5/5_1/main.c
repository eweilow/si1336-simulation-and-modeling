#include <stdlib.h>
#include <math.h>

#define WANTED_POINTS 1000000
#define INITIAL_SKIP 250
#define SUM_STEPS (WANTED_POINTS - INITIAL_SKIP)
#define MEAN_STEPS 25
#define MEAN_INCR SUM_STEPS / MEAN_STEPS
#define DELTA 1.0
#define RND(a, b) (((double)(rand()) / (double)RAND_MAX) * ((double)b - (double)a) + (double)a)

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

void execute(double *values, double *deviations, double *points, double *partialMeans, double *partialDeviations)
{
#pragma acc parallel loop present(values, deviations, points)
  for (unsigned long i = 0; i < SUM_STEPS; i++)
  {
    float f = function(points[i + INITIAL_SKIP]);
    values[i] = f;
    deviations[i] = f * f;
  }

  for (unsigned long i = 1; i <= MEAN_STEPS; i++)
  {
    unsigned long to = min(SUM_STEPS, i * MEAN_INCR);

    double mean = 0.0;
    double deviation = 0.0;
#pragma acc parallel loop present(values) reduction(+                   \
                                                    : mean) reduction(+ \
                                                                      : deviation)
    for (unsigned long j = 0; j < to; j++)
    {
      mean += values[j] / (double)(to);
      deviation += values[j] * values[j] / (double)(to);
    }
    partialMeans[i - 1] = mean;
    partialDeviations[i - 1] = sqrt(deviation - mean * mean) / sqrt((double)(to));
  }
}

int main()
{
  unsigned long head = 0;
  double *points = (double *)malloc(sizeof(double) * WANTED_POINTS);
  points[head] = 0.01;

  unsigned long partialSumHead = 0;
  double *values = (double *)malloc(sizeof(double) * SUM_STEPS);
  double *deviations = (double *)malloc(sizeof(double) * SUM_STEPS);
  double *partialMeans = (double *)malloc(sizeof(double) * MEAN_STEPS);
  double *partialDeviations = (double *)malloc(sizeof(double) * MEAN_STEPS);

  printf("Generating points\n");
  while ((head + 1) < WANTED_POINTS)
  {
    double next = points[head] + RND(-DELTA, DELTA);

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
#pragma acc data copyout(values [0:SUM_STEPS]) copyout(deviations [0:SUM_STEPS]) copyin(points [0:WANTED_POINTS])
  execute(values, deviations, points, partialMeans, partialDeviations);

  double analyzedMean = 0.0;
  double analyzedSigma = 0.0;
  for (int i = 0; i < SUM_STEPS; i++)
  {
    analyzedMean += values[i] / (double)(SUM_STEPS);
    analyzedSigma += values[i] * values[i] / (double)(SUM_STEPS);
  }
  analyzedSigma -= analyzedMean * analyzedMean;
  analyzedSigma = sqrt(analyzedSigma);
  analyzedSigma /= sqrt((double)(SUM_STEPS));
  printf("mean: %f vs %f\n", analyzedMean, partialMeans[MEAN_STEPS - 1]);
  printf("delta: %f vs %f\n", analyzedSigma, partialDeviations[MEAN_STEPS - 1]);

  for (int i = 0; i < MEAN_STEPS; i++)
  {
    printf("%d: %f, %f\n", (i + 1) * MEAN_INCR, partialMeans[i], partialDeviations[i]);
  }

  return 0;
}