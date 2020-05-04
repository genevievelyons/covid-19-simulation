# Flattening the Curve: A Simulation Study of the Spread of COVID-19
### Jingyi Chen, Genevieve Lyons, Rebecca Youngerman, Huahua Zheng
### Harvard T.H. Chan School of Public Health

Note: This is a toy simulation of the spread of an infectious disease, and is not intended to represent any particular geographic location or use parameters that are scientifically accurate for COVID-19.

## Introduction

### Background

The purpose of this simulation is to analyze the spread of infectious diseases such as COVID-19 to better understand the way that social distancing may slow the spread for various cities in the United States.

COVID-19 is a respiratory illness that spreads from person to person. Transmission occurs through respiratory droplets, and spread is more likely when people are in close contact with one another. In March, the US government issued a number of social distancing policies and guidelines. These guidelines encourage us to avoid mass gatherings, stay in our homes, and only leave for essential needs. 

Through this simulation study, we seek to understand how these measures may help to combat the spread of an infectious disease such as this one. 

### SIR Model with a Simple Spatial Network

The simulation uses a standard SIR model with a simple spatial network. The SIR model is a simple compartmental epidemiological model with three main elements:

**Susceptible (S)**, where the individual has not yet been infected, and has no immunity.

**Infected (I)**, where the individual is currently infected and contagious to Susceptible neighbors.

**Removed (R)**, where the removal from further participation in the process is assumed to be permanent, due to death.

In our model, all individuals are initially susceptible. The pandemic is initiated by a single infected individual at a random location in the network. Each individual has a probability *p* of being infected by any individual in its infection neighborhood, calculated by the Euclidean Distance:

<img src="https://render.githubusercontent.com/render/math?math={(x,y) s.t. \sqrt{(x-x_0)^2 %2B (y-y_0)^2} \leq r}">

We assume that this probability of infection *p* is constant per time step, and each infected individual has a probability *q* to be removed from the population through death. After recovery, each individual becomes immune to the disease. The simulation is conducted over sufficient discrete time steps to run the pandemic to completion.

The social distancing function determines the behavior of each individual. A constant of 1 for each individual indicates that all individuals are moving about as normal. We will explore the effect of changing the social behavior of some individuals to simulate social distancing.


### Need for Big Compute


### Design





## Replicability Information 

### Running the Euclidean Distance Code: Serial Implementation

The code takes argument of N members of the population (defaults to 200 if no number is given)

I ran it on a t2.2xlarge AWS Ubuntu 16.04 instance. You will need to upload both `euclidean.c` and `timing.h`.

First, increase the limit:
`ulimit -s unlimited`

Compile the code:
`gcc -DUSE_CLOCK euclidean.c -lm -o euclidean`

Run the code, including the members of the population (e.g., N = 100):
`./euclidean 100`

The elapsed time will be printed after the results.

### Running the Euclidean Distance Code: OpenMP Implementation

I ran it on a t2.2xlarge AWS Ubuntu 16.04 instance. Upload both `euclidean_omp.c` and `timing.c`.

First, increase the limit:
`ulimit -s unlimited`

Compile the code:
`gcc -DUSE_CLOCK -fopenmp euclidean_omp.c timing.c -lm -o eud_omp`

Set the number of threads:
`export OMP_NUM_THREADS=8`

Run the code, including the members of the population (e.g., N = 100):
`./eud_omp 100`

### Running the Euclidean Distance Code: MPI Implementation

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
`mpirun -np 4 -hosts master2,node2 ./euclidean_mpi 100`

### Running the Euclidean Distance Code: MPI+OpenMP Implementation

Same setup as 'MPI Implementation'

Compile the code on mpiuser@master:
`mpicc -DUSE_CLOCK -fopenmp euclidean_mpi_omp.c timing.c -lm -o eud_mpi_omp`

Move it to the cloud folder: 
`cp eud_mpi_omp cloud && cd cloud`

Run the code:
`mpirun -np 4 -hosts master,node1 -genv OMP_NUM_THREADS 2 ./eud_mpi_omp 100`

### Python/C pipeline

Compile：

`gcc -fPIC -c euclidean_IO.c `  
`gcc -shared -o euclidean_IO.so euclidean_IO.o`

Calling from python:
`python simulation.py`


## Experiments


## Simulation Results


## Conclusions and Recommendations



## References

We were inspired by the Washington Post article, [**"Why outbreaks like coronavirus spread exponentially, and how to “flatten the curve”**](https://www.washingtonpost.com/graphics/2020/world/corona-simulator/) by Harry Stevens. 

We also reference the work of [Philip Mocz](https://github.com/pmocz/coronavirusToySimulation) when building our simulation.
