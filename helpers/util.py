import random


def random_color():
    """
    This generates a random hex color and returns it.
    """
    # Generating a random number in between 0 and 2^24
    color = random.randrange(0, 2**24)

    # Converting that number from base-10
    # (decimal) to base-16 (hexadecimal)
    # hex_color = hex(color)
    return color
