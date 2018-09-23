## Kunal Deshmukh + Eric Tjon

import random


def mutate(sequence):
  # TODO : do something else than just pointwise
  pos1 = random.randint(0,len(sequence)-1)
  pos2 = random.randint(0,len(sequence)-1)
  temp = sequence[pos2]
  sequence[pos2] = sequence[pos1]
  sequence[pos1] = temp
  return sequence