# Kunal Deshmukh + Eric Tjon
import random
import pandas as pd

def crossover(dna):
    dna_complement = []
    dna = list(dna)
    dna = map(int,dna) 
    for ele in dna:
        dna_complement.append(str(len(dna)-1-ele))
    dna = map(str,dna)
    dna_complement = ''.join(dna_complement)
    pos = random.randint(0,len(dna)-1)
    cross_len = random.randint(0,len(dna)-pos)
   
    curr_pos = pos 
    for i in range(cross_len):
        dna[curr_pos] = dna_complement[curr_pos]
        curr_pos += 1
    dna = ''.join(dna)
  
    return(pd.Series(map(str,dna)))
