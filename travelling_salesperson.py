import pandas as pd
import numpy as np
import random
import ga_crossover
import ga_mutation
import sys

POPULATION_SIZE = 100
GENERATIONS = 50
PERCENT_POPULATION_TO_SELECT = 40
RESULTS_FILE_NAME = "KUNAL_DESHMUKH_GA_TS_Result.txt"
PROGRESS_FILE_NAME = "KUNAL_DESHMUKH_GA_TS_Info.tx"
DISTANCE_MATRIX_PATH = "./Data Sets/TS_Distances_Between_Cities.csv"

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
    for _, value in kwargs.iteritems():
        a_matrix = value
    for i in range(len(individual)-1):
            a += a_matrix[individual[i]][individual[i+1]]
    return a


def evaluate_fitness(population,adjacency_matrix,percent_population_to_return = 40 ,certainity = 100):
    """ This method evaluates the fitness of a population and returns indices of % of population 
    in "population to return with certainity passed as "certainity" """
    assert percent_population_to_return >= 1 and percent_population_to_return <= 99 ,\
    " percent population to return needs to be greater than 1\% and less than 100\%. provided: %r" % percent_population_to_return
    assert certainity > 0 and certainity <=100 , \
    "certainity needs to be more than 0 and less than 100. provided: %r" % no_of_genes_per_individual
    distance = population.apply(calculate_distance,a_matrix= adjacency_matrix, axis=1)
    order =  np.argsort(distance) 
    no_to_return = int(len(order)*(percent_population_to_return/100.0))
    best = order[:no_to_return]
    return best


def is_valid(individual):
    if len(individual) != len(set(individual)):
        return False
    else :
        return True

def crossover_and_mutate(individual):
    """ This method tries to mimic biological operations of crossover and mutation
        it accespts each individual in a population as input in the form of
         pandas series. Returns mutated individual.
    """
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

def read_dataset(path):
    df = pd.read_csv(path)
    citi_names =  df.iloc[:, 0].dropna().values
    df = df.drop(df.columns[0], axis=1)
    return df.values,citi_names

if __name__ == '__main__':
    F = open(PROGRESS_FILE_NAME,"w") 

    #read distances between cities
    distance_matrix,citi_names = read_dataset(DISTANCE_MATRIX_PATH)

    # create initial population
    population = population_generator(POPULATION_SIZE,len(citi_names))
    best_candidate = []
    for iter in range(GENERATIONS):
        F.write("iteration : "+str(iter)+'\n')
        # call fitness function
        fit_population = evaluate_fitness(population,distance_matrix,PERCENT_POPULATION_TO_SELECT)
        
        # select fitness
        F.write("Population size : "+str(population.shape[0])+'\n')
        population =  population.ix[fit_population]
        population.index = range(len(population))
        distance = population.apply(calculate_distance,a_matrix= distance_matrix, axis=1)
        F.write("Average fitness score : "+str(distance.mean())+'\n')
        F.write("Median fitness score : "+str(distance.median())+'\n')
        F.write( "STD of fitness scores : "+str(distance.std())+'\n')
        F.write( "Size of the selected subset of the population : "+str(population.shape[0])+'\n\n')
        argsmin = distance.idxmin()
        best_candidate = population.ix[argsmin]
        #perform crossover and mutaton
        population = population.apply(crossover_and_mutate,axis=1)
        children_to_add =  POPULATION_SIZE - len(population)
        # generate_new_population()
        for i in range(children_to_add):
            choice = random.randint(0,len(population)-1)
            population = population.append(crossover_and_mutate(population.iloc[choice]),ignore_index=True)
        #check stopping condition
    F.close()
    best_candidate = best_candidate.values
    F = open(RESULTS_FILE_NAME,"w") 
    for city in best_candidate:
        F.write(str(city)+" "+str(citi_names[city])+'\n')
    F.close()
