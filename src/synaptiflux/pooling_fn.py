"""Define some toy pooling functions."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

def pooling_or(list1):
    """Pool the outputs from our trigger functions into a single value."""
    if len(list1) == 0:
        return 0
    return int(any(list1))

def pooling_xor(list1):
    """Apply xor to the output list."""
    if len(list1) != 2:
        return 0
    return list1[0] ^ list1[1]

def pooling_sum(list1, threshold):
    """Sum the list, and check if above threshold or not."""
    value = sum(list1)
    if value >= threshold:
        return 1
    return 0

def pooling_sum_mod2(list1):
    """Sum the list and apply mod 2."""
    return sum(list1) % 2
