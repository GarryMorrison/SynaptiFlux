"""Implement a general print sequence system that prints to a buffer."""
# Author: Garry Morrison
# Created: 2024-10-9
# Updated: 2024-10-10

from ..neural_system import NeuralSystem
from ..modules import module_sequence
# from ..modules import module_print_symbols_to_buffer
from ..modules import module_store_buffer
from ..source_fn import *

def system_symbol_sequence(name, symbol_sequence, punctuation_symbols):
    """Implement a system to print a sequence."""
    # initialize our system:
    NS = NeuralSystem(name)

    # switch off active synapse display for now:
    NS.enable_active_synapses(False)

    # some prelims:
    seq_len = len(symbol_sequence)
    symbol_set = set([x.lower() for x in symbol_sequence])
    punctuation_set = set(punctuation_symbols) # not currently used. Implement later.

    # add our sources:
    NS.add_source('#OFF#', source_off()) # define various sources
    NS.add_source('#ON#', source_on())
    NS.add_source('#INIT#', source_init())
    NS.add_source('#ALT-1#', source_alt_N(1))

    # add our sequence module:
    NM_sequence = module_sequence.module_sequence('sequence module', seq_len + 2)
    NS.register_module('sequence module', NM_sequence)
    NS.register_module_inputs('sequence module',
                              [['#INIT#', 'init flag'],
                              ['#ALT-1#', 'carry flag'],
                              ['#OFF#', 'off flag']])

    # create our outputs list:
    outputs_list = []
    for k in range(seq_len + 2):
        synapse = f"{k} neuron S0 delta"
        channel = f"!seq-{k}!"
        outputs_list.append([synapse, channel])

    # now register them:
    NS.register_module_outputs('sequence module', outputs_list)


    # add our print sequence module:
    NM_print_symbols = module_store_buffer.module_store_buffer('print symbols module', sorted(symbol_set), infix_str = "")
    NS.register_module('print symbols module', NM_print_symbols)

    # create our outputs list:
    inputs_list = []
    for k in range(seq_len):
        channel = f"!seq-{k}!"
        neuron = f"print {symbol_sequence[k].lower()}"
        if symbol_sequence[k].isupper():
            inputs_list.append([channel, "use capitals flag"])
        inputs_list.append([channel, neuron])
        if symbol_sequence[k] in punctuation_set:
            inputs_list.append([channel, "store buffer flag"])
    flush_channel = f"!seq-{seq_len}!"
    inputs_list.append([flush_channel, "flush buffer flag"]) # be sure to flush our buffer!

    # now register them:
    NS.register_module_inputs('print symbols module', inputs_list)

    # return our constructed system:
    return NS

