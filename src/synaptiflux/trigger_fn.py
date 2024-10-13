"""Define some toy trigger functions."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-10-13

def trigger_dot_product_threshold(list1, list2, threshold):
    """Compute the dot products of list1 and list2, then return 1 if above threshold, else 0."""
    if len(list1) != len(list2):
        raise ValueError("Lists must be the same length.")
    value = sum(x * y for x,y in zip(list1, list2))
    if value >= threshold:
        return 1
    return 0

def trigger_list_simm_threshold(f, g, threshold):
    """Compute the list similarity measure of f and g, then return 1 if above threshold, else 0.

    See here: http://write-up.semantic-db.org/71-a-list-implementation-of-the-simm.html
    """
    if len(f) != len(g):
        raise ValueError("Lists must be the same length.")
    the_len = len(f)

    # rescale step, first find size:
    s1 = sum(abs(f[k]) for k in range(the_len))
    s2 = sum(abs(g[k]) for k in range(the_len))

    # if s1 or s2 == 0 we can't rescale:
    if s1 == 0 or s2 == 0:
        return 0

    # now rescale:
    f = [f[k]/s1 for k in range(the_len)]
    g = [g[k]/s2 for k in range(the_len)]

    wfg = sum(abs(f[k] - g[k]) for k in range(the_len))

    value = (2 - wfg)/2

    if value >= threshold:
        return 1
    return 0


