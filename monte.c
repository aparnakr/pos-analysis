// assumption: the validator set doesn't increase or change.
#include <time.h>
#include <stdlib.h>
#include <math.h>


/* Egs of inputs inflation = 1 , total_p_bonded = 0.1 (<= 1), p_adv = 0.25 (<=1) */ 
void monte_carlo(double inflation, double total_p_bonded, double p_adver){

	srand(time(NULL)); 

	int t = 0; //number of blocks
	double total = 87936854.71875; //current ETH supply in the market
	double bonded = total * total_p_bonded;  //amount of ETH bonded
	double myBond = bonded * p_adver;  // adversary's inital stake (I am the adversary)
	double fees = 0.161/163.05; // worst case avg fees
	double infl_amt = 1; // from range 1% to 14%
	double number_blocks_year = 525600 * 60/ 15; // 15 second block ts
	double infl_quotient = powl((1.0 + infl_amt/100.0),(1/(number_blocks_year))); 


	printf("%f\n", number_blocks_year);
	double eecs =  ((double)1.0 )/ ((double) number_blocks_year);
	printf("1 over 100 %f \n", eecs);
	//printf("num blocks %Lf \n", number_blocks_year);
	//printf("%Lf\n", infl_quotient);
	/* We calculate infl_quotient as follows:
	 1.0y)^1/x 
	 Example if infl_amt = 5% and the time chunks is 6 months
	 Then (1.05)^(1/(12/6)) is the inflation_quotient*/

	double reward = 3.0;

	//for plotting
	int dates [1000];
	dates[0] = t;
	double staked[1000];
	staked[0] = 100* myBond/bonded;

	while(t <1000000000){

		reward = (total * infl_quotient) - total; // 21% infl, n root(1.inflrate) in round 1, the block reward is 10 , 11,etc. 
	    fees = fees * infl_quotient;
	    double ran = (double)(rand()%100);
	    //printf("random: %f, stake %f \n", ran, myBond/bonded);

	    if(ran < (myBond/bonded) * 100){
	    	myBond += fees; //only if I am the proposer should I get transaction fees
	    } 

	    myBond =  myBond + (reward * (myBond / bonded)); // every round I get block validation rewards proportional to my stake in that round
	    bonded = bonded + reward + fees; //every round bonded increases by reward(minted from thin air) and the tx fees paid which are rebonded
	    total = total * infl_quotient; //total every round increases

	    if(t%1000000 == 0){
	        double prop = myBond/bonded;
	        //printf("%Lf \n", prop);
	        staked[((int)t)%1000000] = 100*prop;
	        dates[((int)t)%1000000] = t;
	    }

	    t+=1;

	}
	// double x = 1000000; 
	// double total = 0; 
	// double rest_of_network = 9000000; 
	// int t = 0;
	// total = rest_of_network + x; 
	// while (x/total < 0.33){
	// 	t = t + 1;
	// 	double prob = x/total;
	// 	double ran = (double)(rand()%100);
	//     if ( ran < prob * 100){
	//             x = x + r;
	//         }
	//         total = total + r;
	// }
	//return t;
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


