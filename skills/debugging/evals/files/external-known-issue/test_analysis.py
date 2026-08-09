import numpy as np

from analysis import to_float_array


def test_to_float_array():
    result = to_float_array([1, 2, 3])
    assert result.dtype == np.float64
