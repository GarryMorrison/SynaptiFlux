"""Testing neuron -> synapse map rules."""
# Author: Garry Morrison
# Created: 2024-11-4
# Updated: 2024-11-4

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing neuron to synapse learn rules in the map format:")

    filename0 = 'machines/spelling-Sam.map'
    NM0 = sf.NeuralModule('testing neuron synapse map learn rules')
    NM0.load_from_map(filename0, verbose=True)

    # see what we have:
    # print(NM0)

    # now poke and evolve:
    # NM0.poke_neuron('spelling of Sam') # works!
    # NM0.update_system(5)

    print()
    NM0.poke_neurons(['Sam', 'op: spelling'])
    NM0.update_system(10)

    print()
    filename1 = 'machines/alpha-beta.map'
    NM1 = sf.NeuralModule('testing alpha beta map')
    NM1.load_from_map(filename1, verbose=True)

    # see what we have:
    # print(NM1)

    # now poke and evolve:
    print()
    NM1.poke_neuron('alpha beta')
    NM1.update_system(10)


