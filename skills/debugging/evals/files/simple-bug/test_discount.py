from discount import calculate_discount


def test_normal_discount():
    assert calculate_discount(100, 20) == 80


def test_discount_clamps_over_100():
    assert calculate_discount(100, 150) == 0
