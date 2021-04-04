"""Exposes several functions that simulate situations to demonstrate the
capabilities of the estimators defined elsewhere in iceberg.
"""

import numpy as np

import iceberg.estimate as est


def identical_samples_save_one(n_samples=10, sample_size=10):
    """Simulates a collection of n_samples identical samples of size
    sample_size, appends one unique entity to one sample, and calculates the BBC
    estimate of the population size; Cuthbert's method is analytically solvable
    and will yield sample_size as an estimate of the population.

    Examples
    --------
    >>> identical_samples_save_one()
    {'bbc': 12, 'cuthbert': {'uncorrected': 10, 'corrected': []}}

    Parameters
    ----------
    n_samples: int
        The number of samples to simulate.
    sample_size: int
        The (uniform) size of each sample.

    Returns
    -------
    dict
        A dictionary of estimates; the structure is { 'bbc': int, 'cuthbert':
        {'uncorrected': int, 'corrected': []} }.

    Raises
    ------
    ValueError
        If n <=1.
    """

    # Catch bad input
    if n_samples <= 1:
        raise ValueError('n must be greater than 1')
    # Initialize result structure and simulate samples
    results = {}
    samples = [
        [str(i) for i in range(sample_size)] for _ in range(n_samples)
    ]
    samples[0].append(str(sample_size))
    # Calculate BBC estimate
    results['bbc'] = est.bbc(samples)
    results['cuthbert'] = {'uncorrected': sample_size, 'corrected': []}
    # Return final results
    return results


def unique_entities(n_samples=10, sample_size=10):
    """Simulates a collection of n_samples samples of size sample_size where no
    entity is observed more than once, calculates the BBC estimate of the
    population size, and calculates the uncorrected Cuthbert estimate after
    repeating one entity to ensure convergence.

    Examples
    --------
    >>> unique_entities()
    {'bbc': 141, 'cuthbert': {'uncorrected': 4564, 'corrected': []}}
    >>> unique_entities(n_samples=100, sample_size=25)
    {'bbc': 3503, 'cuthbert': {'uncorrected': 250000, 'corrected': []}}

    Parameters
    ----------
    n_samples: int
        The number of samples to simulate.
    sample_size: int
        The (uniform) size of each sample.

    Returns
    -------
    dict
        A dictionary of estimates; the structure is { 'bbc': int, 'cuthbert':
        {'uncorrected': int, 'corrected': []} }.

    Raises
    ------
    ValueError
        If n <=1.
    """

    # Catch bad input
    if n_samples <= 1:
        raise ValueError('n must be greater than 1')
    # Initialize result structure and simulate samples
    results = {}
    samples = [
        [str(sample_size * i + j) for j in range(sample_size)]
        for i in range(n_samples)
    ]
    # Calculate BBC estimate
    results['bbc'] = est.bbc(samples)
    # Append entity '0' to last sample to ensure Cuthbert convergence and
    # calculate
    samples[n_samples - 1].append('0')
    results['cuthbert'] = est.cuthbert(samples)
    # Return final results
    return results


def random_samples(pop_size, sample_sizes, n_samples=None):
    """Simulates a random collection of samples taken from a population of a
    given size and returns BBC and  (uncorrected) Cuthbert estimates of
    population size. Can construct samples of uniform size or of varying size,
    depending on the values of the parameters.

    Examples
    --------
    >>> np.random.seed(1729)
    >>> random_samples(1000, 20, 20)
    {'entities_observed': 330, 'bbc': 449, 'cuthbert': {'uncorrected': 962, 'corrected': []}}
    >>> random_samples(10000, 20, 200)
    {'entities_observed': 3297, 'bbc': 4483, 'cuthbert': {'uncorrected': 9960, 'corrected': []}}
    >>> random_samples(1000, [10, 10, 20, 20, 25, 25, 30, 40, 80, 160])
    {'entities_observed': 359, 'bbc': 492, 'cuthbert': {'uncorrected': 1053, 'corrected': []}}

    Parameters
    ----------
    pop_size: int
        The size of the population to be simulated.
    sample_sizes: list or int
        If a list of ints, specifies the size of each sample individually. If an
        int, the uniform size of all samples (in this case n_samples is
        required).
    n_samples: int
        If sample_sizes is an int, then n_samples indicates the number of
        uniformly sized samples that should be simulated.

    Returns
    -------
    dict
        A dictionary of estimates; the structure is { 'entities_observed': int,
        'bbc': int, 'cuthbert': {'uncorrected': int, 'corrected': []} }.

    Raises
    ------
    ValueError
        If pop_size < sample_sizes or max(sample_sizes).
    """

    # Catch bad input
    if (
            (isinstance(sample_sizes, int) and pop_size < sample_sizes)
            or
            (isinstance(sample_sizes, list) and pop_size < max(sample_sizes))
    ):
        raise ValueError('pop_size must be larger than the largest sample size')

    # Population of dummy entities
    population = [str(i) for i in range(pop_size)]
    # Simulate uniformly sized samples
    if isinstance(sample_sizes, int):
        samples = [
            np.random.choice(population, sample_sizes, replace=False).tolist()
            for _ in range(n_samples)
        ]
    # Simulate samples of varying size
    elif isinstance(sample_sizes, list):
        samples = [
            np.random.choice(population, size, replace=False).tolist()
            for size in sample_sizes
        ]
    # Catch any other input
    else:
        raise TypeError('sample_sizes must either be a list or an int')

    # Calculate and return results
    results = {}
    results['entities_observed'] = len(
        set(entity for sample in samples for entity in sample)
    )
    results['bbc'] = est.bbc(samples)
    results['cuthbert'] = est.cuthbert(samples)
    return results
