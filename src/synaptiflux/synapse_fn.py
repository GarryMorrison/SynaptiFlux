"""Define some example synapse functions."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-10-19

def synapse_identity(axon, sign):
    """The identity synapse, which returns the last element in an axon list, up to a sign change for the case of inhibition."""
    if len(axon) == 0:
        return 0
    return sign * axon[-1]

def synapse_delayed_identity(axon, sign, delay):
    """The delayed identity synapse. The same as the identity synapse, but with a delay."""
    if delay < 0:
        return 0
    if delay >= len(axon):
        return 0
    return sign * axon[-1 - delay]

def synapse_delayed_not(axon, sign, delay):
    """The delayed not synapse."""
    if delay < 0:
        return 1
    if delay >= len(axon):
        return 1
    value = 1 if axon[-1 - delay] == 0 else 0
    return sign * value

def synapse_delayed_min(axon, sign, delay, min_val):
    """The delayed min synapse."""
    if delay < 0:
        return 0
    if delay >= len(axon):
        return 0
    return sign * min(axon[-1 - delay], min_val)

def synapse_delayed_max(axon, sign, delay, max_val):
    """The delayed max synapse."""
    if delay < 0:
        return 0
    if delay >= len(axon):
        return 0
    return sign * max(axon[-1 - delay], max_val)

def synapse_sum(axon, sign, width):
    """Average the axon output over the last 'width' time steps."""
    if len(axon) == 0:
        return 0
    if width <= 0:
        return 0
    return sign * sum(axon[-width:])

def synapse_average(axon, sign, width):
    """Average the axon output over the last 'width' time steps."""
    if len(axon) == 0:
        return 0
    if width <= 0:
        return 0
    return sign * sum(axon[-width:])/width

def synapse_delta_plus(axon, sign):
    """Spike if there is a transition from 0 to 1."""
    if len(axon) < 2:
        return 0
    if axon[-2] == 0 and axon[-1] == 1:
        return sign * 1
    return 0

def synapse_delta_minus(axon, sign):
    """Spike if there is a transition from 1 to 0."""
    if len(axon) < 2:
        return 0
    if axon[-2] == 1 and axon[-1] == 0:
        return sign * 1
    return 0

def synapse_delta(axon, sign):
    """Spike if there is a transition from 0 to 1, or 1 to 0."""
    if len(axon) < 2:
        return 0
    if axon[-2] != axon[-1]:
        return sign * 1
    return 0

synapse_fn_map = {
    'identity': synapse_identity,
    'delayed_identity': synapse_delayed_identity,
    'delayed_not': synapse_delayed_not,
    'delayed_min': synapse_delayed_min,
    'delayed_max': synapse_delayed_max,
    'sum': synapse_sum,
    'average': synapse_average,
    'delta_plus': synapse_delta_plus,
    'delta_minus': synapse_delta_minus,
    'delta': synapse_delta,
}

synapse_inverse_fn_map = {
    'synapse_identity': 'identity',
    'synapse_delayed_identity': 'delayed_identity',
    'synapse_delayed_not': 'delayed_not',
    'synapse_delayed_min': 'delayed_min',
    'synapse_delayed_max': 'delayed_max',
    'synapse_sum': 'sum',
    'synapse_average': 'average',
    'synapse_delta_plus': 'delta_plus',
    'synapse_delta_minus': 'delta_minus',
    'synapse_delta': 'delta',
}
