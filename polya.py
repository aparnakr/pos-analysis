from math import *
from itertools import *
from decimal import Decimal
#from np import *


num_rounds = 3
X_0 = [1000 for i in range(64)]
# for i in range(64):
# 	X_0 = [1000, 1212, 1332, 2110, 1333, 1412, 1990]
num_validators = len(X_0)

# This calculates the multinomial i.e 
#  n!/ (y1! * y2! .. * ym!)
def multinomial(arr_len, num, arr_denom):
	if sum(arr_denom) != num:
		return 0
	denom = 1
	for e in arr_denom:
		denom *= factorial(e)
	return Decimal(factorial(num))/Decimal(denom)

# This calculates x * (x + 1) .. * (x + (n - 1))
def rev_factorial(x, n):
	i = 0
	prod = 1
	while i < n:
		prod = prod * (x + i)
		i += 1
	return prod

# This calculates prob(x_j = y_j + x_0, for j = 1.. m)
def prob_win_vector(n, m, Y, X_0):
	if sum(Y) != n:
		return 0
	product = 1
	for i in range(m):
		if Y[i] != 0:
			product *= rev_factorial(X_0[i], Y[i])
	denom = rev_factorial(sum(X_0), n)
	coeff = multinomial(m, n, Y)
	#print("product",product)
	return Decimal(product * coeff) / Decimal(denom)

def multichoose(k, objects):
    """n multichoose k multisets from the list of objects.  n is the size of
    the objects."""
    j,j_1,q = k,k,k  # init here for scoping
    r = len(objects) - 1
    a = [0 for i in range(k)] # initial multiset indexes
    while True:
        yield [objects[a[i]] for i in range(0,k)]  # emit result
        j = k - 1
        while j >= 0 and a[j] == r: j -= 1
        if j < 0: break  # check for end condition
        j_1 = j
        while j_1 <= k - 1:
            a[j_1] = a[j_1] + 1 # increment
            q = j_1
            while q < k - 1:
                a[q+1] = a[q] # shift left
                q += 1
            q += 1
            j_1 = q


# This returns all permutations of putting balls in the boxes 
def all_sets(boxes, balls):
	# rng = list(range(balls + 1)) * boxes
	# return set(i for i in permutations(rng, boxes) if sum(i) == balls)
	sets = set()
	all_boxes = [i for i in range(boxes)]
	for s in multichoose(balls, all_boxes):
		row = [0 for i in range (boxes)]
		for e in s:
			row[e] +=1
		sets.add(tuple(row))
	return sets



# Helper function for i_exactly_x_stake such that it returns true
# if the X[j] validator has exactly s tokens
def f(X, s, j):
	return X[j] == s

# Returns the probability of the i^th validator having exactly p 
# proportion of the stake 
# remeber to input p in form of 4.0/5 
def i_exact_stake(X_0, p, n, m, i):
	t_n = sum(X_0) + n
	s = t_n * p
	prob = 0
	for Y in all_sets(m, n):
		y_x = [Y[j] + X_0[j] for j in range(m)]
		prob += f(y_x, s, i)* prob_win_vector(n, m, Y, X_0)
	return prob

# Helper function for prob_any_threshold such that it returns true
# if any of validator has >= s tokens
def g(X, s):
	for x in X:
		if x >= s:
			return True
	return False

# Returns the probability of the any validator having >= p 
# proportion of the stake 
# remeber to input p in form of 4.0/5 
def prob_any_threshold(X_0, p, n, m):
	t_n = sum(X_0) + n
	s = t_n * p
	prob = 0
	sets = all_sets(m, n)
	for Y in sets:
		y_x = [Y[j] + X_0[j] for j in range(m)]
		prob += g(y_x, s)* prob_win_vector(n, m, Y, X_0)
	return prob

# Returns the expected stake composition vector of the validators
# after n rounds. 
def expected_value(X_0, n, m):
	expected = X_0
	for Y in all_sets(m, n):
		Y_i = [prob_win_vector(n, m, Y, X_0)*y for y in Y]
		expected = [expected[i] + Y_i[i] for i in range(m)]
	return expected

# check to see that the probabilities are written out right. 
# for Y in all_sets(3,4):
# 	#print(Y, prob_win_vector(4, 3, Y, [1, 2, 1]))
# 	prob+= prob_win_vector(4, 3, Y, [1, 2, 1])
#print(expected_value(X_0, num_rounds, num_validators))
print(prob_any_threshold(X_0, Decimal(1.0/3), num_rounds,num_validators))
