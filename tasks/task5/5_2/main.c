#include <math.h>
#include <stdlib.h>
#include "../mtwist/mtwist.c"

#define SIMULATION_LENGTH 10000
#define PARTICLE_COUNT 20

// Defines Boltzmann's constant
#define kB 1.0
// Defines temperature
#define T 0.6
#define kBT (kB * T)

#define SIGMA 1.0
#define EPSILON 1.0

#define RND(a, b) ((mt_ldrand()) * ((double)b - (double)a) + (double)a)

// Unit cell sizes in x,y
#define Lx 5.6
#define Ly 5.6

#define MEAN_SKIP 500
#define MEAN_STEPS 100
#define MEAN_INCR (SIMULATION_LENGTH - MEAN_SKIP) / MEAN_STEPS

double potential(double r)
{
  double d = SIGMA / r;
  return 4 * EPSILON * (pow(d, 12) - pow(d, 6));
}

struct Particle
{
  double x;
  double y;
};

// Calculates the shortest distance between two particles in a periodic box
double periodicDistance(
    struct Particle *a,
    struct Particle *b)
{
  double dx = a->x - b->x;
  double dy = a->y - b->y;

  while (dx < -0.5 * Lx)
  {
    dx += Lx;
  }
  while (dx > 0.5 * Lx)
  {
    dx -= Lx;
  }
  while (dy < -0.5 * Ly)
  {
    dy += Ly;
  }
  while (dy > 0.5 * Ly)
  {
    dy -= Ly;
  }
  return sqrt(dx * dx + dy * dy);
}

double computePotential(struct Particle *particles, long n)
{
  double sum = 0.0;

  int toI = n;
  int toJ = n - 1;
  for (int i = 0; i < toI; i++)
  {
    for (int j = i; j < toJ; j++)
    {
      double r = periodicDistance(&particles[i], &particles[j + 1]);
      sum += potential(r);
    }
  }

  return sum;
}

void boundParticle(struct Particle *particles, long i)
{
  while (particles[i].x < 0.0)
  {
    particles[i].x += Lx;
  }
  while (particles[i].x >= Lx)
  {
    particles[i].x -= Lx;
  }
  while (particles[i].y < 0.0)
  {
    particles[i].y += Ly;
  }
  while (particles[i].y >= Ly)
  {
    particles[i].y -= Ly;
  }
}

// Initializes n particles in a hexagonal lattice
void initialize(struct Particle *particles, long n)
{
  for (int i = 0; i < n; i++)
  {
    particles[i].x = Lx / 5.0 * ((i % 5) + 0.5 * floor((double)i / 5.0));
    particles[i].y = Lx / 5.0 * 0.87 * (i / 5);

    boundParticle(particles, i);
  }
}

double sweep(double maxStepSize, struct Particle *particles, struct Particle *temporary, long n)
{
  double totalRatio = 0.0;
  for (int i = 0; i < n; i++)
  {
    temporary[i].x = particles[i].x + RND(-maxStepSize, maxStepSize);
    temporary[i].y = particles[i].y + RND(-maxStepSize, maxStepSize);

    double potentialChange = 0.0;
    for (int j = 0; j < n; j++)
    {
      if (i == j)
      {
        continue;
      }
      double previousDistance = periodicDistance(&particles[i], &particles[j]);
      double temporaryDistance = periodicDistance(&temporary[i], &particles[j]);

      potentialChange += potential(temporaryDistance) - potential(previousDistance);
    }

    double ratio = exp(-potentialChange / kBT);

    if (ratio > RND(0, 1))
    {
      particles[i] = temporary[i];
      boundParticle(particles, i);
    }

    totalRatio += min(1.0, ratio);
  }
  return totalRatio;
}

struct Result
{
  double maxStepSize;
  double mean;
  double cV;
  double ratio;
};

struct Result createSimulation(double maxStepSize)
{
  struct Particle *particles = (struct Particle *)malloc(sizeof(struct Particle) * PARTICLE_COUNT);
  struct Particle *temporary = (struct Particle *)malloc(sizeof(struct Particle) * PARTICLE_COUNT);

  initialize(particles, PARTICLE_COUNT);

  double initialPotential = computePotential(particles, PARTICLE_COUNT);
  //printf("Initial potential: %f\n", initialPotential);

  double *potentials = (double *)malloc(sizeof(double) * SIMULATION_LENGTH);
  double *ratios = (double *)malloc(sizeof(double) * SIMULATION_LENGTH);
  for (long i = 0; i < SIMULATION_LENGTH; i++)
  {
    ratios[i] = sweep(maxStepSize, particles, temporary, PARTICLE_COUNT);
    potentials[i] = computePotential(particles, PARTICLE_COUNT);
  }

  double *partialMeans = (double *)malloc(sizeof(double) * MEAN_STEPS);
  double *partialDeviations = (double *)malloc(sizeof(double) * MEAN_STEPS);
  double *partialRatios = (double *)malloc(sizeof(double) * MEAN_STEPS);
  for (unsigned long i = 1; i <= MEAN_STEPS; i++)
  {
    unsigned long to = min(SIMULATION_LENGTH, i * MEAN_INCR);

    double mean = 0.0;
    double deviation = 0.0;
    double ratio = 0.0;
    for (unsigned long j = MEAN_SKIP; j < to; j++)
    {
      mean += potentials[j] / (double)(to - MEAN_SKIP);
      deviation += potentials[j] * potentials[j] / (double)(to - MEAN_SKIP);
      ratio += ratios[j] / (double)((to - MEAN_SKIP) * PARTICLE_COUNT);
    }
    partialMeans[i - 1] = mean;
    partialDeviations[i - 1] = (deviation - mean * mean) / (kB * T * T);
    partialRatios[i - 1] = ratio;
  }

  struct Result result;
  result.maxStepSize = maxStepSize;
  result.mean = partialMeans[MEAN_STEPS - 1];
  result.cV = partialDeviations[MEAN_STEPS - 1];
  result.ratio = partialRatios[MEAN_STEPS - 1];

  free(particles);
  free(temporary);
  free(potentials);
  free(ratios);
  free(partialMeans);
  free(partialDeviations);
  free(partialRatios);

  return result;
}

#define N 1000
#define FROM -5.0
#define TO 2.0
int main()
{
  struct Result *results = (struct Result *)malloc(sizeof(struct Result) * N);
#pragma acc parallel loop copy(results [0:N])
  for (unsigned int n = 0; n < N; ++n)
  {
    printf("Running %d\n", n);
    struct Result result = createSimulation(pow(10, FROM + ((TO - FROM) / N) * n));
    results[n] = result;
  }

  FILE *ptr;
  ptr = fopen("./data.bin", "wb");
  unsigned int count = N;
  fwrite(&count, sizeof(unsigned int), 1, ptr);
  fwrite(results, sizeof(struct Result), N, ptr);
  fclose(ptr);

  for (unsigned int n = 0; n < N; ++n)
  {
    printf("stepSize: %f, ", results[n].maxStepSize);
    printf("mean: %f, ", results[n].mean);
    printf("cV: %f, ", results[n].cV);
    printf("ratio: %f\n", results[n].ratio);
  }

  return 0;
}