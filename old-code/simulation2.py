import pickle
import csv
from pylab import *
from random import *
import numpy as np

#Things to do, change the amount of bonded stake, change myBond, change, inflation quotient, randomize transaction fees? 
fig, ax = subplots()
colors = ["red", "blue", "green"]
inflation = [1, 7, 14]


for k in range(100):

	for i in range(3):
		t = 0; #number of blocks
		total = 87936854.71875 #current ETH supply in the market
		bonded = total/10.0 #amount of ETH bonded
		myBond = bonded * 0.25 # adversary's inital stake (I am the adversary)
		fees = 0.3 #0.161/163.05 # ?
		infl_quotient = inflation[i] # from range 1% to 14%
  		print(infl_quotient)
		number_blocks_year = 525600 * 60/ 15 # 15 second block ts
		infl_quotient = (1.0 + infl_quotient/100.0)**(1/float(number_blocks_year)) # (1.0y)^1/x 

		reward = 3

		# data for plotting
		dates = [t]
		staked = [100* myBond/bonded]

		while(t <500000000):

		    reward = total*infl_quotient - total # 21% infl, n root(1.inflrate) in round 1, the block reward is 10 , 11,etc. 
		    fees = fees * infl_quotient
		    if(random() < (myBond/bonded)):
		        myBond += fees #only if I am the proposer should I get transaction fees
		    myBond += reward*(myBond/bonded) # every round I get block validation rewards proportional to my stake in that round
		    bonded = bonded + reward + fees #every round bonded increases by reward(minted from thin air) and the tx fees paid which are rebonded
		    total *= infl_quotient # total every round increases

		    if(t%1000000 == 0):
		        prop = myBond/bonded
		        #print(prop)
		        staked.append(100*prop)
		        dates.append(t)
		        
		    t+=1
		# setting up the plottign environment
		index = np.arange(len(staked))
		opacity = 0.25
		error_config = {'ecolor': '0.3'}

		#write into the CSV 
		with open('monte_carlo_' + str(i) + '_' + str(k) + '.csv', 'w') as csvfile:
			fieldnames = ['block_number', 'adv_stake_percent', 'inflation_rate', 'start_staked_percent', 'bonded_percent']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			#writer.writerow({'block_number':1, 'adv_stake_percent':1, 'inflation_rate':4, 'start_staked_percent':6, 'bonded_percent':9})
			for j in range(len(staked)):
				writer.writerow({'block_number': dates[j], 'adv_stake_percent': staked[j], 'inflation_rate': inflation[i], 'start_staked_percent': 25, 'bonded_percent': 10 })


		print(staked)
		print(dates)

		rects2 = plot(dates, staked, color=colors[i])
		#plot(dates, [25 for i in dates], color = 'red')

	xlabel('Block Number')
	ylabel('Attacker\'s Stake')
	title('')
	legend()

	tight_layout()
	ax.set_xlim(xmin=0)
	ax.set_xlim(xmax=dates[-1])


show()
