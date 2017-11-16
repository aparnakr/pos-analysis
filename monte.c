/* assumption: the validator set doesn't increase or change. */ 
#include <time.h>
#include <stdlib.h>
#include <math.h>


/* Egs of inputs inflation = 1 , total_p_bonded = 0.1 (<= 1), p_adv = 0.25 (<=1) */ 
void monte_carlo(double inflation, double total_p_bonded, double p_adver){

	srand(time(NULL)); 

	int t = 0; 										/* Number of blocks */ 
	double total = 87936854.71875; 					/* Current ETH supply in the market */
	double bonded = total * total_p_bonded; 		/* Amount of ETH bonded */ 
	double myBond = bonded * p_adver;  				/* Adversary's inital stake (I am the adversary) */ 
	double fees =  0.161 / 163.05;					/* Worst case avg fees over a month from blockchain.info  */
	double infl_amt = 1; 							/* from range 1% to 14% */ 
	double number_blocks_year = 525600 * 60 / 15;   /* 15 second block ts */

/* 	We calculate infl_quotient as follows:
		(1.0y)^1/x
	Example: if infl_amt = 5% and the time chunks is 6 months
	 Then (1.05)^(1/(12/6)) is the inflation_quotient. */
	double infl_quotient = powl((1.0 + infl_amt / 100.0), (1 / (number_blocks_year))); 
	double reward;

	/* Plotting data */
	int dates [1000];
	dates[0] = t;
	double staked[1000];
	staked[0] = 100 * myBond/bonded;

	while(t < 1000000000){

		reward = (total * infl_quotient) - total; 		/* Inflation rate multiplied in at each block*/
	    fees = fees * infl_quotient; 					/* Inflation rate also affects fees */
	    double ran = (double)(rand()%100);

	    if(ran < (myBond / bonded) * 100){
	    	//printf(" WON :) my bond %.9f, total bonded %.9f , percent %.9f \n", myBond, bonded, 100 * (myBond/bonded));
	    	myBond += fees; 							/* Only if I am the proposer should I get transaction fees */
	    }else{

	    //printf(" LOST :( my bond %.9f, total bonded %.9f , percent %.9f \n", myBond, bonded, 100 * (myBond/bonded));
	    }

	    myBond =  myBond + (reward * (myBond / bonded)); /* Every round I get block validation rewards proportional to my stake in that round */
	    bonded = bonded + fees + reward; 				 /* Every round bonded increases by reward(minted from thin air) and the tx fees paid which are rebonded */
	    total = total * infl_quotient; 					 /* Total every round increases */

	    t++;

	    if(t % 1000000 == 0){
	        double prop = myBond/bonded;
	        printf("%.9f \n", prop);
	        staked[((int)t) % 1000000] = 100 * prop;
	        dates[((int)t) % 1000000] = t;
	    }

	}
	
   // return &staked;

}

int main(int argc, char const *argv[])
{	
	monte_carlo(1.0, 0.1, 0.25);
	// int num_runs = 1;
	// double staked[1000 * num_runs];

	// //#pragma omp parallel for
	// for( int i = 0; i < num_runs; i++) {

	// 	monte_carlo(1.0, 0.1, 0.25);
	// 	// double* stake_m = monte_carlo(1.0, 0.1, 0.25);
	// 	// printf("%f", stake_m[0]);
	// 	// int k = 0;
	// 	// for (int j = i * 1000; j < (j + 1) * 1000; ++j)
	// 	// {
	// 	// 	staked[j] = stake_m[k];
	// 	// 	k++;
	// 	// }

	// }

	return 0;
}


