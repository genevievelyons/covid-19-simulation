# Flattening the Curve: A Simulation Study of the Spread of COVID-19

Note: This is a toy simulation of the spread of an infectious disease, and is not intended to represent any particular geographic location or use parameters that are scientifically accurate for COVID-19.

## Running the Euclidean Distance Code: Serial Implementation

The code takes argument of N members of the population (defaults to 200 if no number is given)

I ran it on a t2.2xlarge AWS Ubuntu 16.04 instance. You will need to upload both `euclidean.c` and `timing.h`.

First, increase the limit:
`ulimit -s unlimited`

Compile the code:
`gcc -DUSE_CLOCK euclidean.c -lm -o euclidean`

Run the code, including the members of the population (e.g., N = 100):
`./euclidean 100`

The elapsed time will be printed after the results.

## Running the Euclidean Distance Code: OpenMP Implementation

I ran it on a t2.2xlarge AWS Ubuntu 16.04 instance. Upload both `euclidean_omp.c` and `timing.c`.

First, increase the limit:
`ulimit -s unlimited`

Compile the code:
`gcc -DUSE_CLOCK -fopenmp euclidean_omp.c timing.c -lm -o eud_omp`

Set the number of threads:
`export OMP_NUM_THREADS=8`

Run the code, including the members of the population (e.g., N = 100):
`./eud_omp 100`

## Running the Euclidean Distance Code: MPI Implementation

Set up a distributed AWS cluster following IG7.

First, increase the limit:
`ulimit -s unlimited`

Then, export the ports:

`export MPICH_PORT_RANGE=10000:10100`

`export MPIR_CVAR_CH3_PORT_RANGE=10000:10100`

Compile the code on mpiuser@master:
`mpicc -DUSE_CLOCK euclidean_mpi.c -lm -o euclidean_mpi`

Move it to the cloud folder: 
`cp euclidean_mpi cloud && cd cloud`

Run the code:
`mpirun -np 4 -hosts master2,node2 ./euclidean_mpi 100 | sort -V`

## Running the Euclidean Distance Code: MPI+OpenMP Implementation

Same setup as 'MPI Implementation'

Compile the code on mpiuser@master:
`mpicc -DUSE_CLOCK -fopenmp euclidean_mpi_omp.c timing.c -lm -o eud_mpi_omp`

Move it to the cloud folder: 
`cp eud_mpi_omp cloud && cd cloud`

Run the code:
`mpirun -np 4 -hosts master,node1 -genv OMP_NUM_THREADS 2 ./eud_mpi_omp 100`

## Python/C pipeline

Compile：

`gcc -fPIC -c euclidean_IO.c `  
`gcc -shared -o euclidean_IO.so euclidean_IO.o`

Calling from python:
`python simulation.py`






### References

We were inspired by the Washington Post article, [**"Why outbreaks like coronavirus spread exponentially, and how to “flatten the curve”**](https://www.washingtonpost.com/graphics/2020/world/corona-simulator/) by Harry Stevens. 

We also reference the work of [Philip Mocz](https://github.com/pmocz/coronavirusToySimulation) when building our simulation.
