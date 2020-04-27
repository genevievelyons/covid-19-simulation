# Flattening the Curve: A Simulation Study of the Spread of COVID-19

Note: This is a toy simulation of the spread of an infectious disease, and is not intended to represent any particular geographic location or use parameters that are scientifically accurate for COVID-19.

## Running the Euclidean Distance Code

The code takes argument of N members of the population (defaults to 200 if no number is given)

I ran it on a t2.2xlarge AWS Ubuntu 16.04 instance. You will need to upload both `euclidean.c` and `timing.h`.

First, increase the limit:
`ulimit -s unlimited`

Compile the code:
`gcc -DUSE_CLOCK euclidean.c -lm -o euclidean`

Run the code, including the members of the population (e.g., N = 100):
`./euclidean 100`

The elapsed time will be printed after the results.

### References

We were inspired by the Washington Post article, [**"Why outbreaks like coronavirus spread exponentially, and how to “flatten the curve”**](https://www.washingtonpost.com/graphics/2020/world/corona-simulator/) by Harry Stevens. 

We also reference the work of [Philip Mocz](https://github.com/pmocz/coronavirusToySimulation) when building our simulation.
