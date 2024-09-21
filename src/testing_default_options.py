"""A quick test of neural module default settings and updating them."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

import synaptiflux as sf

if __name__ == '__main__':
    print("Test of neural model default settings:")

    NM = sf.NeuralModule('Default settings example')
    NM.set_default_trigger(sf.trigger_dot_product_threshold, {'threshold': 1})
    NM.set_default_pooling(sf.pooling_or, {})
    NM.set_default_synapse(sf.synapse_delayed_identity, {'sign': 1, 'delay': 0})
    NM.set_default_action(sf.action_null, {})
    NM.add_default_neuron('first neuron', [1,2,3], ['alpha', 'beta', 'gamma'])
    NM.append_default_neuron_pattern('first neuron', [1,1], ['X', 'Y'])
    print(NM)

    print('\n-------------------------')
    print('updated neural module')
    NM.update_neuron_pooling('first neuron', sf.pooling_xor, {})
    # NM.update_neuron_trigger('first neuron', 1, sf.action_println, {'s': 'first neuron'}) # actions are not triggers!
    print(NM)

    print('\n-------------------------')
    print('add default synapse')
    NM.add_default_synapse('first neuron S0', 'first neuron')
    NM.add_default_synapse('first neuron S1', 'first neuron')
    NM.update_synapse_fn('first neuron S1', sf.synapse_sum, {'sign': 1, 'width': 5})
    NM.update_synapse_action('first neuron S1', sf.action_println, {'s': 'first neuron S1'})
    print(NM)
