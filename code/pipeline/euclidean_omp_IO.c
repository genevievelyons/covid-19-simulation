#include <stdio.h>
#include <math.h>
#include <stdlib.h>

//function to find distance between 2 points
float dis(float x1, float y1, float x2, float y2) {
   float distance = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
   return distance;
}

void contact( double* x, double *y,double* contact,int N,double r_inf) {
   int i, j;
   double  r[N][N];

   #pragma omp parallel shared(r, x, y) private(i, j)
   {
   #pragma omp for
   for(i=0; i<N; i++) {
      for(j=0;j<N;j++) {
         //Calculate the distance
         r[i][j] = dis(x[i], y[i], x[j], y[j]);
         //printf("r[%d][%d] = %f\n", i,j, r[i][j]);
         //Contact
         if(r[i][j]<r_inf){contact[i*N+j]=1;}
      
      }
   }
}
}
