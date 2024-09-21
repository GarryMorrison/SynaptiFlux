"""Just a quick test of the neuron system class."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

import synaptiflux as sf

if __name__ == '__main__':
    print("Let's implement a couple of sample modules in a neural system:")

    NS = sf.NeuralSystem('sequence example system')
    NS.add_source('#OFF#', sf.source_off()) # define various sources
    NS.add_source('#ON#', sf.source_on())
    NS.add_source('#INIT#', sf.source_init())

    NM_sequence = sf.NeuralModule('sequence module')
    NM_print_sequence = sf.NeuralModule('print alphabet module')
    NS.register_module('sequence module', NM_sequence)
    NS.register_module_input('sequence module', '!start-seq!', 'init flag')
    NS.register_module_input('sequence module', '!inc-seq!', 'carry flag')
    NS.register_module_input('sequence module', '!stop-seq!', 'off flag')
    NS.register_module_output('sequence module', '0 neuron S0', '!seq-0!')
    NS.register_module_output('sequence module', '1 neuron S0', '!seq-1!')
    NS.register_module_output('sequence module', '2 neuron S0', '!seq-2!')
    NS.register_module_output('sequence module', '3 neuron S0', '!seq-3!')
    NS.register_module_output('sequence module', '4 neuron S0', '!seq-4!')
    NS.register_module('print alphabet module', NM_print_sequence)
    NS.register_module_input('print alphabet module', '#ON#', 'use capitals')
    NS.register_module_input('print alphabet module', '!seq-0!', 'print A')
    NS.register_module_input('print alphabet module', '!seq-1!', 'print B')
    NS.register_module_input('print alphabet module', '!seq-2!', 'print C')
    NS.register_module_input('print alphabet module', '!seq-3!', 'print D')
    NS.register_module_input('print alphabet module', '!seq-4!', 'print E')
    print(NS)


