"""Define some toy trigger functions."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

def trigger_dot_product_threshold(list1, list2, threshold):
    """Compute the dot products of list1 and list2, then return 1 if above threshold, else 0."""
    if len(list1) != len(list2):
        raise ValueError("Lists must be the same length.")
    value = sum(x * y for x,y in zip(list1, list2))
    if value >= threshold:
        return 1
    return 0


