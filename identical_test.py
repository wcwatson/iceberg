# /identical_test.py
# Will Watson
#
# Simulating identity save one for BBC (Cuthbert's method is solvable analytically for identity)

# LIBRARIES
import bbc

# SET SIMULATION PARAMETERS
sims = []
num_samples = [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]
sample_size = [10]

# FUNCTION TO BUILD IDENTICAL SAMPLES
def build_samples(num, size):
    samples = []
    sample = []
    for i in range(size):
        sample.append(i)
    for i in range(num):
        samples.append(sample.copy())
    samples[0].insert(0, 'new')
    return samples

# RUN SIMULATION
for num in num_samples:
    for size in sample_size:
        samples = build_samples(num, size)
        bbc_est = bbc.estimate(samples)
        sims.append([num, size, bbc_est])

# PRINT RESULTS
for sim in sims:
    print("Number of samples: {} | Sample size: {} | BBC Est: {:.6f}".format(sim[0], sim[1], sim[2]))