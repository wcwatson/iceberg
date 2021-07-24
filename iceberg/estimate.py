"""Exposes functions to estimate population size given a list of samples."""

from collections import Counter

import numpy as np


def _calculate_error(estimate, num_entities, sample_sizes):
    """Calculates the error of a population estimate given the number of
    entities observed and the sizes of samples taken without replacement.

    Parameters
    ----------
    estimate: int
        The estimate of population size to be evaluated.
    num_entities: int
        The number of distinct entities observed.
    sample_sizes: list
        A list of integers indicating the size of each sample taken.

    Returns
    -------
    float
        The error incurred by this estimate of population size.
    """

    # Contribution to log sample expectation from each sample
    log_sample_contributions = [
        np.log(estimate - sample_size) - np.log(estimate)
        for sample_size in sample_sizes
    ]
    # Contribution to log sample expectation from estimated population size
    log_pop_contribution = np.log(estimate)
    # Expectation of unobserved entity count from sample distribution
    sample_expectation = np.exp(
        sum(log_sample_contributions) + log_pop_contribution
    )
    # Expectation of unobserved entity count from counting (i.e., the difference
    # between the estimated population size and the number of observed entities)
    count_expectation = estimate - num_entities
    # Return the difference in expectations as a measure of error
    return sample_expectation - count_expectation


def _recurse_to_best_estimate(
        lower_bound, upper_bound, num_entities, sample_sizes
):
    """Recursively finds the best estimate of population size by identifying
    which half of [lower_bound, upper_bound] contains the best estimate.

    Parameters
    ----------
    lower_bound: int
        The lower bound of the interval to be tested; the value of the error
        function can always be assumed to be positive at this point.
    upper_bound: int
        The upper bound of the interval to be tested; the value of the error
        function can always be assumed to be negative at this point.
    num_entities: int
        The number of distinct entities observed.
    sample_sizes: list
        A list of integers indicating the size of each sample taken.

    Returns
    -------
    int
        The best estimate of population size.
    """

    # Base case - return the upper bound when the upper and lower bounds are
    # adjacent
    if upper_bound - lower_bound <= 1:
        return upper_bound

    # Otherwise calculate error at midpoint and recursively evaluate the
    # relevant half of the interval
    midpoint = int(np.ceil((lower_bound + upper_bound) / 2))
    error_at_midpoint = _calculate_error(midpoint, num_entities, sample_sizes)
    if error_at_midpoint > 0:
        return _recurse_to_best_estimate(
            midpoint, upper_bound, num_entities, sample_sizes
        )
    else:
        return _recurse_to_best_estimate(
            lower_bound, midpoint, num_entities, sample_sizes
        )


def _find_best_estimate(num_entities, max_pop_size, sample_sizes):
    """Finds the best integer estimate of population size in the domain
    [num_entities, max_pop_size]. The time complexity is O(log(max_pop_size)).

    NB: this algorithm relies on the following facts: that the error function is
    decreasing on the entire domain; and that the error function is
    positive-valued at the domain's lower bound.

    Parameters
    ----------
    num_entities: int
        The number of distinct entities observed.
    max_pop_size: int
        The maximum allowable population size.
    sample_sizes: list
        A list of integers indicating the size of each sample taken.

    Returns
    -------
    int
        The best estimate of population size or, barring that, the maximum
        allowable estimate.
    """

    # Catch cases where maximum allowable estimate is still too low or where
    # minimum allowable estimate is still too high, and return to save
    # computation
    error_at_max = _calculate_error(max_pop_size, num_entities, sample_sizes)
    if error_at_max > 0:
        return max_pop_size
    error_at_min = _calculate_error(num_entities, num_entities, sample_sizes)
    if error_at_min <= 0:
        return num_entities

    # Return the best estimate in the passed domain
    return _recurse_to_best_estimate(
        num_entities, max_pop_size, num_entities, sample_sizes
    )


