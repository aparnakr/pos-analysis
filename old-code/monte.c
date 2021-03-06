/* assumption: the validator set doesn't increase or change. */
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>


/* Exs of inputs inflation = 1 , total_p_bonded = 0.1 (<= 1), p_adv = 0.25 (<=1) */
void monte_carlo(int run, double inflation, double total_p_bonded, double p_adver) {

  printf("monte_carlo(%d, %.3f, %.3f, %.3f)\n", run, inflation, total_p_bonded, p_adver);

  srand(time(NULL));

  /* Number of blocks */
  int t = 0;
  /* Current ETH supply in the market */
  double total = 87936854.71875;
  /* Amount of ETH bonded */
  double bonded = total * total_p_bonded;
  /* Adversary's inital stake (I am the adversary) */
  double myBond = bonded * p_adver;
  /* Worst case avg fees over a month from blockchain.info  */
  // double fees =  0.161 / 163.05;
  double fees = 0.3;
  /* from range 1% to 14% */
  double infl_amt = 1;
  double number_blocks_year = 525600 * 60 / 15;   /* 15 second block ts */

  /* We calculate infl_quotient as follows:
   * (1.0y)^1/x
   * Example: if infl_amt = 5% and the time chunks is 6 months
   * Then (1.05)^(1/(12/6)) is the inflation_quotient.
   */
  double infl_quotient =
    powl((1.0 + infl_amt / 100.0), (1 / (number_blocks_year)));
  double reward;

  /* Plotting data */
  int dates[1000];
  dates[0] = t;
  double staked[1000];
  staked[0] = 100 * myBond/bonded;
  FILE *fp;
  char filename[256];
  snprintf(filename, 256, "./mcsim_%d_%.3f_%.3f_%.3f.csv",
      run, inflation, total_p_bonded, p_adver);
  fp = fopen(filename, "w");
  fprintf(fp, "round,stake proportion\n");

  while(t < 1000000000){

    /* Inflation rate multiplied in at each block*/
    reward = (total * infl_quotient) - total;
    /* Inflation rate also affects fees */
    fees = fees * infl_quotient;
    double ran = ((double) rand()) / RAND_MAX;

    if(ran < myBond / bonded){
      //printf(" WON :) my bond %.9f, total bonded %.9f , percent %.9f \n", myBond, bonded, 100 * (myBond/bonded));
      /* Only if I am the proposer should I get transaction fees */
      myBond += fees;
    }else{
      //printf(" LOST :( my bond %.9f, total bonded %.9f , percent %.9f \n", myBond, bonded, 100 * (myBond/bonded));
    }

    /* Every round I get block validation rewards proportional to my stake in that round */
    myBond =  myBond + (reward * (myBond / bonded));
    /* Every round bonded increases by reward(minted from thin air) and the tx fees paid which are rebonded */
    bonded = bonded + fees + reward;
    /* Total every round increases */
    total = total * infl_quotient;

    t++;

    if(t % 1000000 == 0){
      double prop = myBond/bonded;
      //printf("%0.9f %0.9f %0.9f \n", prop, myBond, bonded);
      fprintf(fp, "%d,%.9f\n", t, 100*prop);
      staked[((int)t) % 1000000] = 100 * prop;
      dates [((int)t) % 1000000] = t;
    }
  }

  fclose(fp);
}

int main(int argc, char const *argv[])
{
  int num_runs = 1;
  double staked[1000 * num_runs];
  int total_p_bonded = 5;
  int p_adver = 35;

  #pragma omp parallel for collapse(3)
  for (int i = 0; i < num_runs; i++) {
    for (int j = 1; j < total_p_bonded; j++){
      for (int k = 1; k < p_adver; k++){
        monte_carlo(i, 1.0, ((double) j)/100.0, ((double) k/100.0));
      }
    }

    // double* stake_m = monte_carlo(1.0, 0.1, 0.25);
    // printf("%f", stake_m[0]);
    // int k = 0;
    // for (int j = i * 1000; j < (j + 1) * 1000; ++j)
    // {
    // 	staked[j] = stake_m[k];
    // 	k++;
    // }

  }

  return 0;
}


