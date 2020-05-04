#include <stdio.h>
#include <math.h>
#include <time.h>
#include "timing.h"
#include <stdlib.h>
#include <mpi.h>
#include <string.h>

//function to find distance between 2 points
float dis(float x1, float y1, float x2, float y2) {
   float distance = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
   return distance;
}

int main(int argc, char** argv) {

   int i, j;
   double tstart, tend;
   int N;

N  = (argc > 1) ? atoi(argv[1]) : 2000;

   int l = N;
   double x[N],
          y[N];
   int rank, size, rank_num;
   int iloc, nper;
   int p;

//Generate the x and y coordinates
for (i=0; i<N; i++)
    x[i]= i;

for (i=0; i<N; i++)
    y[i]= i;

//Calculate the distance

    /* Initialize MPI and get rank and size */
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Status status;

    /* Split internal index range among processors */
    nper    = N/size;
    double r[nper][N];

/* Run the Distance Calculation */
   tstart = MPI_Wtime();
//get_time(&tstart);

   for(i=rank*nper; i<(rank*nper + nper); i++) {
      for(j=0;j<l;j++) {
         iloc = i - rank*nper;
         r[iloc][j] = dis(x[i], y[i], x[j], y[j]);
      }
   }

    tend = MPI_Wtime();
    
    
    
    

//get_time(&tend);

////if(rank==1){
//    MPI_Send(&r, nper*N, MPI_DOUBLE, 0, 1, MPI_COMM_WORLD);
//}
//
//if(rank==0){
//    MPI_Recv(&r, nper*N, MPI_DOUBLE, 0, 1, MPI_COMM_WORLD, &status);
//}

//FILE* fp = fopen("out.txt", "w+");
    
    
    for (rank_num = 0; rank_num < size; rank_num++){
        MPI_Barrier(MPI_COMM_WORLD);
        if (rank_num == rank) {
                for(i=0; i<nper; i++) {
                    for(j=0;j<N;j++) {
//         fprintf(fp,"r[%d][%d] = %f\n",rank*nper+ i,j, r[i][j]);
                    printf("r[%d][%d] = %f\n",rank*nper+ i,j, r[i][j]);
                    }     
                }
            printf("Hello World from Rank %d\n", rank);
            printf("*Elapsed time: %f s\n", tend - tstart);

            
            
        }
    } 
    MPI_Finalize();
}

//    for(i=0; i<nper; i++) {
//      for(j=0;j<N;j++) {
////         fprintf(fp,"r[%d][%d] = %f\n",rank*nper+ i,j, r[i][j]);
//         printf("r[%d][%d] = %f\n",rank*nper+ i,j, r[i][j]);
//      }
//   }

//fclose(fp);

//if (rank == 0) {
//    printf("*A*****************************************************\n");
//    printf("*Processes: %d\n", size);
//    printf("*Elapsed time: %f s\n", tend - tstart);
//}
//
//MPI_Finalize();
//}

