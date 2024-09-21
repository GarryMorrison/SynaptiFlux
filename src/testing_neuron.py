"""Just a quick test of the neuron class."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

import synaptiflux as sf

if __name__ == '__main__':
    print("Let's implement a couple of sample neurons:")

    N0 = sf.Neuron("first neuron", [0,1,2], ['alpha 0', 'beta 0', 'gamma 0'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_or, {})
    N0.append_pattern([1,1], ['X', 'Y'], sf.trigger_dot_product_threshold, {'threshold':1})
    N0.append_pattern([3,5,2], ['u', 'v', 'w'], sf.trigger_dot_product_threshold, {'threshold':1})
    N0.update_pattern(1, [7,7,7], ['X', 'Y', 'Z'])
    N0.append_to_axon(0)
    N0.append_to_axon(1)
    print(N0)

    N1 = sf.Neuron("second neuron", [1,1,1,1,1], ['a', 'b', 'c', 'd', 'e'], sf.trigger_dot_product_threshold, {'threshold':1}, sf.pooling_or, {})
    N1.append_to_axon(1)
    N1.append_to_axon(1)
    N1.append_to_axon(0)
    N1.append_to_axon(1)
    N1.append_to_axon(0)
    print(N1)
