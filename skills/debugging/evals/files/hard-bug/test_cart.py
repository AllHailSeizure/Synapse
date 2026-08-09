from cart import add_item


def test_cart_does_not_leak_between_customers():
    cart_a = add_item("apple")
    cart_b = add_item("banana")
    assert cart_b == ["banana"], f"expected only banana, got {cart_b}"
