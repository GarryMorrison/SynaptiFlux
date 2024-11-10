"""Testing auto-learning layer numbers in NM.from_map()."""
# Author: Garry Morrison
# Created: 2024-11-10
# Updated: 2024-11-10

import synaptiflux as sf

if __name__ == '__main__':
    print('Testing auto-learning layers in NM.from_map() ...')

    NM = sf.NeuralModule('testing auto-learning')
    s = '|H> . |i> => |Greetings!>'

    NM.from_map(s, verbose=True)

    # see what we have:
    print(NM)
