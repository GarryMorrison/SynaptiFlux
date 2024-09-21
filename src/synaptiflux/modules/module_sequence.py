"""Implement a general sequence module."""
# Author: Garry Morrison
# Created: 2024-9-19
# Updated: 2024-9-19

from ..neural_module import NeuralModule
from ..source_fn import *
from ..trigger_fn import *
from ..pooling_fn import *
from ..synapse_fn import *
from ..action_fn import *

def module_sequence(name, max_digits):
    """Implement a general sequence module."""
    NM = NeuralModule(name)

    # set our sources:
    NM.add_source('#ON#', source_on())
    NM.add_source('#OFF#', source_off())
    NM.add_source('#INIT#', source_init())

    # set our default functions and parameters:
    NM.set_default_trigger(trigger_dot_product_threshold, {'threshold': 1})
    NM.set_default_pooling(pooling_or, {})
    NM.set_default_synapse(synapse_delayed_identity, {'sign': 1, 'delay': 0})
    NM.set_default_action(action_null, {})

    # define our init, carry and off neurons:
    NM.add_default_neuron('init flag', [1], ['#OFF#'])
    NM.add_default_neuron('carry flag', [1], ['#OFF#'])
    NM.add_default_neuron('off flag', [1], ['#OFF#'])

    # define their synapses:
    NM.add_default_synapse('init flag S0', 'init flag')
    NM.add_default_synapse('carry flag S0', 'carry flag')
    NM.add_default_synapse('off flag S0', 'off flag')

    # set our default functions and parameters:
    # NM.set_default_trigger(trigger_dot_product_threshold, {'threshold': 2})
    NM.set_default_pooling(pooling_sum_mod2, {})

    # add our starting sequence neuron and synapses:
    NM.add_default_neuron('0 neuron', [1,1], ['init flag S0', '0 neuron S0'])

    # set the new trigger threshold for the rest of our neurons:
    NM.set_default_trigger(trigger_dot_product_threshold, {'threshold': 2})

    NM.append_default_neuron_pattern('0 neuron', [1,1], ['0 neuron S0', 'carry flag S0'])
    NM.append_default_neuron_pattern('0 neuron', [1,1], ['0 neuron S0', 'off flag S0'])

    NM.add_default_synapse('0 neuron S0', '0 neuron')
    NM.add_synapse("0 neuron S0 delta", "0 neuron", synapse_delta_plus, {'sign': 1}, action_null, {})


    # Now, let's define the rest of them!
    # NM.add_default_neuron('1 neuron', [2,1,1], ['1 neuron S0','0 neuron S0','carry flag S0'])
    # NM.append_default_neuron_pattern('1 neuron', [1,1], ['1 neuron S0', 'carry flag S0'])
    # NM.append_default_neuron_pattern('1 neuron', [1,1], ['1 neuron S0', 'off flag S0'])
    # NM.add_default_synapse('0 neuron S0', '0 neuron')
    # NM.add_synapse("0 neuron S0 delta", "0 neuron", synapse_delta_plus, {'sign': 1}, action_null, {})

    for k in range(1, max_digits): # max_digits + 1?
        neuron_label = f"{k} neuron"
        synapse_label = f"{k} neuron S0"
        previous_synapse_label = f"{k-1} neuron S0"
        NM.add_default_neuron(neuron_label, [2,1,1], [synapse_label, previous_synapse_label, 'carry flag S0'])
        NM.append_default_neuron_pattern(neuron_label, [1,1], [synapse_label, 'carry flag S0'])
        NM.append_default_neuron_pattern(neuron_label, [1,1], [synapse_label, 'off flag S0'])
        NM.add_default_synapse(synapse_label, neuron_label)
        NM.add_synapse(synapse_label + " delta", neuron_label, synapse_delta_plus, {'sign': 1}, action_null, {})
    return NM

