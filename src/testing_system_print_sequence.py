"""Using a print sequence system to print 'Hello World!'."""
# Author: Garry Morrison
# Created: 2024-10-9
# Updated: 2024-10-11

import synaptiflux as sf
import synaptiflux.systems.system_print_sequence
# import synaptiflux.modules.module_sequence
# import synaptiflux.modules.module_print_symbols
# import synaptiflux.modules.module_print_symbols_to_buffer

if __name__ == '__main__':
    print("Let's implement 'Hello World!' in a print sequence system:")

    # initialize our system:
    # NS = sf.systems.system_print_sequence.system_symbol_sequence('example sequence system', 'Hello World!', ' ,.!?')
    NS = sf.systems.system_print_sequence.system_symbol_sequence('example sequence system', 'Hello, Hello!', ' ,.!?')

    # see what we have:
    NS.update_system(20)
    print(NS)
