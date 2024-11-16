"""Simple SDB style operators."""
# Author: Garry Morrison
# Created: 2024-11-8
# Updated: 2024-11-16

from collections import defaultdict

def operator_clean(coeffs0, labels0):
    """Clean the coeffs by setting them all to 1."""
    new_coeffs = [1] * len(labels0)
    return new_coeffs, labels0

def operator_normalize(coeffs0, labels0, t=1):
    """Normalize the coeffs in the pattern so their sum == t."""
    coeff_sum = sum(coeffs0)
    if coeff_sum == 0:
        return coeffs0, labels0 # not sure best thing to return when the sum of the coefficients is zero?
    new_coeffs = [elt * t / coeff_sum for elt in coeffs0]
    return new_coeffs, labels0

def operator_rescale(coeffs0, labels0, t=1):
    """Rescale the coeffs in the pattern so the max coeff == t."""
    coeff_max = max(coeffs0)
    if coeff_max == 0:
        return coeffs0, labels0 # not sure the best thing to return when the max of the coeffs is zero?
    new_coeffs = [elt * t / coeff_max for elt in coeffs0]
    return new_coeffs, labels0

def operator_drop_below(coeffs0, labels0, threshold):
    """Drop elements from the pattern with coeff < threshold."""
    new_coeffs, new_labels = zip(*[(v,l) for v,l in zip(coeffs0, labels0) if v >= threshold])
    return list(new_coeffs), list(new_labels)

def operator_add(coeffs0, labels0, coeffs1, labels1):
    """Superposition add the two input patterns."""
    sp_sum = defaultdict(float)
    for v,l in zip(coeffs0, labels0):
        sp_sum[l] += v
    for v,l in zip(coeffs1, labels1):
        sp_sum[l] += v
    return list(sp_sum.values()), list(sp_sum.keys()) # hopefully the ordering is correct?

def operator_or(coeffs0, labels0, coeffs1, labels1):
    """Or the two input patterns."""
    new_labels = sorted(set(labels0) | set(labels1))
    new_coeffs = [1] * len(new_labels)
    return new_coeffs, new_labels


