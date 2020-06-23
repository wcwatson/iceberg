# /unica_test.py
# Will Watson
#
# Simulating universes of unica for Cuthbert's and BBC's methods

# LIBRARIES
import cuthbert
import bbc

# SET SIMULATION PARAMETERS, INITIALIZE STORAGE STRUCTURE
num_samples = [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]
sample_size = [10]
sims = []

# FUNCTION TO BUILD SAMPLES OF UNICA
def build_samples(num, size, est_type):
    samples = []
    for i in range(num):
        sample = []
        for j in range(size):
            sample.append(i * size + j)
        samples.append(sample)
    if est_type == 'cuthbert':
        samples[1][0] = 0
    return samples

# RUN SIMULATION
for num in num_samples:
    for size in sample_size:
        for est_type in ['cuthbert', 'bbc']:
            samples = build_samples(num, size, est_type)
            if est_type == 'cuthbert':
                est = cuthbert.estimate(samples, cv=False)['uncorrected']
            else:
                est = bbc.estimate(samples)
            sims.append([num, size, est_type, est])

# PRINT RESULTS
for sim in sims:
    print("Number of samples: {} | Sample size: {} | Estimate type: {} | Estimate: {:.0f}".format(sim[0], sim[1], sim[2], sim[3]))