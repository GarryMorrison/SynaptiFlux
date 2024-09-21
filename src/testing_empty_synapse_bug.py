"""Just a quick test of the empty synapse bug. Fixed!"""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

import synaptiflux as sf

if __name__ == '__main__':
    print("Let's implement a sample buggy neuron:")

    NM = sf.NeuralModule('buggy neuron example') # initialize our neural system
    NM.add_source('#OFF#', sf.source_off()) # define various sources
    NM.add_source('#ON#', sf.source_on())
    NM.add_source('#INIT#', sf.source_init())
    NM.add_source('#ALT-2#', sf.source_alt_N(2))
    NM.add_source('#ALT-3#', sf.source_alt_N(3))
    NM.add_source('#ALT-4#', sf.source_alt_N(4))
    NM.add_source('#ALT-5#', sf.source_alt_N(5))
    NM.add_neuron('first neuron', [1,-10], ['#ON#', 'bogus S0'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_or, {})
    NM.add_synapse("first neuron S0", "first neuron", sf.synapse_delayed_identity, {'sign': 1, 'delay': 0}, sf.action_null, {})
    NM.update_system(6)
    print(NM)

