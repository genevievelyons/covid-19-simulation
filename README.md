# Flattening the Curve: A Simulation Study of the Spread of COVID-19
### Jingyi Chen, Genevieve Lyons, Rebecca Youngerman, Huahua Zheng
### Harvard T.H. Chan School of Public Health

## Check out our [WEBSITE](https://ryoungerman8.wixsite.com/cs205finalproject)! (Has the same information as is below, but much prettier.)

Note: This is a toy simulation of the spread of an infectious disease and is not intended to represent any particular geographic location or use parameters that are scientifically accurate for COVID-19.

## Introduction

### Background

The purpose of this simulation is to analyze the spread of infectious diseases such as COVID-19 to better understand the way that social distancing may slow the spread for various cities in the United States.

COVID-19 is a respiratory illness that spreads from person to person. Transmission occurs through respiratory droplets, and spread is more likely when people are in close contact with one another. In March, the US government issued a number of social distancing policies and guidelines. These guidelines encourage us to avoid mass gatherings, stay in our homes, and only leave for essential needs. The purpose of these guidelines is to ensure that our healthcare system is not burdened beyond its capacity.

Many studies and experts have demonstrated the effectiveness of these policies, such as [**Impact assessment of non-pharmaceutical interventions against coronavirus disease 2019 and influenza in Hong Kong: an observational study**](https://www.thelancet.com/journals/lanpub/article/PIIS2468-2667(20)30090-6/fulltext?utm_campaign=tlcoronavirus20&utm_content=126713203&utm_medium=social&utm_source=twitter&hss_channel=tw-758678085176795136#%20), [**"Why outbreaks like coronavirus spread exponentially, and how to “flatten the curve”**](https://www.washingtonpost.com/graphics/2020/world/corona-simulator/), and [New York Times interviews with public health / epidemiology experts](https://www.nytimes.com/2020/04/18/health/coronavirus-america-future.html).

Through this simulation study, we seek to understand how these measures may help to combat the spread of an infectious disease such as this one. 

![](./Visualizations/00_Flatten_the_Curve.png)


### SIR Model with a Simple Spatial Network

The simulation uses a standard SIR model with a simple spatial network. The SIR model is a simple compartmental epidemiological model with three main elements:

**Susceptible (S)**, where the individual has not yet been infected, and has no immunity.

**Infected (I)**, where the individual is currently infected and contagious to Susceptible neighbors.

**Removed (R)**, where the removal from further participation in the process is assumed to be permanent, due to death.

![](./Visualizations/01_SIR_Model.png)

*Source: Maharaj, S., Kleczkowski, A. Controlling epidemic spread by social distancing: Do it well or not at all. BMC Public Health 12, 679 (2012).*

In our model, all individuals are initially susceptible. The pandemic is initiated by a single infected individual at a random location in the network. Each individual has a probability *p* of being infected by any individual in its infection neighborhood, calculated by the Euclidean Distance:

<img src="https://render.githubusercontent.com/render/math?math={(x,y) s.t. \sqrt{(x-x_0)^2 %2B (y-y_0)^2} \leq r}">

We assume that this probability of infection *p* is constant per time step, and each infected individual has a probability *q* to be removed from the population through death. After recovery, each individual becomes immune to the disease. The simulation is conducted over sufficient discrete time steps to run the pandemic to completion.

The social distancing function determines the behavior of each individual. A constant of 1 for each individual indicates that all individuals are moving about as normal. We will explore the effect of changing the social behavior of some individuals to simulate social distancing.


### Need for Big Compute

**Serial Implementation:** This simulation is written serially and in Python. For a population size of N = 2,000, the runtime to pandemic completion is roughly **45 minutes** (about 30 seconds per discrete time step *t*). To model a city such as New York City, where the population density is 26,000 per square mile, the problem size would grow infeasibly large.

**Time Complexity:** <img src="https://render.githubusercontent.com/render/math?math=O(N^2)">

**Code Profiling:** There is a very clear bottleneck in the Euclidean Distance calculation, which is calculated between every individual in the population. This is an embarrassingly parallel problem where each individual distance may be calculated independently of one another. 

The parallelizable fraction of the existing code is **92%**.

![](./Visualizations/02_Code_Profile.png)


### Design

To fully exploit powerful parallelism techniques for Big Compute, we calculate the Euclidean Distance portion of the code in C. The rest of the simulation is in Python however, so we create a Python/C pipeline by which we run the simulation through Python, but the Euclidean Distance calculation is exported to parallelized C code. 

As such, our experiments will focus on the results of parallelizing **only the subsection of the code which is in C**. We will also run some experiments on the Python/C pipeline.

Here is a snippet of the C code that will be parallelized in subsequent sections:

![](./Visualizations/03_Code_Snip.png)

We will demonstrate parallelization using a hybrid system of shared and distributed memory.

![](./Visualizations/04_Design_Plan.png)


## Replicability Information 

### Amazon Web Services Instance

Create a Multi-Node Cluster on AWS using a t2.2xlarge AWS Ubuntu 16.04 instance. Follow the instructions found in [Infrastructure Guide 7: MPI on AWS](https://harvard-iacs.github.io/2020-CS205/lab/I7/guide/Guide_I7.pdf). 

Upload all files found in the `code` folder in this repository. The C code `euclidean.c`, `euclidean_omp.c`, `euclidean_mpi.c`, and `euclidean_mpi_omp.c` take argument of N members of the population. 

**Instance Specs:**


Architecture:          x86_64

CPU op-mode(s):        32-bit, 64-bit

Byte Order:            Little Endian

CPU(s):                8

On-line CPU(s) list:   0-7

Thread(s) per core:    1

Core(s) per socket:    8

Socket(s):             1

NUMA node(s):          1

Vendor ID:             GenuineIntel

CPU family:            6

Model:                 79

Model name:            Intel(R) Xeon(R) CPU E5-2686 v4 @ 2.30GHz

Stepping:              1

CPU MHz:               2300.040

BogoMIPS:              4600.08

Hypervisor vendor:     Xen

Virtualization type:   full

L1d cache:             32K

L1i cache:             32K

L2 cache:              256K

L3 cache:              46080K

NUMA node0 CPU(s):     0-7

Flags:                 fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_t


### Running the Euclidean Distance Code: Serial Implementation

First, increase the user limit:
`ulimit -s unlimited`

Compile the serial code:
`gcc -DUSE_CLOCK euclidean.c -lm -o euclidean`

Run the code, including the members of the population (e.g., N = 100):
`./euclidean 100`

The elapsed time will be printed after the results.

### Running the Euclidean Distance Code: OpenMP Implementation

First, increase the user limit:
`ulimit -s unlimited`

Compile the code:
`gcc -DUSE_CLOCK -fopenmp euclidean_omp.c timing.c -lm -o eud_omp`

Set the number of threads (e.g., 8):
`export OMP_NUM_THREADS=8`

Run the code, including the members of the population (e.g., N = 100):
`./eud_omp 100`

### Running the Euclidean Distance Code: MPI Implementation

First, ensure that both your master and node have been created and are running. Also be sure that your cloud is mounted as detailed in [Infrastructure Guide 7: MPI on AWS](https://harvard-iacs.github.io/2020-CS205/lab/I7/guide/Guide_I7.pdf). 

Enter the the `mpiuser` that you created:
`su - mpiuser`

In `mpiuser@master`:

First, increase the user limit:
`ulimit -s unlimited`

Export the ports so the master and node can communicate:

`export MPICH_PORT_RANGE=10000:10100`

`export MPIR_CVAR_CH3_PORT_RANGE=10000:10100`

Compile the code on mpiuser@master:
`mpicc -DUSE_CLOCK euclidean_mpi.c -lm -o euclidean_mpi`

Move it to the cloud folder: 
`cp euclidean_mpi cloud && cd cloud`

Run the code, including the members of the population (e.g., N = 100) and the number of processes (e.g., 4):
`mpirun -np 4 -hosts master,node1 ./euclidean_mpi 100`

### Running the Euclidean Distance Code: MPI+OpenMP Hybrid Implementation

First, ensure that both your master and node have been created and are running. Also be sure that your cloud is mounted as detailed in [Infrastructure Guide 7: MPI on AWS](https://harvard-iacs.github.io/2020-CS205/lab/I7/guide/Guide_I7.pdf). 

Enter the the `mpiuser` that you created:
`su - mpiuser`

In `mpiuser@master`:

First, increase the user limit:
`ulimit -s unlimited`

Don't forget to use dynamic scheduling: `export OMP_SCHEDULE=dynamic`

Export the ports so the master and node can communicate:

`export MPICH_PORT_RANGE=10000:10100`

`export MPIR_CVAR_CH3_PORT_RANGE=10000:10100`

Compile the code on mpiuser@master:
`mpicc -DUSE_CLOCK -fopenmp euclidean_mpi_omp.c timing.c -lm -o eud_mpi_omp`

Move it to the cloud folder: 
`cp eud_mpi_omp cloud && cd cloud`

Run the code, including the members of the population (e.g., N = 100), the number of processes (e.g., 4), and the number of threads (e.g., 2):
`mpirun -np 4 -hosts master,node1 -genv OMP_NUM_THREADS 2 ./eud_mpi_omp 100`

### Python/C pipeline


First, increase the user limit:
`ulimit -s unlimited`

Compile the code：

`gcc -fPIC -c euclidean_IO.c`  
`gcc -shared -o euclidean_IO.so euclidean_IO.o`

Update any desired parameters or variable in the python simulation script. Run the simulation script, calling the C code from Python:
`python simulation.py`

#### pipeline+OpenMP

create a folder 'lib' to store the C library file `mkdir lib`

set the default library path to that folder `export LD_LIBRARY_PATH=/home/ubuntu/lib`

compile the code `gcc -fPIC -c -fopenmp euclidean_omp_IO.c`

set the number of threads `export OMP_NUM_THREADS=8`

convert the C file to a library object `gcc -shared -o /home/ubuntu/lib/euclidean_omp_IO.so /home/ubuntu/euclidean_omp_IO.o -fopenmp`

call the C file from python `python3 simulation.py`

## Experiments and Discussion

### Strong Scaling (N=2000)

#### OpenMP (seconds)
| # of threads | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 
| --- | --- |---|---|---|---|---|---|---|
| 0| 0.104764 | 0.052442 | 0.0351157 | 0.0264497 | 0.0211322 | 0.0175604 | 0.0151527 | 0.0132662 |

![](./Visualizations/experiment_results/result-ss-omp-3.png)

OpenMP reaches a nearly optimal speedup for strong scaling. This indicates that the communication/synchronization cost is negligible in our case. This is because the program is embarrassingly parallel. The communication cost is limited to the I/O operation of splitting the task across the many threads. There is no communication/synchronization cost during the process that would greatly impact performance in non-embarrassingly parallel applications.  

#### MPI - two nodes (seconds)
| # of tasks | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8| 
| --- | --- |---|---|---|---|---|---|---|
| | 0.120043 | 0.059907 | 0.040406 |0.030658 | 0.023996  |0.019987 | 0.017079 | 0.015065 |

![](./Visualizations/experiment_results/result-ss-mpi-3.png)

We see an increasing speed-up that, expectedly, does not meet the theoretical expectation. There is increase I/O cost as we scale up across more nodes and cores. This is because we must transmit the data between processes. We observed over 6-times speed-up over 8 cores. However, it's notable that because there is no communication/synchronization within each task the speed-up plot is linear and not flattening off as we would expect in a non-embarrassingly parallel MPI implementation.  

#### Hybrid

2 cores, 2 thread (1 thread/core): 12.779103 s

2 cores, 4 threads (2 threads/core): 10.085558 s

4 cores, 4 threads (1 thread/core): 8.677512 s

4 cores, 8 threads (2 threads/core): 5.500008 s

8 cores, 8 threads (1 thread/core): 3.066303 s

8 cores, 16 threads (2 threads/core): 2.556881 s

![](./Visualizations/experiment_results/result-hybrid.png)

The hybrid OpenMP-MPI implementation shows an increasing speed-up with our number of threads and cores. We see our greatest speed-up when we increase the cores, not when we retain the number of cores and only increase our threads. For example, between 4 cores, 4 threads (1 thread per core) and 4 cores, 8 threads (two threads per core) we see a movement from around 2-times speed-up to 3-times speed up. If we compare 4 cores, 4 threads with 8 cores, 8 threads (so, both with 1 thread per core), we see even greater than doubling from around 2-times speed-up to over 5-times speed-up. We extrapolate that we do not see anywhere near linear speed-up with increased threads per core because we are retaining the overheads of I/O, communication, etc. involved with multiple cores. Our best attainable speed-up is around 7-times as we fully saturate our available CPUs. 

#### Pipeline - OMP (seconds) (N=14000)
| # of threads | 2 | 3 | 4 | 5 | 6 | 7 | 8| 
| --- | --- |---|---|---|---|---|---|
| |440| 382 | 354 | 334 | 321 | 317 | 313 |

![](./Visualizations/experiment_results/result-ss-pipeline-2.png)

The pipeline takes the Python script that generates the location of each simulated individual, exports that information to C, and pulls the Euclidean distance results back to Python at every time step. Note that we were able to implement this pipeline with our OpenMP results, but not with MPI. This would be a great next step for the project. We were anticipating increased I/O to be associated with the pipeline but saw that the speed-up of parallelizing in C was a worthwhile endeavor. We were then surprised to see the speed-up flattening out around 2-times. However, upon further reflection this makes sense. 

We saw that 92% of our Python code was parallelizable. This was back when our Euclidean distance calculation was taking 45 seconds (when it was massively inefficient in the serial Python code). It is notable that simply changing our program from a Python for-loop to a C for-loop decreased our computation time **significantly**. This was over 40-times - from a 45 second runtime to less than a second when moving from serial Python to serial C code. 

Now, the parallelized Euclidean distance operation is going so much faster that the serial portion of the code is likely overtaking the run-time. The hefty process moved from being the distance calculation to now the bottleneck of our plotting operations. This leads to a next step in implementation of addressing this new bottleneck using parallelization. 



### Weak Scaling

#### Serial (seconds)
| N/threads  | 500 | 2000 | 14000 | 26000 |
| ---------- | ----|------|-------|-------|
|  | 0.006557 | 0.1| 5.0395 | 17.422 |
 
#### OpenMP (seconds)
| N/threads  | 500 | 2000 | 14000 | 26000 |
| ---------- | ----|------|-------|-------|
| 2 | 0.00331253 | 0.052442 | 2.58289 | 8.77539 |
| 4 | 0.00167364 | 0.0264497 | 1.28463 | 4.40093 |
| 8 | 0.000937424 | 0.0132662 | 0.639876 | 2.21066 | 

![](./Visualizations/experiment_results/result-ws-omp.png)

We can see as that the speed-up grows with the size of the problem. As problem size increases, the synchronization overhead due to creation/control of threads becomes lower compared with the computing in each time step. It is interesting that weak scaling has better speed-up when looking at 8 threads. We see this as our blue bars are flat (2 threads) and our orange bars are flat (4 threads), but the green bars indicating 8 threads increase from around 7-times to 8-times speed-up. We see better speed-up for bigger problem sizes because lightweight tasks benefit less from parallelization due to their overall small computation time. 

#### MPI - single node (seconds)
| N/tasks  | 500 | 2000 | 14000 | 26000 |
| ---------- | ----|------|-------|-------|
| 2 | 0.003757  | 0.060158 | 2.980379 | 10.120353 |
| 4 | 0.001895 | 0.030686 | 1.475987 | 5.081657 |
| 8 | 0.000939 | 0.015082 | 0.742917 | 2.540809 |

![](./Visualizations/experiment_results/result-ws-mpi.png)

MPI is different from our OpenMP results as even with our largest problem size we do not see an increase in speed-up (the green bars are all about the same height). This can be attributed to the overheads (I/O, communication, synchronization) of MPI, which are larger as the problem size increases as we are not using shared memory. This counteracts the additional speed-up that we saw with OpenMP. 

#### Hybrid - 8 cores, 8 threads

| N | 500 | 2000 | 14000 | 26000 |
| ---------- | ----|------|-------|-------|
| | 0.015991 | 0.038632 | 0.815790 | 2.675975 |

![](./Visualizations/experiment_results/result-ws-hybrid.png)

For our hybrid weak scaling, we chose to run on 8 cores and 8 threads (1 thread/core) in order to observe its speed-up. This is because we saw with previous weak scaling examples that there was the most meaningful speed-up (if any) as we worked across more threads. We see really good speed-up here, though it flattens out with our two largest problem sizes of Boston and NYC. For 8 threads, this seems to be a point where the overheads that we have mentioned for OpenMP and MPI really impact the ability to see speed-up. This could lead to a recommendation to increase computational power beyond 8 threads once the simulation is run on areas as dense as cities. 

#### Pipeline - OMP (seconds)
| N/threads  | 500 | 2000 | 14000 | 26000 |
| ---------- | ----|------|-------|-------|
| 1 | 1.8 | 12.93 | 606 | 2105 |
| 2 | 1.63 | 9.64 | 440 | 1503 |
| 4 | 1.55 | 7.82 | 354 | 1208 |
| 8 | 1.76 | 8.07 | 313 | 1061 | 

![](./Visualizations/experiment_results/result-ws-pipeline.png)

With our pipeline, we do see increased speed-up with the problem size. This follows what was seen with OpenMP's weak scaling. Again, though, we do not see the same increases due to the pipeline's bottleneck within the Python code. We are attaining that same speed-up in the OpenMP section, but with the surrounding communication and slower Python operations the increase is stunted. Please see our discussion of strong scaling pipeline results for more information on this observation.

## Simulation Results

This simulation demonstrates the benefits of social distancing policies. Understanding that our model is very simplistic, we have simulated the effect of 75% of the population in a given community following social distancing guidelines (i.e., shelter-in-place).

Without social distancing policies, we observe that the pandemic comes to a peak comparatively quickly, and at that point **35%** of the population is infected with COVID-19. In a rural community (N = 500), that means that 175 people would be simultaneously infected, and in a metropolitan community such as New York City (N = 26,000), that means that over 9,000 people would be simultaneously infected. For reference, the average rural hospital has 76 beds available, and would service multiple towns, and the average urban hospital has 252 beds available ([Hatten and Connerton: Urban and rural hospitals: How do they differ?](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4191541/)).

After employing social distancing policies, we note a few important trends. First, we see that the course of the pandemic is significantly elongated. As we know, this would gain us valuable time for preparedness, although it means that we will be following the social distancing guidelines for longer periods of time. Second, at the time of peak, only **10%** of the population is infected. Finally, we notice an interesting second spike on the tail end of the pandemic. This is the "second wave" that many have been speaking of. 

![](./Visualizations/simulation-results/Infections.png) 


We have visualized our simulation for a small rural community (N = 500). The figure on the left shows the course of the pandemic **without social distancing**, and the figure on the right shows the course of the pandemic **with social distancing**.

![Alt Text](https://github.com/genevievelyons/covid-19-simulation/blob/master/Visualizations/simulation-results/nodist/nodist_sim_nomove.gif) ![Alt Text](https://github.com/genevievelyons/covid-19-simulation/blob/master/Visualizations/simulation-results/social_dist/social_dist_sim_nomove.gif)

Based on the results of this study, the convictions of many epidemiologists, and many studies supporting our findings, we believe that vehement declarations 
[such as Laura Ingraham claiming that there was no real scientific basis for social distancing](https://www.mediamatters.org/laura-ingraham/laura-ingraham-there-was-no-real-scientific-basis-social-distancing) are easily refutable.


## Conclusions and Recommendations

In conclusion, this task turned out to be a fantastic candidate for parallelization. This is partially because it is an embarrassingly parallel task, which lead to almost no communication/synchronization cost in our speed-up. We observed the best speed-up in the Euclidean distance calculation by using the Hybrid OpenMP + MPI solution.

Initially, we saw that 92% of the code was designated as parallelizable as we set our sights on improving the nested for-loop calculating Euclidean distance in Python. We greatly improved this operation. The simple act of moving the sequential operation from Python to C yielded over 40-times speed-up. Our further attempts at parallelizing the Python-C pipeline resulted in a cap of 2-times speed-up when compared to the serial C implementation. With this improvement, the initial "non-parallelizable" 8% of our code then became the most time-consuming portion of the simulation. This is specifically attributed to the plotting operation, which is hefty. Refer back to our discussion of strong scaling with our pipeline for more information. This conclusion lends itself to a great next extension for this simulation: parallelizing the graphing operation to allow for even more complex simulations of disease spread.

## References

We were inspired by the Washington Post article, [**"Why outbreaks like coronavirus spread exponentially, and how to “flatten the curve”**](https://www.washingtonpost.com/graphics/2020/world/corona-simulator/) by Harry Stevens. 

We also reference the work of [Philip Mocz](https://github.com/pmocz/coronavirusToySimulation) when building our simulation.
