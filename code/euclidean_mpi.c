#include <stdio.h>
#include <math.h>
#include <time.h>
#include "timing.h"
#include <stdlib.h>
#include <mpi.h>
#include <string.h>

//function to find distance between 2 points
double dis(double x1, double y1, double x2, double y2) {
   double distance = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
   return distance;
}

int main(int argc, char** argv) {

int size, rank;

    /* Initialize MPI and get rank and size */
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Status status;

   int i, j;
   double tstart, tend;
   int N;

N  = (argc > 1) ? atoi(argv[1]) : 200;

   int l = N;
   double *x;
   double *y;

    /* Allocate and initialize local arrays */
    x = (double*)malloc( (N) * sizeof(double) );
    y = (double*)malloc( (N) * sizeof(double) );
    memset(x, 0, (N) * sizeof(double));
    memset(y, 0, (N) * sizeof(double));

//   int rank, size;
   int iloc, nper;
   int p;

//Generate the x and y coordinates
for (i=0; i<N; i++)
    x[i]= i;

for (i=0; i<N; i++)
    y[i]= i;

//Calculate the distance

    /* Split internal index range among processors */
    nper    = N/size;
    double *r;
    /*Allocate and initialize local array r*/
    r =(double*) malloc( (nper*N) * sizeof(double) );
    memset(r, 0, (nper*N) * sizeof(double));

/* Run the Distance Calculation */
   tstart = MPI_Wtime();
//get_time(&tstart);

   for(i=rank*nper; i<(rank*nper + nper); i++) {
      for(j=0;j<l;j++) {
         iloc = i - rank*nper;
//         (&r)[iloc * N + j] = malloc(dis(x[i], y[i], x[j], y[j]));
           /* Uncomment this line if you want to print the array*/
//          printf("r[%d][%d] = %f\n",i,j, dis(x[i], y[i], x[j], y[j]));
          /* Use this line for simple timing experiments*/
          dis(x[i], y[i], x[j], y[j]);
       
      }
   }

    tend = MPI_Wtime();

/* First way to print */

//FILE* fp = fopen("out.txt", "w+");

//    for(i=0; i<nper; i++) {
 //     for(j=0;j<N;j++) {
//         fprintf(fp,"r[%d][%d] = %f\n",rank*nper+ i,j, r[i][j]);
 //        printf("r[%d][%d] = %f\n",rank*nper+ i,j, r[i][j]);
 //     }
 //  }

//fclose(fp);


if (rank == 0) {
    printf("*A*****************************************************\n");
    printf("*Processes: %d\n", size);
    printf("*Elapsed time: %f s\n", tend - tstart);
}

free(x);
free(y);
free(r);

MPI_Finalize();
return 0;
}



