"""A quick test of generating a prime spike history."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing prime spike history:")

    NM = sf.NeuralModule('Prime numbers less than 25')
    NM.add_source('#INIT#', sf.source_init())
    NM.add_source('#ALT-2#', sf.source_alt_N(2))
    NM.add_source('#ALT-3#', sf.source_alt_N(3))
    NM.add_source('#ALT-5#', sf.source_alt_N(5))
    # NS.add_neuron('prime', [1,1,1], ['#ALT-2#','#ALT-3#','#ALT-5#'], trigger_dot_product_threshold, {'threshold':1}, pooling_or, {})
    NM.add_neuron('not prime', [-10, -10, -10, 1,1,1,1], ['init delay 1','init delay 2','init delay 4', 'init delay 0','#ALT-2#','#ALT-3#','#ALT-5#'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_or, {})
    NM.add_neuron('init neuron', [1], ['#INIT#'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_or, {})
    NM.add_synapse("init delay 0", "init neuron", sf.synapse_delayed_identity, {'sign': 1, 'delay': 0}, sf.action_null, {})
    NM.add_synapse("init delay 1", "init neuron", sf.synapse_delayed_identity, {'sign': 1, 'delay': 1}, sf.action_null, {})
    NM.add_synapse("init delay 2", "init neuron", sf.synapse_delayed_identity, {'sign': 1, 'delay': 2}, sf.action_null, {})
    NM.add_synapse("init delay 4", "init neuron", sf.synapse_delayed_identity, {'sign': 1, 'delay': 4}, sf.action_null, {})
    NM.add_synapse("not prime S0", "not prime", sf.synapse_delayed_identity, {'sign': 1, 'delay': 0}, sf.action_println, {'s': 'not prime'})
    NM.add_synapse("not prime S1", "not prime", sf.synapse_delayed_not, {'sign': 1, 'delay': 0}, sf.action_println, {'s': 'prime'})
    NM.update_system(25)
    print(NM)