def _cross_validate_estimate(
        simulated_population, samples, num_observed, cv_ppn
):
    """Returns a cross-validated estimate of population size.

    Parameters
    ----------
    simulated_population: list
        A simulated population containing all observed entities and a number of
        simulated entities not in any sample.
    samples: list
        A list of lists; each element is a list of entities observed in a
        particular sample.
    num_observed: int
        The number of distinct entities observed in the samples (this is
        derivable from samples, but it's already calculated in the calling
        function, so why duplicate effort?).
    cv_ppn: float
        The proportion of samples to be used for each cross-validation attempt.

    Returns
    -------
    int
        A cross-validated estimate of population size.
    """

    # Select samples to hold as a validation set
    cv_size = int(np.ceil(cv_ppn * len(samples)))
    validation_samples = np.random.choice(
        np.array(samples, dtype=object), cv_size, replace=False
    ).tolist()

    # Construct simulated samples identical in size to the holdout sets
    simulated_entities = set(
        entity for simulated_sample in [
            np.random.choice(
                simulated_population, len(sample), replace=False
            ).tolist()
            for sample in validation_samples
        ]
        for entity in simulated_sample
    )

    # Identify entities in samples not held back for cross validation
    retained_samples = [
        sample for sample in samples if sample not in validation_samples
    ]
    retained_entities = set(
        entity for sample in retained_samples for entity in sample
    )

    # Calculate number of "new" entities in held-back and simulated samples,
    # determine correction factor
    true_new = num_observed - len(retained_entities)
    simulated_new = len(simulated_entities.difference(retained_entities))
    correction_factor = max(true_new - simulated_new, 0) / max(simulated_new, 1)

    # Return corrected estimate of population size
    corrected_estimate_of_new_entities = int(np.ceil(
        (len(simulated_population) - num_observed) * (1 + correction_factor)
    ))
    return num_observed + corrected_estimate_of_new_entities


def cuthbert(samples, min_survival=0.01, cv=None, cv_ppn=0.2):
    """Estimates population size given a collection of samples without
    replacement, using method proposed in Cuthbert (2009).

    Parameters
    ----------
    samples: list
        A list of lists; each element is a list of entities observed in a
        particular sample.
    min_survival: float
        The minimum allowable estimate of the survival rate; implicitly defines
        the maximum population size that will be returned.
    cv: int
        The number of cross-validation iterations that should be performed; if
        None then cross-validation will be skipped.
    cv_ppn: float
        The proportion of samples to be used for each cross-validation attempt.

    Returns
    -------
    dict
        All estimated population sizes; the structure is { 'uncorrected': int,
        'corrected': [int] }, where len(dict['corrected']) is equal to cv.
    """

    # Initialize result
    estimates = {'uncorrected': 0, 'corrected': []}

    # Generate an uncorrected estimate of population size by recursively
    # identifying the estimate of minimum error within the domain defined by the
    # number of sampled entities and min_survival
    sample_sizes = [len(sample) for sample in samples]
    entities = set(entity for sample in samples for entity in sample)
    max_pop_size = int(np.ceil(len(entities) / min_survival))
    estimates['uncorrected'] = _find_best_estimate(
        len(entities), max_pop_size, sample_sizes
    )

    # If indicated, generate corrected estimates using cross-validation
    if cv is not None:
        # Generate a simulated population the size of the uncorrected estimate
        simulated_entities = [
            'simulated_entity_' + str(i)
            for i in range(estimates['uncorrected'] - len(entities))
        ]
        simulated_population = list(entities) + simulated_entities
        # Calculate cv cross-validated estimates
        for _ in range(cv):
            estimates['corrected'].append(
                _cross_validate_estimate(
                    simulated_population, samples, len(entities), cv_ppn
                )
            )

    # Return final result
    return estimates


def bbc(samples, max_delta=0.001):
    """Estimates population size given a collection of samples without
    replacement, using method proposed in Boneh, Boneh, and Caron (1998).

    Parameters
    ----------
    samples: list
        A list of lists; each element is a list of entities observed in a
        particular sample.
    max_delta: float
        The incremental change to which the correction algorithm must converge
        prior to termination.

    Returns
    -------
    int
        The estimated population size.

    Raises
    ------
    ValueError
        If there are no entities observed exactly once.
    """

    # Generate a dictionary mapping natural numbers, n, to the number of
    # entities observed n times across all samples
    entity_counts = dict(Counter(
        [entity for sample in samples for entity in sample]
    ))
    frequency_counts = dict(Counter(list(entity_counts.values())))

    # Raise value error if no singletons
    if frequency_counts.get(1) is None:
        raise ValueError('no entity was observed exactly once')

    # Generate biased estimate of the number of unobserved entities
    biased_est = sum(
        [frequency_counts[f] / np.exp(f) for f in frequency_counts]
    )

    # Correct for bias in estimate of unobserved entities via BBC's suggested
    # algorithm
    corrected_est = biased_est
    delta = max_delta + 1
    while delta > max_delta:
        previous_est = corrected_est
        corrected_est = biased_est + (
            previous_est * np.exp(-1 * frequency_counts[1] / previous_est)
        )
        delta = abs(corrected_est - previous_est)

    # Return corrected estimated total population size
    corrected_est = int(np.ceil(corrected_est))
    return len(entity_counts) + corrected_est
