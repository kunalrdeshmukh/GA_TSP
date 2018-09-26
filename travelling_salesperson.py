import pandas as pd
import numpy as np
import random
import ga_crossover
import ga_mutation


def population_generator(no_of_individuals = 1000,no_of_genes_per_individual = 10):
    """ Generates a population for TSP with n no of population """
    
    assert no_of_individuals >=2 , "no_of_individuals should be >=2 provided: %r" % no_of_individuals
    assert no_of_genes_per_individual >= 3 , "numbet of genes should be >= 3 provided: %r" % no_of_genes_per_individual
    
    population = []
    for i in range(no_of_individuals):
        individual = random.sample(range(0,no_of_genes_per_individual),no_of_genes_per_individual)
        population.append(individual)
    return pd.DataFrame(population)


def calculate_distance(individual,**kwargs):
    a = 0
    # if (len(individual) != len(set(individual))):
    #     a += 100    # penalty for a duplicate element in a list
    for _, value in kwargs.iteritems():
        a_matrix = value
    # print individual
    for i in range(len(individual)-1):
            a += a_matrix[individual[i]][individual[i+1]]
    return a


def evaluate_fitness(population,adjacency_matrix,percent_population_to_return = 80 ,certainity = 100):
    """ This method evaluates the fitness of a population and returns indices of % of population 
    in "population to return with certainity passed as "certainity" """
    assert percent_population_to_return >= 1 and percent_population_to_return <= 99 ,\
    " percent population to return needs to be greater than 1\% and less than 100\%. provided: %r" % percent_population_to_return
    assert certainity > 0 and certainity <=100 , \
    "certainity needs to be more than 0 and less than 100. provided: %r" % no_of_genes_per_individual
    distance = population.apply(calculate_distance,a_matrix= adjacency_matrix, axis=1)
    print "avg distance : "+str(reduce(lambda x, y: x + y, distance) / len(distance))
    order =  np.argsort(distance) 
    no_to_return = int(len(order)*(percent_population_to_return/100.0))
    return order[:no_to_return]
    # TODO: use certainity to select "best" candidate with probablity.

def is_valid(individual):
    if len(individual) != len(set(individual)):
        return False
    else :
        return True

def crossover_and_mutate(individual):
    choice = random.randint(0,100)
    if choice % 2 == 0:
        individual = ga_crossover.crossover(individual)
    if choice % 3 == 0:
        individual = ga_mutation.mutate(individual)
    # TODO : do this in a optimal way
    if is_valid(individual):
        return individual
    else :
        return crossover_and_mutate(individual)

if __name__ == '__main__':
    # create initial population
    population_size = 10
    population = population_generator(population_size,8)
    
    #read distances between cities
    with open('adjacency_matrix.txt') as f:
        lines = f.readlines()
    cities = int(lines[0])
    distance_matrix = []
    for i in range(cities):
        distance_matrix.append(list(map(int,lines[i+1].strip().split(' '))))
    
    for iter in range(100):
        print "iteration : "+str(iter)
        # call fitness function
        fit_population = evaluate_fitness(population,distance_matrix)
        
        # select fitness
        population =  population.ix[fit_population]
        population.index = range(len(population))
        #perform crossover and mutaton
        population = population.apply(crossover_and_mutate,axis=1)
        children_to_add =  population_size - len(population)
        # generate_new_population()
        for i in range(children_to_add):
            choice = random.randint(0,len(population)-1)
            population = population.append(crossover_and_mutate(population.iloc[choice]),ignore_index=True)
    print population
        #check stopping condition