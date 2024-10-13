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
    seq0 = 'Hello, Hello!'
    print(f"The sequence to process: {seq0}")
    NS0 = sf.systems.system_print_sequence.system_symbol_sequence('example sequence system', seq0, ' ,.!?', verbose=False)

    # see what we have:
    NS0.update_system(20)
    # print(NS0)

    # next sequence:
    print("\n----------------------------------------")
    seq1 = 'Hello, Hlelo!' # note the deliberate typo!
    print(f"The sequence to process: {seq1}")
    NS1 = sf.systems.system_print_sequence.system_symbol_sequence('example sequence system', seq1, ' ,.!?', verbose=False)
    NS1.update_system(20)
    # print(NS1)

    # next sequence:
    print("\n----------------------------------------")
    seq2 = 'Hello World!'
    print(f"The sequence to process: {seq2}")
    NS2 = sf.systems.system_print_sequence.system_symbol_sequence('example sequence system', seq2, ' ,.!?', verbose=False)
    NS2.update_system(20)
    # print(NS2)
