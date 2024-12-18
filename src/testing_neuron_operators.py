"""This script will test some neuron operators."""
# Author: Garry Morrison
# Created: 2024-11-8
# Updated: 2024-11-16

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing neuron operators ...")

    N1 = sf.Neuron('neuron example 1', 0, [1,1,1,1], ['alpha', 'beta', 'gamma', 'epsilon'], sf.trigger_list_min_simm_threshold, {'threshold': 0.98}, sf.pooling_or, {})

    # see what we have:
    print(N1)

    # apply the normalize operator:
    print("Normalize(100):")
    N1.apply_operator(0, sf.operator_normalize, {'t': 100})
    print(N1)

    # apply the clean operator:
    print("Clean:")
    N1.apply_operator(0, sf.operator_clean, {})
    print(N1)

    # add patterns:
    print("Add superposition patterns:")
    N1.apply_operator(0, sf.operator_add, {'coeffs1': [1,1], 'labels1': ['alpha', 'gamma']})
    N1.apply_operator(0, sf.operator_add, {'coeffs1': [1,1], 'labels1': ['beta', 'gamma']})
    N1.apply_operator(0, sf.operator_add, {'coeffs1': [1,1,1], 'labels1': ['alpha', 'gamma', 'delta']})
    print(N1)

    # drop below(2.5):
    print("drop-below(2.5):")
    N1.apply_operator(0, sf.operator_drop_below, {'threshold': 2.5})
    print(N1)

    # rescale(10):
    print("rescale(10):")
    N1.apply_operator(0, sf.operator_rescale, {'t': 10})
    print(N1)

    # test or'ing patterns:
    N2 = sf.Neuron('neuron example 2', 0, [2,3,5,7], ['alpha', 'beta', 'gamma', 'epsilon'], sf.trigger_list_min_simm_threshold, {'threshold': 0.98}, sf.pooling_or, {})
    print("Or patterns:")
    N2.apply_operator(0, sf.operator_or, {'coeffs1': [11,13,17,19], 'labels1': ['alpha', 'gamma', 'eta', 'theta']})
    N2.apply_operator(0, sf.operator_or, {'coeffs1': [23,29,31], 'labels1': ['iota', 'lambda', 'kappa']})
    print(N2)
