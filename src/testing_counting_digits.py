"""A quick test of counting digits."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing counting digits:")

    NM = sf.NeuralModule('Couting digits example')
    NM.add_source('#ON#', sf.source_on())
    NM.add_source('#OFF#', sf.source_off())
    NM.add_source('#INIT#', sf.source_init())
    NM.add_neuron('carry flag', [1], ['#OFF#'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_or, {})
    NM.add_neuron('1 neuron', [1,1], ['#INIT#', '1 neuron S0'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_xor, {})
    NM.append_neuron_pattern('1 neuron', [1,1], ['1 neuron S0', 'carry flag S0'], sf.trigger_dot_product_threshold, {'threshold':2})
    NM.add_neuron('2 neuron', [2,1,1], ['2 neuron S0','1 neuron S0','carry flag S0'], sf.trigger_dot_product_threshold, {'threshold':2}, sf.pooling_xor, {})
    NM.append_neuron_pattern('2 neuron', [1,1], ['2 neuron S0', 'carry flag S0'], sf.trigger_dot_product_threshold, {'threshold':2})
    NM.add_neuron('3 neuron', [2,1,1], ['3 neuron S0','2 neuron S0','carry flag S0'], sf.trigger_dot_product_threshold, {'threshold':2}, sf.pooling_xor, {})
    NM.append_neuron_pattern('3 neuron', [1,1], ['3 neuron S0', 'carry flag S0'], sf.trigger_dot_product_threshold, {'threshold':2})
    NM.add_neuron('4 neuron', [2,1,1], ['4 neuron S0','3 neuron S0','carry flag S0'], sf.trigger_dot_product_threshold, {'threshold':2}, sf.pooling_xor, {})
    NM.append_neuron_pattern('4 neuron', [1,1], ['4 neuron S0', 'carry flag S0'], sf.trigger_dot_product_threshold, {'threshold':2})
    NM.add_synapse("carry flag S0", "carry flag", sf.synapse_delayed_identity, {'sign': 1, 'delay': 0}, sf.action_null, {})
    NM.add_synapse("1 neuron S0", "1 neuron", sf.synapse_delayed_identity, {'sign': 1, 'delay': 0}, sf.action_null, {})
    NM.add_synapse("2 neuron S0", "2 neuron", sf.synapse_delayed_identity, {'sign': 1, 'delay': 0}, sf.action_null, {})
    NM.add_synapse("3 neuron S0", "3 neuron", sf.synapse_delayed_identity, {'sign': 1, 'delay': 0}, sf.action_null, {})
    NM.add_synapse("4 neuron S0", "4 neuron", sf.synapse_delayed_identity, {'sign': 1, 'delay': 0}, sf.action_null, {})
    NM.update_system(4)
    NM.poke_neurons(['carry flag'])
    NM.update_system(4)
    NM.poke_neurons(['carry flag'])
    NM.update_system(4)
    NM.poke_neurons(['carry flag'])
    NM.update_system(4)
    NM.poke_neurons(['carry flag'])
    NM.update_system(4)
    print(NM)

