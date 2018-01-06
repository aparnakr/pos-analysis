from math import *
from itertools import *
from decimal import *

num_rounds = 750
# Note, technically number of validators needs to be greater than 3 for this
# implementation to be technically correct. Otherwhise I have to include adding back in
# 3 people all getting to 1/3rd
validators = [Decimal(10) for i in range(110)] + [Decimal(500)]
total_stake = Decimal(sum(validators))
num_validators = len(validators)
threshold = 1/Decimal(3)
getcontext().prec = 28

# Computes (start + length - 1)! / (start - 1)!
fact_memo = {}
def modified_factorial(start, length):
    if (start, length) in fact_memo:
        return fact_memo[(start, length)]
    result = 1
    for i in range(0, length):
        result *= (start + i)
    fact_memo[(start, length)] = result
    return result

# Computes binomial coefficient
binom_memo = {}
def binom_coefficient(n,c):
    if (n,c) in binom_memo:
        return binom_memo[(n,c)]
    result = 1
    for i in range(n - c + 1, n+1):
        result *= i
    for i in range(1, c+1):
        result //= i
    binom_memo[(n,c)] = result
    return result

# Compute trinomial coefficient
trinom_memo = {}
def trinom_coefficient(n,c1,c2):
    if (n,c1,c2) in trinom_memo:
        return trinom_memo[(n,c1,c2)]
    result = 1
    for i in range(n - c1 - c2 + 1, n+1):
        result *= i
    for i in range(1, c1+1):
        result //= i
    for i in range(1, c2+1):
        result //= i
    trinom_memo[(n,c1,c2)] = result
    return result

Y = [int(ceil(threshold * (total_stake + num_rounds) - validator)) for validator in validators]

def main():
    # check trivial solutions
    MAX = max(validators)
    if (MAX / (total_stake + num_rounds)) > threshold:
        return 1.0
    if ((MAX + num_rounds) / total_stake) < threshold:
        return 0.0

    TOTAL = 0
    for validator in range(len(validators)):
        TOTAL += solve_validator(validators[validator],
            total_stake - validators[validator], Y[validator])
    print("First order approximation complete")
    print("First order probability of failure =",TOTAL*100, "%")
    for i in range(len(validators)):
        for j in range(i):
            TOTAL -= solve_validator_pair(validators[i], validators[j],
                total_stake - validators[i] - validators[j], Y[i], Y[j])
    return TOTAL

# TODO Store denominator and minimum_number_of_selections calculations.
def solve_validator(value, rest, min_num_selections):
    if min_num_selections > num_rounds:
        return 0 # Make sure its possible to have a solution
    denominator = modified_factorial(value+rest, num_rounds)
    total_probability = 0
    for j in range(min_num_selections, num_rounds+1):
        ways = binom_coefficient(num_rounds, j)
        probability = modified_factorial(value, j) * modified_factorial(rest, num_rounds - j)
        total_probability += ways*probability
    return total_probability / denominator

def solve_validator_pair(value1, value2, rest, min_selection1, min_selection2):
    if min_selection1 + min_selection2 > num_rounds:
        return 0 # Make sure its possible to have a solution
    denominator = modified_factorial(value1 + value2 + rest, num_rounds)
    total_probability = 0
    for i in range(min_selection1, num_rounds+1 - min_selection2):
        for j in range(min_selection2, num_rounds+1 - i):
            assert i + j <= num_rounds
            ways = trinom_coefficient(num_rounds, i, j)
            probability = (modified_factorial(value1, i) *
                modified_factorial(value2, j) * modified_factorial(rest, num_rounds - i - j))
            total_probability += ways*probability
    return total_probability / denominator

print("Computing the probability that the system fails for the given set of %s validators with %s rounds." % (num_validators, num_rounds))

import time
t0 = time.clock()
print("Probability of failure is", 100*main(), "%")
print(str(time.clock() - t0) +" seconds process time to complete")
