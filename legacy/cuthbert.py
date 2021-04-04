# /cuthbert.py
# Will Watson
#
# Exposes function for estimating population size using Cuthbert's method of estimation

# Libraries
import math
import random

# Given list of samples, returns total number of entities
def __list_entities__(samples):
    entities = set()
    for sample in samples:
        for entity in sample:
            if entity not in entities:
                entities.add(entity)
    return list(entities)

# Given hpothesized population size, entity count, list of sample sizes, returns error measurement
def __calc_error__(pop_size, num_entities, sample_sizes):
    error = 1.0
    for sample_size in sample_sizes:
        error *= (pop_size - sample_size) / pop_size
    error *= pop_size
    error += (num_entities - pop_size)
    error = abs(error)
    return error

# Initializes population for cross validation given a list of entities and a target pop size
def __build_cv_population__(entities, initial_estimate):
    to_sim = initial_estimate - len(entities)
    cv_pop = entities
    for i in range(to_sim):
        cv_pop.append('Simulated Entity ' + str(i))
    return cv_pop

# Given the number of entities observed, a simulated population for cross validation, and a proportion (optional),
# returns a "corrected" estimate of the population size, which will never be smaller than the initial estimate.
def __cross_validate__(samples, num_entities, cv_population, cv_proportion):
    # Select samples to hold back for cross validation
    cv_samples = random.sample(samples, int(cv_proportion * len(samples)))
    # Construct simulated sets identical to the cross validation sets in size
    sim_samples = []
    for sample in cv_samples:
        sim_sample = random.sample(cv_population, len(sample))
        sim_samples.append(sim_sample)
    sim_set = set(__list_entities__(sim_samples))
    # Identify samples not held back
    retain_samples = []
    for sample in samples:
        if sample not in cv_samples:
            retain_samples.append(sample)
    retain_set = set(__list_entities__(retain_samples))
    # Compare sets, adjust by error factor
    new_cv = num_entities - len(retain_set)
    new_sim = max(len(sim_set.difference(retain_set)), 1)
    error_factor = max(new_cv - new_sim, 0) / new_sim
    corrected_pop_size = (len(cv_population) - num_entities) * (1 + error_factor) + num_entities
    return corrected_pop_size


# Primary calculation function; given list of samples (each sample is a list of entity names), alongside other optional
# variables, returns dictionary of estimates (one 'uncorrected' and a list of 'corrected')
def estimate(samples, min_estimate=0.01, cv=True, cv_iterations=100, cv_proportion=0.25):
    # INITIALIZE RETURN STRUCTURE
    estimates = {}

    # GENERATE UNCORRECTED ESTIMATE
    # List all entities sampled, derive maximum population size
    entities = __list_entities__(samples)
    num_entities = len(entities)
    max_pop_size = math.ceil(num_entities / min_estimate)
    # Populate list of sample sizes
    sample_sizes = []
    for sample in samples:
        sample_sizes.append(len(sample))
    # Generate errors
    errors = {}
    for i in range(num_entities, max_pop_size):
        errors[i] = __calc_error__(i, num_entities, sample_sizes)
    # Identify minimum error estimate, record in estimates
    initial_estimate = num_entities
    min_error = 10.0
    for est in errors.keys():
        if errors[est] < min_error:
            initial_estimate = est
            min_error = errors[est]
    estimates['uncorrected'] = initial_estimate

    # GENERATE CORRECTED ESTIMATES USING CROSS-VALIDATION OR NOT
    # Set up list, initialize loop
    if cv:
        corrected_estimates = []
        cv_population = __build_cv_population__(entities, initial_estimate)
        for i in range(cv_iterations):
            corrected_estimates.append(__cross_validate__(samples, num_entities, cv_population, cv_proportion))
        estimates['corrected'] = corrected_estimates

    # RETURN ESTIMATES
    return estimates