"""Testing of neural module synapse aliases."""
# Author: Garry Morrison
# Created: 2024-11-4
# Updated: 2024-11-4

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing synapse aliases in neural modules:")

    # define our module:
    NM = sf.NeuralModule("Testing synapse aliases")

    # NM.add_neuron(self, name, layer, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
    # layer 0:
    NM.add_neuron('a', 0, [1], ['#OFF'], sf.trigger_list_min_simm_threshold, {'threshold': 0.98}, sf.pooling_or, {})
    NM.add_neuron('b', 0, [1], ['#OFF'], sf.trigger_list_min_simm_threshold, {'threshold': 0.98}, sf.pooling_or, {})
    NM.add_neuron('alpha', 0, [1], ['#OFF'], sf.trigger_list_min_simm_threshold, {'threshold': 0.98}, sf.pooling_or, {})

    # layer 1:
    NM.add_neuron('a detected', 1, [1], ['a S0'], sf.trigger_list_min_simm_threshold, {'threshold': 0.98}, sf.pooling_or, {})
    NM.add_neuron('b detected', 1, [1], ['b S0'], sf.trigger_list_min_simm_threshold, {'threshold': 0.98}, sf.pooling_or, {})

    # NM.add_synapse(self, name, axon_name, synapse_fn_type, params, synapse_action_type, action_params)
    NM.add_synapse('a S0', 'a', sf.synapse_identity, {'sign': 1}, sf.action_time_step_println, {'s': 'a', 'NM': NM})
    NM.add_synapse('b S0', 'b', sf.synapse_identity, {'sign': 1}, sf.action_time_step_println, {'s': 'b', 'NM': NM})
    NM.add_synapse('alpha S0', 'alpha', sf.synapse_identity, {'sign': 1}, sf.action_time_step_println, {'s': 'alpha', 'NM': NM})
    NM.add_synapse('a detected S0', 'a detected', sf.synapse_identity, {'sign': 1}, sf.action_time_step_println, {'s': 'a detected', 'NM': NM})
    NM.add_synapse('b detected S0', 'b detected', sf.synapse_identity, {'sign': 1}, sf.action_time_step_println, {'s': 'b detected', 'NM': NM})

    # patch in our synapses:
    NM.patch_in_new_synapses()

    # add our alias:
    NM.add_synapse_alias('alpha S0', 'a S0')

    # poke and evolve the system:
    NM.poke_neuron('a')
    NM.update_system(3)

    NM.poke_neuron('b')
    NM.update_system(3)

    NM.poke_neuron('alpha')
    NM.update_system(3)

    # see what we have:
    print(NM)

