"""Just a quick test of our sf print symbols module."""
# Author: Garry Morrison
# Created: 2024-9-19
# Updated: 2024-9-19

import synaptiflux as sf
import synaptiflux.modules.module_print_symbols

if __name__ == '__main__':
    print("Let's implement a sf print alphabet module:")

    NM = sf.modules.module_print_symbols.module_print_symbols('print alphabet', 'abcd', append_newline=True)
    # NM.update_system(1)
    NM.poke_neuron('print a')
    NM.update_system(3)
    NM.poke_neuron('print b')
    NM.update_system(4)
    NM.poke_neuron('print c')
    NM.update_system(1)
    NM.poke_neuron('print d')
    NM.update_system(2)
    print(NM)

    # quick test of synapse read:
    # print('Synapse lower d:', NM.read_synapse('print lower d S0'))
