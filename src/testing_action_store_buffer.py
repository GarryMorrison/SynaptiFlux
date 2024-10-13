"""Testing our action store buffer code."""
# Author: Garry Morrison
# Created: 2024-10-13
# Updated: 2024-10-13

import synaptiflux as sf
import synaptiflux.systems.system_print_sequence
# import synaptiflux.modules.module_sequence
# import synaptiflux.modules.module_print_symbols
# import synaptiflux.modules.module_print_symbols_to_buffer

if __name__ == '__main__':
    print("Let's implement some character sequences using a system and action_store_buffer:")

    # initialize our system:
    seq = 'Hello, Hello!'
    print(f"The sequence to process: {seq}")
    NS0 = sf.systems.system_print_sequence.system_symbol_sequence('example sequence system', seq, ' ,.!?', verbose=False)

    # see what we have:
    NS0.update_system(20)
    # print(NS0)
