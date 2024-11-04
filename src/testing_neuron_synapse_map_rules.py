"""Testing neuron -> synapse map rules."""
# Author: Garry Morrison
# Created: 2024-11-4
# Updated: 2024-11-4

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing neuron to synapse learn rules in the map format:")

    filename0 = 'machines/spelling-Sam.map'
    NM = sf.NeuralModule('testing neuron synapse map learn rules')
    NM.load_from_map(filename0, verbose=True)

    # see what we have:
    print(NM)

    # now poke and evolve:
    NM.poke_neuron('spelling of Sam')
    NM.update_system(5)

