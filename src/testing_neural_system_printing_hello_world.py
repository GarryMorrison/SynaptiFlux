"""Using a neural system to print 'Hello World!'."""
# Author: Garry Morrison
# Created: 2024-9-21
# Updated: 2024-9-21

import synaptiflux as sf
import synaptiflux.modules.module_sequence
import synaptiflux.modules.module_print_symbols

if __name__ == '__main__':
    print("Let's implement 'Hello World!' in a neural system:")

    NS = sf.NeuralSystem('sequence example system')
    NS.add_source('#OFF#', sf.source_off()) # define various sources
    NS.add_source('#ON#', sf.source_on())
    NS.add_source('#INIT#', sf.source_init())
    NS.add_source('#ALT-1#', sf.source_alt_N(1))

    NM_sequence = sf.modules.module_sequence.module_sequence('sequence module', 13)
    NS.register_module('sequence module', NM_sequence)
    NS.register_module_inputs('sequence module',
                              [['#INIT#', 'init flag'],
                              ['#ALT-1#', 'carry flag'],
                              ['#OFF#', 'off flag']])
    NS.register_module_outputs('sequence module',
                               [['0 neuron S0 delta', '!seq-0!'],
                               ['1 neuron S0 delta', '!seq-1!'],
                               ['2 neuron S0 delta', '!seq-2!'],
                               ['3 neuron S0 delta', '!seq-3!'],
                               ['4 neuron S0 delta', '!seq-4!'],
                               ['5 neuron S0 delta', '!seq-5!'],
                               ['6 neuron S0 delta', '!seq-6!'],
                               ['7 neuron S0 delta', '!seq-7!'],
                               ['8 neuron S0 delta', '!seq-8!'],
                               ['9 neuron S0 delta', '!seq-9!'],
                               ['10 neuron S0 delta', '!seq-10!'],
                               ['11 neuron S0 delta', '!seq-11!'],
                               ['12 neuron S0 delta', '!seq-12!']])

    NM_print_sequence = sf.modules.module_print_symbols.module_print_symbols('print alphabet module', 'dehlorw !\n', append_newline=False)
    NS.register_module('print alphabet module', NM_print_sequence)
    NS.register_module_inputs('print alphabet module',
                              # [['#OFF#', 'use capitals'],
                              [['!seq-0!', 'use capitals'],
                              ['!seq-0!', 'print h'],
                              ['!seq-1!', 'print e'],
                              ['!seq-2!', 'print l'],
                              ['!seq-3!', 'print l'],
                              ['!seq-4!', 'print o'],
                              ['!seq-5!', 'print  '],
                              ['!seq-6!', 'use capitals'],
                              ['!seq-6!', 'print w'],
                              ['!seq-7!', 'print o'],
                              ['!seq-8!', 'print r'],
                              ['!seq-9!', 'print l'],
                              ['!seq-10!', 'print d'],
                              ['!seq-11!', 'print !'],
                              ['!seq-12!', 'print \\n']])

    NS.update_system(20)
    print(NS)


