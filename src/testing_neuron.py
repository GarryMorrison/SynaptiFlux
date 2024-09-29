"""Just a quick test of the neuron class."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

import synaptiflux as sf

if __name__ == '__main__':
    print("Let's implement a couple of sample neurons:")

    N0 = sf.Neuron("first neuron", 0, [0,1,2,3], ['alpha S0', 'beta S0', 'gamma S0', 'delta S0'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_or, {})
    N0.append_pattern([1,1], ['X S0', 'Y S0'], sf.trigger_dot_product_threshold, {'threshold':1})
    N0.append_pattern([3,5,2], ['u S0', 'v S0', 'w S0'], sf.trigger_dot_product_threshold, {'threshold':1})
    N0.update_pattern(1, [7,7,7], ['X S0', 'Y S0', 'Z S0'])
    N0.append_to_axon(0)
    N0.append_to_axon(1)
    print(N0)

    N1 = sf.Neuron("second neuron", 1, [1,1,1,1,1], ['a S0', 'b S0', 'c S0', 'd S0', 'e S0'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_or, {})
    N1.append_to_axon(1)
    N1.append_to_axon(1)
    N1.append_to_axon(0)
    N1.append_to_axon(1)
    N1.append_to_axon(0)
    print(N1)
