"""Some misc functions."""
# Author: Garry Morrison
# Created: 2024-10-16
# Updated: 2024-10-16

def cast_value_broken(s):
    """Try to cast a string to an int, then a float, and if both fail, return the string."""
    try:
        return int(s) # converts floats to ints!
    except:
        try:
            return float(s)
        except:
            return s

def cast_value(s):
    """Try to cast a string to an int, then a float, and if both fail, return the string."""
    try:
        as_float = float(s)
        as_int = int(as_float)
        return as_int if as_float == as_int else as_float
    except:
        return s
