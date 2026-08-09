import numpy as np

from script import to_stats_array


def test_to_stats_array():
    result = to_stats_array([1, 2, 3])
    assert result.dtype == np.float64
