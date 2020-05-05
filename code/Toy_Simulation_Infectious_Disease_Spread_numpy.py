#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:28:35 2020

@author: genevievelyons
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toy Simulation Model - Infectious Disease Spread

Created on Mon Mar 30 13:33:40 2020

@author: genevievelyons

Inspired by / adapted from: Philip Mocz, Princeton University - https://github.com/pmocz/coronavirusToySimulation

"""

#%%
%reset
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sklearn.metrics.pairwise import euclidean_distances

#Be sure to cd into the directory of this script!

#%%
##############################################################################################################################
##############################################################################################################################
##################### NO SOCIAL DISTANCING
##############################################################################################################################
##############################################################################################################################

#####################
# Set parameters
#####################

N = 500                    #population size
p_inf = 0.5                #probability of infection when in contact with an infected individual
r_inf = 0.05               #infection radius of an individual
t_inf = 1                   #time that an individual remains contagious
p_death = 0.02              #probability of death while infected


#isolation_fun = isolation function of time (= 1 means regular interaction level; = 0 means no interaction)
#isolation_fun = @(t) ones(size(t)); % constant function
#isolation_fun = @(t) exp(-0.1*t); % social distancing
#isolation_fun = @(t) (cos(2*t)+1)/2; % sinusoidal distancing
def isolation_fun(t): 
    return np.ones(1)


t = 0
dt = 0.1
Tfinal = 9.9 #end of simulation; set as 10 for final
p = 1


#%%
#####################
# Initial Conditions
#####################

#np.random.seed(123)

x = np.random.uniform(0,1,N)
y = np.random.uniform(0,1,N)

infected = np.zeros(len(x))
infected_t_counter = np.zeros(len(x))
immune = np.zeros(len(x))

#Infect 1 random person
infected[0] = 1

num_infected = []
num_dead = []
ts = []

#plt.scatter(x[infected == 0], y[infected == 0], s = 0.5, c = "g", label = "Not Infected")
#plt.scatter(x[infected == 1], y[infected == 1], s = 0.5, c = "r", label = "Infected")
#plt.legend()
#plt.show();

#%%
#####################
# Simulation - No Distancing
#####################

while t <= Tfinal:
        
    ###
    #Plot
    ###
    
    plt.cla()
    plt.scatter(x[infected == 0], y[infected == 0], s = 3, c = "b", label = "Not Infected")
    plt.scatter(x[immune == 1], y[immune == 1], s = 3, c = "g", label = "Immune")
    plt.scatter(x[infected == 1], y[infected == 1], s = 3, c = "r", label = "Infected")
    plt.title("t = " + str(round(t,1)))
    plt.legend(loc = 'lower right')
    plt.savefig("../Visualizations/simulation-results/nodist/nodist_" + str(int(round(t,1)*10)) + ".png", format = "png")
    
    
    ###
    #Distance between the individual pairs (bottleneck)
    ###
    
    
    
    r = euclidean_distances(list(zip(x,y)), list(zip(x,y)))
    contact = (r < r_inf) & (r > 0)
    
#    r = np.zeros((len(x), len(x)))
#    contact = np.zeros((len(x), len(x)))
    
#    for i in range(len(x)):
#        for j in range(len(x)):
#            r[i,j] = np.power(np.power(x[i] - x[j], 2) + np.power(y[i] - y[j], 2), 0.5)
#            contact[i,j] = (r[i,j] < r_inf) & (r[i,j] > 0)
    
    ###
    #Infect the individuals
    ###
            
    #Compute potential infections from contact
    infected_contact = contact * infected
    
    #Compute probability of being infected
    infected_contact = infected_contact * np.random.uniform(0,1,len(x)**2).reshape(len(x),len(x))
    
    #True infections upon contact
    infected_contact = np.max((infected_contact != 0) & (infected_contact < p_inf), axis = 1)
    
    #Exclude people who are immune 
    infected = ((infected_contact == True) & (immune == 0)) | (infected == True)
    
    
    ###
    #Update params for next time t
    ###
    
    
    #Velocity of movement
    vx = np.random.normal(size = len(x))*0.1
    vy = np.random.normal(size = len(y))*0.1

    #movement = location + unit time * velocity of x, y * isolation function of t
    x = x + dt*vx*isolation_fun(t)
    y = y + dt*vy*isolation_fun(t)
    
    #Calculate how long each individual has been infected; they recover when they have been infected for t_inf units of time
    infected_t_counter[infected] = infected_t_counter[infected] + dt    #Add the amount of time a patient has been sick
    recovered = infected_t_counter > t_inf                              #Recovered if they have been sick t_inf time
    infected[recovered] = False                                         #Recovered from infection pool
    infected_t_counter[recovered] = 0                                   #Reset timer for recovered patients
    immune[recovered] = 1                                               #Recovered patients are immune
    
    #Some patients die with probability p_death (p_death evenly distributed across the entire infection period)
    death = (infected == True) & (np.random.uniform(0,1,len(infected)) < p_death * dt/t_inf)
    
    x = x[death == False]
    y = y[death == False]
    vx = vx[death == False]
    vy = vy[death == False]
    infected = infected[death == False]
    infected_t_counter = infected_t_counter[death == False]
    immune = immune[death == False]
    
    #Calculate metrics
    ts.append(t)
    num_infected.append(np.sum(infected))
    num_dead.append(np.sum(death))
    
    #Advance Time
    t = t + dt
    p = p + 1
    
    print("Starting t = " + str(t) + " at " + str(datetime.datetime.now().strftime("%H:%M:%S")))
    
#%%
##############################################################################################################################
##############################################################################################################################
##################### SOCIAL DISTANCING
##############################################################################################################################
##############################################################################################################################

#####################
# Set parameters
#####################

#N = 500                    #population size
#p_inf = 0.5                #probability of infection when in contact with an infected individual
#r_inf = 0.05               #infection radius of an individual
#t_inf = 1                   #time that an individual remains contagious
#p_death = 0.02              #probability of death while infected


#isolation_fun = isolation function of time (= 1 means regular interaction level; = 0 means no interaction)
#isolation_fun = @(t) ones(size(t)); % constant function
#isolation_fun = @(t) exp(-0.1*t); % social distancing
#isolation_fun = @(t) (cos(2*t)+1)/2; % sinusoidal distancing
isolation_fun = np.random.binomial(1, 0.25, N)


t = 0
dt = 0.1
Tfinal = 9.9 #end of simulation; set as 10 for final
p = 1


#%%
#####################
# Initial Conditions
#####################

#np.random.seed(123)

x = np.random.uniform(0,1,N)
y = np.random.uniform(0,1,N)

infected = np.zeros(len(x))
infected_t_counter = np.zeros(len(x))
immune = np.zeros(len(x))

#Infect 1 random person
infected[0] = 1

num_infected_sd = []
num_dead_sd = []
ts = []

#plt.scatter(x[infected == 0], y[infected == 0], s = 0.5, c = "g", label = "Not Infected")
#plt.scatter(x[infected == 1], y[infected == 1], s = 0.5, c = "r", label = "Infected")
#plt.legend()
#plt.show();

#%%
#####################
# Simulation - No Distancing
#####################

while t <= Tfinal:
        
    ###
    #Plot
    ###
    
    plt.cla()
    plt.scatter(x[infected == 0], y[infected == 0], s = 3, c = "b", label = "Not Infected")
    plt.scatter(x[immune == 1], y[immune == 1], s = 3, c = "g", label = "Immune")
    plt.scatter(x[infected == 1], y[infected == 1], s = 3, c = "r", label = "Infected")
    plt.title("t = " + str(round(t,1)))
    plt.legend(loc = 'lower right')
    plt.savefig("../Visualizations/simulation-results/social_dist/social_dist_" + str(int(round(t,1)*10)) + ".png", format = "png")
    
    
    ###
    #Distance between the individual pairs (bottleneck)
    ###
    
    r = euclidean_distances(list(zip(x,y)), list(zip(x,y)))
    contact = (r < r_inf) & (r > 0)
    
#    r = np.zeros((len(x), len(x)))
#    contact = np.zeros((len(x), len(x)))
#    
#    for i in range(len(x)):
#        for j in range(len(x)):
#            r[i,j] = np.power(np.power(x[i] - x[j], 2) + np.power(y[i] - y[j], 2), 0.5)
#            contact[i,j] = (r[i,j] < r_inf) & (r[i,j] > 0)
    
    ###
    #Infect the individuals
    ###
            
    #Compute potential infections from contact
    infected_contact = contact * infected
    
    #Compute probability of being infected
    infected_contact = infected_contact * np.random.uniform(0,1,len(x)**2).reshape(len(x),len(x))
    
    #True infections upon contact
    infected_contact = np.max((infected_contact != 0) & (infected_contact < p_inf), axis = 1)
    
    #Exclude people who are immune 
    infected = ((infected_contact == True) & (immune == 0)) | (infected == True)
    
    
    ###
    #Update params for next time t
    ###
    
    
    #Velocity of movement
    vx = np.random.normal(size = len(x))*0.1
    vy = np.random.normal(size = len(y))*0.1

    #movement = location + unit time * velocity of x, y * isolation function of t
    x = x + dt*vx*isolation_fun
    y = y + dt*vy*isolation_fun
    
    #Calculate how long each individual has been infected; they recover when they have been infected for t_inf units of time
    infected_t_counter[infected] = infected_t_counter[infected] + dt    #Add the amount of time a patient has been sick
    recovered = infected_t_counter > t_inf                              #Recovered if they have been sick t_inf time
    infected[recovered] = False                                         #Recovered from infection pool
    infected_t_counter[recovered] = 0                                   #Reset timer for recovered patients
    immune[recovered] = 1                                               #Recovered patients are immune
    
    #Some patients die with probability p_death (p_death evenly distributed across the entire infection period)
    death = (infected == True) & (np.random.uniform(0,1,len(infected)) < p_death * dt/t_inf)
    
    x = x[death == False]
    y = y[death == False]
    vx = vx[death == False]
    vy = vy[death == False]
    infected = infected[death == False]
    infected_t_counter = infected_t_counter[death == False]
    immune = immune[death == False]
    isolation_fun = isolation_fun[death == False]
    
    #Calculate metrics
    ts.append(t)
    num_infected_sd.append(np.sum(infected))
    num_dead_sd.append(np.sum(death))
    
    #Advance Time
    t = t + dt
    p = p + 1
    
    print("Starting t = " + str(t) + " at " + str(datetime.datetime.now().strftime("%H:%M:%S")))


#%%

#Plot Infections
plt.cla()
plt.plot(ts, np.array(num_infected) / N, label = "No Social Distancing")
plt.plot(ts, np.array(num_infected_sd) / N, label = "With Social Distancing")
plt.title("Percent of Population Infected at time t")
plt.xlabel("Time (t)")
plt.legend()
plt.savefig("../Visualizations/simulation-results/Infections.png", format = "png")

#Plot Deaths
plt.cla()
plt.plot(ts, np.cumsum(num_dead), label = "No Social Distancing")
plt.plot(ts, np.cumsum(num_dead_sd), label = "With Social Distancing")
plt.title("Number Dead at time t")
plt.xlabel("Time (t)")
plt.legend()
plt.savefig("../Visualizations/simulation-results/Deaths.png", format = "png")



