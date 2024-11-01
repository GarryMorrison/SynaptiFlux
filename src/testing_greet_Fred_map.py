"""Test the NM.from_map() method using the Greet Fred machine."""
# Author: Garry Morrison
# Created: 2024-11-2
# Updated: 2024-11-2

import synaptiflux as sf

if __name__ == '__main__':
    print('Testing the neural module from_map() method using the Greet Fred machine:')

    # load a sample file:
    filename = 'machines/greet-Fred.map'
    NM = sf.NeuralModule('testing from_map method using Greet Fred machine')
    NM.load_from_map(filename, verbose=True)

    # test poking:
    print()
    NM.poke_neuron_sequence(list('Hey Fred. Afternoon Robo'))
    NM.update_system(30)
    print()

    # see what we have:
    # print(NM)
