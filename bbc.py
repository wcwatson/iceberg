# /bbc.py
# Will Watson
#
# Exposes function for estimating population size using BBC's method of estimating "the prediction function."

# Libraries
import math

# Given list of samples, returns a dictionary indicating how many times each entity appears
def __count_entities__(samples):
    entity_counts = {}
    for sample in samples:
        for entity in sample:
            if entity in entity_counts.keys():
                entity_counts[entity] += 1
            else:
                entity_counts[entity] = 1
    return entity_counts

# Given dictionary of entities and counts, returns a dictionary indicating the number of entities observed once, twice,
# and so forth.
def __count_frequencies__(entity_counts):
    frequency_counts = {}
    for entity in entity_counts:
        if entity_counts[entity] in frequency_counts.keys():
            frequency_counts[entity_counts[entity]] += 1
        else:
            frequency_counts[entity_counts[entity]] = 1
    return frequency_counts

# Primary calculation function; given list of samples, returns bias-corrected estimate of population size
def estimate(samples):
    # Generate dictionary indicating the number of entities observed once, twice, etc.
    entity_counts = __count_entities__(samples)
    frequency_counts = __count_frequencies__(entity_counts)
    num_entities = sum(frequency_counts.values())
    if 1 not in frequency_counts.keys():
        print("ERROR: BBC calculation impossible due to no singletons")
        return 0
    # Generate biased estimate
    biased_estimate = 0.0
    for frequency in frequency_counts.keys():
        biased_estimate += frequency_counts[frequency] / math.exp(frequency)
    # Correct for bias using BBC's algorithm
    DELTA = 0.001
    corrected_estimate = 0.0
    prev_estimate = biased_estimate
    error = 100.0
    while error > DELTA:
        corrected_estimate = biased_estimate + (prev_estimate * math.exp(-1 * frequency_counts[1] / prev_estimate))
        error = abs(corrected_estimate - prev_estimate)
        prev_estimate = corrected_estimate
    return num_entities + corrected_estimate