## Kunal Deshmukh + Eric Tjon

import random
import pandas as pd


def mutate(sequence):
  option = random.randint(0,1)
  option = 1
  if option == 0:
    pos1 = random.randint(0,len(sequence)-1)
    pos2 = random.randint(0,len(sequence)-1)  
    temp = sequence[pos2]
    sequence[pos2] = sequence[pos1]
    sequence[pos1] = temp
    return sequence
  elif option == 1 :
    pos1 = random.randint(2,len(sequence)-3)
    pos2 = random.randint(pos1,len(sequence)-2)  
    sub = sequence[pos1:pos2]
    sub = sub[::-1]
    new_seq = pd.concat([pd.concat([sequence[:pos1],sub]),sequence[pos2:]])
    return new_seq