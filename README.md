# modeling_icebergs

Code and write-up analyzing efficacy of two methods of population estimation given samples with replacement. `Watson_Modeling+Icebergs.pdf` contains a draft article elaborating on the other contents of this repo. This material expands on arguments and code presented in the third chapter of my dissertation, "Circulating Song from the Century Before Print" (2020).

## Files
* `bbc.py` exposes a function that estimates population size using an analytic method proposed in Boneh, Boneh, and Caron (1998)
* `cuthbert.py` exposes a function that estimates population size using a probabilistic method proposed in Cuthbert (2009)
* `random_simulation.py` exposes a function that simulates random samples with replacement on a population of a given size and applies both methods of estimation
* `sim_sandbox.ipynb` performs some of the analysis discussed in the write-up
* `unica_test.py` evaluates both methods' performances on a collection of samples where no entities appear more than once
* `identical_test.py` evaluates Boneh, Boneh, and Caron's method's performance on a collection of samples that are (almost) identical
