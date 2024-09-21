"""A quick test of the NeuralModule class."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18


import synaptiflux as sf

if __name__ == '__main__':
    print("Testing Neural Module:")

    NM = sf.NeuralModule('Jacob example') # initialize our neural system
    NM.add_source('#OFF#', sf.source_off()) # define various sources
    NM.add_source('#ON#', sf.source_on())
    NM.add_source('#INIT#', sf.source_init())
    NM.add_source('#ALT-2#', sf.source_alt_N(2))
    NM.add_source('#ALT-3#', sf.source_alt_N(3))
    NM.add_source('#ALT-4#', sf.source_alt_N(4))
    NM.add_source('#ALT-5#', sf.source_alt_N(5))
    NM.add_neuron('Jacob', [1], ['#INIT#'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_or, {})
    NM.add_synapse("Jacob 0", "Jacob", sf.synapse_delayed_identity, {'sign': 1, 'delay': 0}, sf.action_println, {'s': 'J'})
    NM.add_synapse("Jacob 1", "Jacob", sf.synapse_delayed_identity, {'sign': 1, 'delay': 1}, sf.action_println, {'s': 'a'})
    NM.add_synapse("Jacob 2", "Jacob", sf.synapse_delayed_identity, {'sign': 1, 'delay': 2}, sf.action_println, {'s': 'c'})
    NM.add_synapse("Jacob 3", "Jacob", sf.synapse_delayed_identity, {'sign': 1, 'delay': 3}, sf.action_println, {'s': 'o'})
    NM.add_synapse("Jacob 4", "Jacob", sf.synapse_delayed_identity, {'sign': 1, 'delay': 4}, sf.action_println, {'s': 'b'})
    print(NM)
    # NS.test_source('#ALT-4#', 15)
    # NS.update_sources()
    # NS.update_neurons()
    # NS.update_sources()
    NM.update_system(8)
    print(NM)
