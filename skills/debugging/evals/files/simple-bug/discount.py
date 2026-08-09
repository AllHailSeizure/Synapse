def calculate_discount(price, pct):
    """Apply a percentage discount to price. Discount percentage should be clamped to [0, 100]."""
    return price - (price * pct / 100)
