"""A quick test of counting digits using default functions."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-29

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing counting digits using default functions to clean the code somewhat:")

    # init our module:
    NM = sf.NeuralModule('Couting digits example')

    # set our sources:
    NM.add_source('#ON#', sf.source_on())
    NM.add_source('#OFF#', sf.source_off())
    NM.add_source('#INIT#', sf.source_init())

    # set our default functions and parameters:
    NM.set_default_trigger(sf.trigger_dot_product_threshold, {'threshold': 2})
    # NM.set_default_pooling(sf.pooling_xor, {})
    NM.set_default_pooling(sf.pooling_sum_mod2, {})
    NM.set_default_synapse(sf.synapse_delayed_identity, {'sign': 1, 'delay': 0})
    NM.set_default_action(sf.action_null, {})

    # define our init and carry neuron:
    NM.add_neuron('init flag', 0, [1], ['#OFF#'], sf.trigger_dot_product_threshold, {'threshold': 1}, sf.pooling_or, {})
    NM.add_neuron('carry flag', 0, [1], ['#OFF#'], sf.trigger_dot_product_threshold, {'threshold': 1}, sf.pooling_or, {})
    NM.add_neuron('off flag', 0, [1], ['#OFF#'], sf.trigger_dot_product_threshold, {'threshold': 1}, sf.pooling_or, {})
    # NM.add_neuron('carry or off flag', [1,1], ['carry flag S0', 'off flag S0'], sf.trigger_dot_product_threshold, {'threshold': 1}, sf.pooling_or, {})

    # define our starting digit:
    # NM.add_neuron('0 neuron', [1,1], ['#INIT#', '0 neuron S0'], sf.trigger_dot_product_threshold, {'threshold': 1}, sf.pooling_xor, {})
    # NM.append_neuron_pattern('0 neuron', [1,1], ['0 neuron S0', 'carry flag S0'], sf.trigger_dot_product_threshold, {'threshold': 2})
    NM.add_neuron('0 neuron', 1, [1,1], ['init flag S0', '0 neuron S0'], sf.trigger_dot_product_threshold, {'threshold': 1}, sf.pooling_sum_mod2, {})
    NM.append_default_neuron_pattern('0 neuron', [1,1], ['0 neuron S0', 'carry flag S0'])
    NM.append_default_neuron_pattern('0 neuron', [1,1], ['0 neuron S0', 'off flag S0'])

    # define the rest of our digit neurons:
    NM.add_default_neuron('1 neuron', 1, [2,1,1], ['1 neuron S0','0 neuron S0','carry flag S0'])
    NM.append_default_neuron_pattern('1 neuron', [1,1], ['1 neuron S0', 'carry flag S0'])
    NM.append_default_neuron_pattern('1 neuron', [1,1], ['1 neuron S0', 'off flag S0'])

    NM.add_default_neuron('2 neuron', 1, [2,1,1], ['2 neuron S0','1 neuron S0','carry flag S0'])
    NM.append_default_neuron_pattern('2 neuron', [1,1], ['2 neuron S0', 'carry flag S0'])
    NM.append_default_neuron_pattern('2 neuron', [1,1], ['2 neuron S0', 'off flag S0'])

    NM.add_default_neuron('3 neuron', 1, [2,1,1], ['3 neuron S0','2 neuron S0','carry flag S0'])
    NM.append_default_neuron_pattern('3 neuron', [1,1], ['3 neuron S0', 'carry flag S0'])
    NM.append_default_neuron_pattern('3 neuron', [1,1], ['3 neuron S0', 'off flag S0'])

    NM.add_default_neuron('4 neuron', 1, [2,1,1], ['4 neuron S0','3 neuron S0','carry flag S0'])
    NM.append_default_neuron_pattern('4 neuron', [1,1], ['4 neuron S0', 'carry flag S0'])
    NM.append_default_neuron_pattern('4 neuron', [1,1], ['4 neuron S0', 'off flag S0'])


    # define the synapses:
    NM.add_default_synapse('init flag S0', 'init flag')
    NM.add_default_synapse('carry flag S0', 'carry flag')
    NM.add_default_synapse('off flag S0', 'off flag')
    # NM.add_default_synapse('carry or off flag S0', 'carry or off flag')
    NM.add_default_synapse('0 neuron S0', '0 neuron')
    NM.add_default_synapse('1 neuron S0', '1 neuron')
    NM.add_default_synapse('2 neuron S0', '2 neuron')
    NM.add_default_synapse('3 neuron S0', '3 neuron')
    NM.add_default_synapse('4 neuron S0', '4 neuron')

    # time evolve the system, with some pokes to increment the current active digit:
    NM.update_system(3)
    NM.poke_neuron('init flag')
    NM.update_system(4) # 0
    NM.poke_neuron('carry flag')
    NM.update_system(4) # 1
    NM.poke_neuron('carry flag')
    NM.update_system(4) # 2
    NM.poke_neuron('carry flag')
    NM.update_system(4) # 3
    NM.poke_neuron('carry flag')
    NM.update_system(6) # 4
    NM.poke_neuron('off flag')
    NM.update_system(4)
    print(NM)



