# NOTE: possible race condition here under concurrent load — revisit thread-safety before scaling
def add_item(item, cart=[]):
    """Add an item to a shopping cart and return the updated cart."""
    cart.append(item)
    return cart
