"""Just a quick test of the neuron system class."""
# Author: Garry Morrison
# Created: 2024-9-20
# Updated: 2024-9-21

import synaptiflux as sf
import synaptiflux.modules.module_sequence
import synaptiflux.modules.module_print_symbols

if __name__ == '__main__':
    print("Let's implement a couple of sample modules in a neural system:")

    NS = sf.NeuralSystem('sequence example system')
    NS.add_source('#OFF#', sf.source_off()) # define various sources
    NS.add_source('#ON#', sf.source_on())
    NS.add_source('#INIT#', sf.source_init())
    NS.add_source('#ALT-3#', sf.source_alt_N(3))

    NM_sequence = sf.modules.module_sequence.module_sequence('sequence module', 4)
    NS.register_module('sequence module', NM_sequence)
    NS.register_module_inputs('sequence module',
                              [['#INIT#', 'init flag'],
                              ['#ALT-3#', 'carry flag'],
                              ['#OFF#', 'off flag']])
    NS.register_module_outputs('sequence module',
                               [['0 neuron S0 delta', '!seq-0!'],
                               ['1 neuron S0 delta', '!seq-1!'],
                               ['2 neuron S0', '!seq-2!'],
                               ['3 neuron S0 delta', '!seq-3!'],
                               ['4 neuron S0 delta', '!seq-4!']])

    NM_print_sequence = sf.modules.module_print_symbols.module_print_symbols('print alphabet module', 'abcd', append_newline=True)
    NS.register_module('print alphabet module', NM_print_sequence)
    NS.register_module_inputs('print alphabet module',
                              # [['#OFF#', 'use capitals'],
                              [['!seq-0!', 'use capitals'],
                              ['!seq-0!', 'print a'],
                              ['!seq-1!', 'print b'],
                              ['!seq-2!', 'use capitals'],
                              ['!seq-2!', 'print c'],
                              ['!seq-3!', 'print d'],
                              ['!seq-4!', 'print e']])

    NS.update_system(20)
    print(NS)


