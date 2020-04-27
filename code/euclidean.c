#include <stdio.h>
#include <math.h>
#include <time.h>
#include "timing.h"
#include <stdlib.h>

//function to find distance between 2 points
float dis(float x1, float y1, float x2, float y2) {
   float distance = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
   return distance;
}

int main(int argc, char** argv) {
  // int l = N;
   int i, j;
   timing_t tstart, tend;

int N;
N      = (argc > 1) ? atoi(argv[1]) : 200;

   int l = N;
   double x[N],
          y[N],
          r[N][N];

//Generate the x and y coordinates
for (i=0; i<N; i++)
    x[i]= i;

for (i=0; i<N; i++)
    y[i]= i;

get_time(&tstart);

//Calculate the distance

   for(i=0; i<l; i++) {
      for(j=0;j<l;j++) {
         r[i][j] = dis(x[i], y[i], x[j], y[j]);
         printf("r[%d][%d] = %f\n", i,j, r[i][j]);
      }
   }
get_time(&tend);

printf("******************************************************\n");
printf("Elapsed time: %g s\n", timespec_diff(tstart, tend));
}


