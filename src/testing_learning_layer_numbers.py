"""Testing auto learning layer numbers in .map notation."""
# Author: Garry Morrison
# Created: 2024-11-14
# Updated: 2024-11-14

import synaptiflux as sf

if __name__ == '__main__':
    print('Testing auto layer numbers ...')

    NM = sf.NeuralModule('Testing auto layer numbers')
    s = """
-- layer(N1) = max(layer(N1), layer(S0) + 1)
|S0> => |N1>

-- layer(S3) = max(layer(S3), layer(N2) + 1)
|N2> |=> |S3>
"""
    NM.from_map(s, verbose=True)

    # see what we have:
    print(NM)
