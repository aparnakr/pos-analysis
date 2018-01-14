# Calculates the probability that the provided validator set gets
# someone above the threshold.
from math import *
import random
from decimal import *

num_rounds = 1000
debug = False
# Enter your own validator set if you want to use a specific set
validators = []
stake_reward_per_round = 1
threshold = 1 / Decimal(3)
getcontext().prec = 15
getcontext().Emax = 1000000
# Otherwhise fill in one set of parameters,
# either set generate_type to uniform, constant, or normal (for normal disr)
generate_type = "constant"
num_validators = 64
# CONSTANT DISTR PARAMETERS:
constant_value = 10
# UNIFORM RANDOM DISTR PARAMETERS: Format is (min, max), inclusive bounds
uniform_range = (0,200)
# NORMAL  DISTR PARAMETERS: Format is (mean, standard deviation)
# note negative numbers will not be generated
norm_dist_parameters = (45, 15)
# SKEW PARAMETERS
skewed_percentage = .3

generate = (validators == [])
if generate:
    generate_type = generate_type.lower().strip()
    if generate_type == "constant":
        validators = [constant_value] * num_validators
    elif generate_type == "uniform":
        validators = [random.uniform(uniform_range[0],uniform_range[1]) for x in range(num_validators)]
    elif generate_type == "normal":
        validators = [-1] * num_validators
        for x in range(len(validators)):
            while validators[x] < 0:
                validators[x] = random.normalvariate(norm_dist_parameters[0],norm_dist_parameters[1])
    elif generate_type == "skew":
        validators = [random.uniform(uniform_range[0],uniform_range[1]) for x in range(num_validators-1)]
        validators.append(skewed_percentage * sum(validators) / (1 - skewed_percentage))
for x in range(len(validators)):
    validators[x] = Decimal(validators[x] / stake_reward_per_round)
total_stake = Decimal(sum(validators))
if debug:
    print("validators = ", validators)
    print(total_stake)

#If a probability is less than epsilon, skip consequent calculations for that validator / pair
epsilon = Decimal(10**-15)

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

def main(num_rounds, second_order=True):
    Y = [int(ceil(threshold * (total_stake + num_rounds) - validator)) for validator in validators]
    # check trivial solutions
    MAX = max(validators)
    if (MAX / (total_stake + num_rounds)) > threshold:
        return 1.0
    if ((MAX + num_rounds) / total_stake) < threshold:
        return 0.0

    TOTAL = 0
    for validator in range(len(validators)):
        TOTAL += solve_validator(validators[validator],
            total_stake - validators[validator], Y[validator], num_rounds)
    print("First order approximation complete")
    # print("First order probability of failure =",TOTAL*100, "%")
    if not second_order:
        return TOTAL
    for i in range(len(validators)):
        for j in range(i):
            TOTAL -= solve_validator_pair(validators[i], validators[j],
                total_stake - validators[i] - validators[j], Y[i], Y[j], num_rounds)
    print("Second order approximation complete")
    return TOTAL

# TODO Store denominator and minimum_number_of_selections calculations.
def solve_validator(value, rest, min_num_selections, num_rounds):
    if min_num_selections > num_rounds:
        return 0 # Make sure its possible to have a solution
    denominator = modified_factorial(value+rest, num_rounds)
    total_probability = 0
    local_eps = epsilon * denominator
    for j in range(min_num_selections, num_rounds+1):
        ways = binom_coefficient(num_rounds, j)
        probability = modified_factorial(value, j) * modified_factorial(rest, num_rounds - j)
        cur = ways*probability
        total_probability += ways*probability
        if cur < local_eps and j > num_rounds/2:
            break
    return total_probability / denominator

def solve_validator_pair(value1, value2, rest, min_selection1, min_selection2, num_rounds):
    if min_selection1 + min_selection2 > num_rounds:
        return 0 # Make sure its possible to have a solution
    denominator = modified_factorial(value1 + value2 + rest, num_rounds)
    local_eps = epsilon * denominator
    total_probability = 0
    for i in range(min_selection1, num_rounds+1 - min_selection2):
        for j in range(min_selection2, num_rounds+1 - i):
            assert i + j <= num_rounds
            ways = trinom_coefficient(num_rounds, i, j)
            probability = (modified_factorial(value1, i) *
                modified_factorial(value2, j) * modified_factorial(rest, num_rounds - i - j))
            total_probability += ways*probability
            if cur < local_eps and j > (num_rounds - i)/2:
                break
    return total_probability / denominator

print("Computing the probability that the system fails for the given set of %s validators with %s rounds." % (num_validators, num_rounds))
import time
t0 = time.clock()
print("Probability of failure is", 100*main(num_rounds), "%")
print(str(time.clock() - t0) +" seconds process time to complete")