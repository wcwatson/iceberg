"""Non-doctest unit tests for the iceberg library"""

import pytest

import iceberg.estimate as est

# Ensure that the BBC estimation raises an error in the event that there are no
# uniquely observed entities
def test_bbc_singletons():
    samples = [[0, 1], [0, 1]]
    with pytest.raises(ValueError):
        est.bbc(samples)
