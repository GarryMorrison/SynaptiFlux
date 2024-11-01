"""Test the NM.from_map() method."""
# Author: Garry Morrison
# Created: 2024-11-1
# Updated: 2024-11-1

import synaptiflux as sf

if __name__ == '__main__':
    print('Testing the neural module from_map() method:')

    # load a sample file:
    filename = 'machines/Sam.map'
    NM = sf.NeuralModule('testing from_map method')
    NM.load_from_map(filename, verbose=True)

    # test poking:
    print()
    NM.poke_neurons(['Sam', 'op: mother'])
    NM.update_system(4)
    print()
    NM.poke_neurons(['Sam', 'op: friends'])
    NM.update_system(4)
    print()
    NM.poke_neuron('S')
    NM.update_system(1)
    NM.poke_neuron('a')
    NM.update_system(1)
    NM.poke_neuron('m')
    NM.update_system(3)
    print()

    # see what we have:
    print(NM)
