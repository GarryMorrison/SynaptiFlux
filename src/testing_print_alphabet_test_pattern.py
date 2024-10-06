"""A quick test of printing the start of the alphabet using default functions, and NM.get_test_neurons(pattern)."""
# Author: Garry Morrison
# Created: 2024-10-6
# Updated: 2024-10-6

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing printing the start of the alphabet:")

    # init our module:
    NM = sf.NeuralModule('print alphabet example')

    # set our sources:
    NM.add_source('#ON#', sf.source_on())
    NM.add_source('#OFF#', sf.source_off())
    NM.add_source('#INIT#', sf.source_init())

    # set our default functions and parameters:
    NM.set_default_trigger(sf.trigger_dot_product_threshold, {'threshold': 1})
    NM.set_default_pooling(sf.pooling_or, {})
    NM.set_default_synapse(sf.synapse_delayed_identity, {'sign': 1, 'delay': 0})
    NM.set_default_action(sf.action_null, {})

    # define our 'use capitals' neuron and synapses:
    NM.add_default_neuron('use capitals', 0, [1], ['#INIT#'])
    NM.add_default_synapse('use capitals S0', 'use capitals')
    NM.add_default_synapse('use capitals S0 not', 'use capitals')
    NM.update_synapse_fn('use capitals S0 not', sf.synapse_delayed_not, {'sign': 1, 'delay': 0})

    # define our input print neurons:
    NM.add_default_neuron('print A', 0, [1], ['#OFF#'])
    NM.add_default_neuron('print B', 0, [1], ['#OFF#'])
    NM.add_default_neuron('print C', 0, [1], ['#OFF#'])
    NM.add_default_neuron('print D', 0, [1], ['#OFF#'])

    # define our input print synapses:
    NM.add_default_synapse('print A S0', 'print A')
    NM.add_default_synapse('print B S0', 'print B')
    NM.add_default_synapse('print C S0', 'print C')
    NM.add_default_synapse('print D S0', 'print D')

    # update the default trigger:
    NM.set_default_trigger(sf.trigger_dot_product_threshold, {'threshold': 2})

    # now the print neurons:
    NM.add_default_neuron('print capital A', 1, [1,1], ['print A S0', 'use capitals S0'])
    NM.add_default_neuron('print capital B', 1, [1,1], ['print B S0', 'use capitals S0'])
    NM.add_default_neuron('print capital C', 1, [1,1], ['print C S0', 'use capitals S0'])
    NM.add_default_neuron('print capital D', 1, [1,1], ['print D S0', 'use capitals S0'])

    NM.add_default_neuron('print lower A', 1, [1,1], ['print A S0', 'use capitals S0 not'])
    NM.add_default_neuron('print lower B', 1, [1,1], ['print B S0', 'use capitals S0 not'])
    NM.add_default_neuron('print lower C', 1, [1,1], ['print C S0', 'use capitals S0 not'])
    NM.add_default_neuron('print lower D', 1, [1,1], ['print D S0', 'use capitals S0 not'])

    # now the print synapses:
    NM.add_default_synapse('print capital A S0', 'print capital A')
    NM.add_default_synapse('print capital B S0', 'print capital B')
    NM.add_default_synapse('print capital C S0', 'print capital C')
    NM.add_default_synapse('print capital D S0', 'print capital D')

    NM.add_default_synapse('print lower A S0', 'print lower A')
    NM.add_default_synapse('print lower B S0', 'print lower B')
    NM.add_default_synapse('print lower C S0', 'print lower C')
    NM.add_default_synapse('print lower D S0', 'print lower D')

    # update their actions:
    NM.update_synapse_action('print capital A S0', sf.action_println, {'s': 'A'})
    NM.update_synapse_action('print capital B S0', sf.action_println, {'s': 'B'})
    NM.update_synapse_action('print capital C S0', sf.action_println, {'s': 'C'})
    NM.update_synapse_action('print capital D S0', sf.action_println, {'s': 'D'})

    NM.update_synapse_action('print lower A S0', sf.action_println, {'s': 'a'})
    NM.update_synapse_action('print lower B S0', sf.action_println, {'s': 'b'})
    NM.update_synapse_action('print lower C S0', sf.action_println, {'s': 'c'})
    NM.update_synapse_action('print lower D S0', sf.action_println, {'s': 'd'})


    # NM.update_system(1)
    NM.poke_neuron('print A')
    NM.update_system(3)
    NM.poke_neuron('print B')
    NM.update_system(4)
    NM.poke_neuron('print C')
    NM.update_system(1)
    NM.poke_neuron('print D')
    NM.update_system(2)
    print(NM)

    print("\nTesting NM.get_test_neurons(pattern):")
    pattern0 = ['print A S0', 'use capitals S0']
    pattern1 = ['print C S0', 'use capitals S0 not']
    print("pattern0:", pattern0)
    print("pattern1:", pattern1)
    print("test pattern0:", NM.get_test_neurons(pattern0))
    print("test pattern1:", NM.get_test_neurons(pattern1))
