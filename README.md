# Polya's urn simulations 
The proof-of-stake system we model is one where rewards given out at every round is a constant amount. For the a chosen number of rounds, we calculate the probability of any validator reaching the 1/3 threshold. We also calculate the expected distribution of all the validators after $n$ rounds.

## Calculating the probability that any validator reaches the 1/3 stake threshold:
1. Clone the repository
2. Run `python threshold.py` 
3. Input the parameters as shown.
### Case 1: Initial stake is evenly distributed amongst validators
Example: <br />
The number of rounds you want to run the simulation for <br />
**100** <br />
Type of reward scheme -  <br />
    Type 1 for reward evenly distributed amongst all the validators <br />
    Type 2 for a skewed distribution <br />
**1** <br />
Ratio of stake to rewards of each validator <br />
**10** <br />
Number of validators <br />
**64** <br />

### Case 2: Initial stake distributed amongst validators is skewed
The number of rounds you want to run the simulation for 
**100**
Type of reward scheme - 
 Type 1 for reward evenly distributed amongst all the validators 
 Type 2 for a skewed distribution 
**2**
Proportion of stake the highest stakeholder has
**0.4**
Number of validators 
**64
            
            
            

  
