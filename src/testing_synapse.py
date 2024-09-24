"""Just a quick test of the synapse class."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

import synaptiflux as sf

if __name__ == '__main__':
    print("Let's implement a couple of sample synapses:")

    S0 = sf.Synapse("alpha S0", "alpha", sf.synapse_identity, {'sign': 1}, sf.action_null, {})
    S0.append_to_history(0)
    S0.append_to_history(5)
    S0.append_to_history(8)
    S0.append_to_history(3)
    S0.append_to_history(0)
    S0.append_to_history(1)
    print(S0)

    S1 = sf.Synapse("beta S0", "beta", sf.synapse_delayed_identity, {'sign': 1, 'delay': 3}, sf.action_println, {'s': 'beta activated!'})
    S1.append_to_history(0)
    S1.append_to_history(0)
    S1.append_to_history(0)
    print(S1)

    S2 = sf.Synapse("gamma S0", "gamma", sf.synapse_delayed_identity, {'sign': -1, 'delay': 2}, sf.action_null, {})
    S2.append_to_history(0)
    S2.append_to_history(0)
    S2.append_to_history(0)
    print(S2)
