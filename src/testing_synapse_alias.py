"""Testing of neural module synapse aliases."""
# Author: Garry Morrison
# Created: 2024-11-4
# Updated: 2024-11-4

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing synapse aliases in neural modules:")

    # define our module:
    NM = sf.NeuralModule("Testing synapse aliases")
    NM.add_synapse_alias('alpha S0', 'a S0')

    # see what we have:
    print(NM)

