# /random_simulation.py
# Will Watson
#
# Exposes function to simulate a random population and evaluate the accuracy of Cuthbert's and BBC's methods

# Libraries
import random
from iceberg import bbc, cuthbert


# Given list of samples, returns total number of entities
def __list_entities__(samples):
    entities = set()
    for sample in samples:
        for entity in sample:
            if entity not in entities:
                entities.add(entity)
    return list(entities)

# Primary function, returns dictionary of estimates for population and samples fitting input parameters
# Requires population size, and sample structure, which is either:
# if uniform, the number and size of uniform samples
# if not uniform, a dictionary of samples of the form {id: size}
def random_simulation(pop_size, uniform=True, num_samples=0, sample_size=0, samples={}, cuthbert_cv=True):
    # Generate population
    population = list(range(pop_size))
    # Generate random samples
    random_samples = []
    # Construct samples of uniform size
    if uniform:
        for i in range(num_samples):
            random_samples.append(random.sample(population, sample_size))
    # Construct samples of non-uniform size
    else:
        for sample in samples.keys():
            random_samples.append(random.sample(population, samples[sample]))
    # Generate estimates for both methods, return estimates
    results = {}
    results['pop_size'] = pop_size
    results['n_sampled'] = len(__list_entities__(random_samples))
    results['cuthbert_est'] = cuthbert.estimate(random_samples, cv=cuthbert_cv)
    results['bbc_est'] = bbc.estimate(random_samples)
    return results