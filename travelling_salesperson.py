import pandas as pd
import random

def population_generator(no_of_individuals = 1000,no_of_genes_per_individual = 10):
    """ Generates a population for TSP with n no of population """
    
    assert no_of_individuals >=2 , "no_of_individuals should be >=2 provided: %r" % no_of_individuals
    assert no_of_genes_per_individual >= 3 , "numbet of genes should be >= 3 provided: %r" % no_of_genes_per_individual
    
    population = []
    for i in range(no_of_individuals):
        individual = random.sample(range(0,no_of_genes_per_individual),no_of_genes_per_individual)
        population.append(individual)
    return pd.DataFrame(population)


def evaluate_fitness(population,adjacency_matrix,percent_population_to_return = 80 ,certainity = 100):
    """ This method evaluates the fitness of a population and returns indices of % of population 
    in "population to return with certainity passed as "certainity" """

    assert percent_population_to_return >= 1 and percent_population_to_return <= 99 ,\
    " percent population to return needs to be greater than 1\% and less than 100\%. provided: %r" % percent_population_to_return
    assert certainity > 0 and certainity <=100 , \
    "certainity needs to be more than 0 and less than 100. provided: %r" % no_of_genes_per_individual
    
    



if __name__ == '__main__':
    # create initial population
    population = population_generator()

    #read distances between cities
    with open('adjacency_matrix.txt') as f:
        lines = f.readlines()
    cities = int(lines[0])
    distance_matrix = []
    for i in range(cities):
        distance_matrix.append(list(map(int,lines[i+1].strip().split(' '))))
    # call fitness function
    evaluate_fitness(population,distance_matrix)
    # generate_new_population()