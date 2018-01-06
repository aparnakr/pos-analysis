from math import *
from itertools import *
from decimal import *

num_rounds = 500
validators = [10 for i in range(110)] + [500]
total_stake = Decimal(sum(validators))
num_validators = len(validators)
bound = 1/3
getcontext().prec = 28

# Compute (start + length - 1)! / (start - 1)!
fact_memo = {}
def modified_factorial(start, length):
    if (start, length) in fact_memo:
        return fact_memo[(start, length)]
    result = 1
    for i in range(0, length):
        result *= (start + i)
    fact_memo[(start, length)] = result
    return result

# Compute binomial coefficient
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

# Compute binomial coefficient
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

def main():
    # check trivial solutions
    MAX = 0
    for validator in validators:
        if validator / total_stake > bound:
            return 1.0
        if validator > MAX:
            MAX = validator
    if ((MAX + num_rounds) / total_stake) < bound:
        return 0.0

    TOTAL = 0
    for validator in validators:
        TOTAL += solve_validator(validator, total_stake - validator)
    print("First order approximation complete")
    print("First order probability of failure =",TOTAL*100, "%")
    for i in range(len(validators)):
        for j in range(i):
            TOTAL -= solve_validator_pair(validators[i], validators[j],
                total_stake - validators[i] - validators[j])
    return TOTAL

def solve_validator(value, rest):
    minimum_number_of_selections = int(ceil((num_rounds / Decimal(3)) +
        ((rest - 2*value) / Decimal(3))))
    if minimum_number_of_selections > num_rounds:
        return 0
    denominator = modified_factorial(value+rest, num_rounds)
    total_probability = 0
    for j in range(minimum_number_of_selections, num_rounds+1):
        ways = binom_coefficient(num_rounds, j)
        probability = modified_factorial(value, j) * modified_factorial(rest, num_rounds - j)
        total_probability += ways*probability
    return total_probability / denominator

def solve_validator_pair(value1, value2, rest):
    minimum_number_of_selections1 = int(ceil((num_rounds / Decimal(3)) +
        ((rest - 2*value1) / Decimal(3))))
    minimum_number_of_selections2 = int(ceil((num_rounds / Decimal(3)) +
        ((rest - 2*value2) / Decimal(3))))
    if minimum_number_of_selections1 + minimum_number_of_selections2 > num_rounds:
        return 0
    denominator = modified_factorial(value1 + value2 + rest, num_rounds)
    total_probability = 0
    for i in range(minimum_number_of_selections1, num_rounds+1 - minimum_number_of_selections2):
        for j in range(minimum_number_of_selections2, num_rounds+1 - i):
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
