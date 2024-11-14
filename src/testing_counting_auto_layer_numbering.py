"""Testing auto layer learning in .map format for our counting example."""
# Author: Garry Morrison
# Created: 2024-11-14
# Updated: 2024-11-14

import synaptiflux as sf

if __name__ == '__main__':
    print('Testing auto layer learning in our counting example')

    NM = sf.NeuralModule('testing auto layer learning while counting')
    s = """
|count to two> |=> |0> . |1> . |2>
|op: word> => |word mode on neuron>
|word mode on neuron> |=> |op: word>
|word mode off neuron> |=> -1 |op: word>
|op: word> + |0> => |zero>
|op: word> + |1> => |one>
|op: word> + |2> => |two>
"""
    NM.from_map(s, verbose=True)

    # see what we have:
    print(NM)
