"""Just a quick test of our sf sequence module."""
# Author: Garry Morrison
# Created: 2024-9-19
# Updated: 2024-9-19

import synaptiflux as sf
import synaptiflux.modules.module_sequence

if __name__ == '__main__':
    print("Let's implement a sf sequence module:")

    NM = sf.modules.module_sequence.module_sequence('test sequence module', 5)
    NM.update_system(3)
    NM.poke_neuron('init flag')
    NM.update_system(4) # 0
    NM.poke_neuron('carry flag')
    NM.update_system(4) # 1
    NM.poke_neuron('carry flag')
    NM.update_system(4) # 2
    NM.poke_neuron('carry flag')
    NM.update_system(4) # 3
    NM.poke_neuron('carry flag')
    NM.update_system(6) # 4
    NM.poke_neuron('off flag')
    NM.update_system(4)
    print(NM)


