from math import *
from itertools import *
from decimal import *

num_rounds = 750
# Note, technically number of validators needs to be greater than 3 for this
# implementation to be technically correct. Otherwhise I have to include adding back in
# 3 people all getting to 1/3rd
validators = [8] + [Decimal(10) for i in range(110)] + [Decimal(500)]
num_validators = len(validators)
getcontext().prec = 28

def main(validators, num_rounds):
    validators = list(validators) #Don't mutate
    for _ in range(num_rounds):
        total_stake = sum(validators)
        validators = [validator + (validator/total_stake) for validator in validators]
    return validators

print("Expected distribution of provided", num_validators, "validators after", num_rounds)
import time
t0 = time.clock()
distribution = main(validators, num_rounds)
print("calculation complete")
tf = time.clock()
print(distribution)
print(str(tf- t0) +" seconds process time to calculate")
