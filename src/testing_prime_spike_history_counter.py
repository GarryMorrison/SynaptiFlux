"""A quick test of generating a prime spike history, using the counter class."""
# Author: Garry Morrison
# Created: 2024-10-31
# Updated: 2024-10-31

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing prime spike history:")

    counter = sf.Counter()

    NM = sf.NeuralModule('Prime numbers less than 25')
    NM.add_source('#INIT#', sf.source_init())
    NM.add_source('#ALT-2#', sf.source_alt_N(2))
    NM.add_source('#ALT-3#', sf.source_alt_N(3))
    NM.add_source('#ALT-5#', sf.source_alt_N(5))
    NM.add_neuron('not prime', 1, [-10, -10, -10, 1,1,1,1], ['init S0 D1','init S0 D2','init S0 D4', 'init S0 D0','#ALT-2#','#ALT-3#','#ALT-5#'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_or, {})
    NM.add_neuron('init neuron', 0, [1], ['#INIT#'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_or, {})
    NM.add_synapse("init S0", "init neuron", sf.synapse_delayed_identity, {'sign': 1, 'delay': 0}, sf.action_null, {})
    NM.add_synapse("not prime S0", "not prime", sf.synapse_delayed_identity, {'sign': 1, 'delay': 0}, sf.action_counter_println, {'s': 'not prime', 'counter': counter})
    NM.add_synapse("not prime S1", "not prime", sf.synapse_delayed_not, {'sign': 1, 'delay': 0}, sf.action_counter_println, {'s': 'prime', 'counter': counter})
    NM.update_system(25)
    print(NM)

    print('\nActive synapses:')
    layers = '*'
    delays = [0,1,2,3,4]
    print(sf.display_layer_synapse_dict(NM.get_active_synapses(layers, delays)))
