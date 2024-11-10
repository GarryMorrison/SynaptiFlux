"""Testing NeuralModule global sequences."""
# Author: Garry Morrison
# Created: 2024-11-10
# Updated: 2024-11-10

import synaptiflux as sf

if __name__ == '__main__':
    print('Testing global sequences ...')

    NM = sf.NeuralModule('testing global sequences')
    s = '|H> . |i> => |Greetings!>'

    NM.from_map(s, verbose=False)
    NM.poke_neuron_sequence(['H', 'i'])
    NM.update_system(4)

    NM.append_to_global_sequence(layer=0, time_step=0, s = 'H')
    NM.append_to_global_sequence(layer=0, time_step=1, s = 'i')
    NM.append_to_global_sequence(layer=1, time_step=2, s = 'Greetings!')

    # print()
    NM.print_global_sequences(layers='*')

    NM.clear_global_sequences()
    s2 = '|op: age> + |Sam> => |39>'
    NM.from_map(s2, verbose=False)
    NM.poke_neurons(['op: age', 'Sam'])
    NM.update_system(4)
    NM.append_to_global_sequence(layer=0, time_step=4, s = 'op: age')
    NM.append_to_global_sequence(layer=0, time_step=4, s = 'Sam')
    NM.append_to_global_sequence(layer=1, time_step=5, s = '39')
    # print()
    NM.print_global_sequences(layers='*')

    # see what we have:
    # print(NM)
