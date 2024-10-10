"""Implement a general print symbols module that prints to a buffer and stores buffers to neurons."""
# Author: Garry Morrison
# Created: 2024-10-10
# Updated: 2024-10-10

from ..neural_module import NeuralModule
from ..source_fn import *
from ..trigger_fn import *
from ..pooling_fn import *
from ..synapse_fn import *
from ..action_fn import *
from ..buffer import *

def escape_symbol(s):
    """Escape symbols."""
    s = s.replace('\n', '\\n') # more later!
    return s

def module_store_buffer(name, symbols, infix_str):
    """Implement a general print symbols module that prints to a buffer."""
    # check infix_str is a string:
    if not isinstance(infix_str, str):
        raise TypeError(f"Expected a string, but got {type(infix_str).__name__}")

    # initialize our module:
    NM = NeuralModule(name)

    # Define our buffer:
    # buffer = Buffer("buffer: ")
    # buffer = Buffer("")
    global_buffer = Buffer("")
    store_buffer = Buffer("")

    # Define our action function:
    # action_fn = action_print_to_buffer
    action_fn = action_print_to_buffers

    # Define our flush function:
    action_flush_fn = action_print_to_buffer_flush

    # Define our store buffer function:
    action_store_fn = action_store_buffer

    # comment out for now:
    # set infix_str to "\n" if desire println property.
    # set our action function:
    # if append_newline:
    #     action_fn = action_println
    # else:
    #     action_fn = action_print

    # set our sources:
    NM.add_source('#ON#', source_on())
    NM.add_source('#OFF#', source_off())
    NM.add_source('#INIT#', source_init())

    # set our default functions and parameters:
    NM.set_default_trigger(trigger_dot_product_threshold, {'threshold': 1})
    NM.set_default_pooling(pooling_or, {})
    NM.set_default_synapse(synapse_delayed_identity, {'sign': 1, 'delay': 0})
    NM.set_default_action(action_null, {})

    # define our 'use capitals flag' neuron and synapses:
    NM.add_default_neuron('use capitals flag', 0, [1], ['#INIT#']) # set to #OFF# instead of #INIT#?
    NM.add_default_synapse('use capitals flag S0', 'use capitals flag')
    NM.add_default_synapse('use capitals flag S0 not', 'use capitals flag')
    NM.update_synapse_fn('use capitals flag S0 not', synapse_delayed_not, {'sign': 1, 'delay': 0})

    # define our 'flush buffer flag' neuron and synapse:
    NM.add_default_neuron('flush buffer flag', 0, [1], ['#OFF#'])
    NM.add_default_synapse('flush buffer flag S0', 'flush buffer flag')
    NM.update_synapse_fn('flush buffer flag S0', synapse_delayed_identity, {'sign': 1, 'delay': 1})
    NM.update_synapse_action('flush buffer flag S0', action_flush_fn, {'buffer': global_buffer, 's': ''})

    # define our 'store buffer flag' neuron and synapse:
    NM.add_default_neuron('store buffer flag', 0, [1], ['#OFF#'])
    NM.add_default_synapse('store buffer flag S0', 'store buffer flag')
    NM.update_synapse_fn('store buffer flag S0', synapse_delayed_identity, {'sign': 1, 'delay': 1})
    NM.update_synapse_action('store buffer flag S0', action_store_fn, {'NM': NM, 'buffer': store_buffer})

    # update the default trigger:
    NM.set_default_trigger(trigger_dot_product_threshold, {'threshold': 2})

    # now define the symbols neurons and synapses:
    for symbol in symbols:
        # action_fn(1, symbol) # quick test of action function

        # escape our symbol:
        escaped_symbol = escape_symbol(symbol)

        # define our labels:
        print_neuron = f"print {escaped_symbol}"
        print_synapse = f"print {escaped_symbol} S0"
        print_capital_neuron = f"print capital {escaped_symbol}"
        print_capital_synapse = f"print capital {escaped_symbol} S0"
        print_lower_neuron = f"print lower {escaped_symbol}"
        print_lower_synapse = f"print lower {escaped_symbol} S0"

        # define our neurons and synapses:
        NM.add_default_neuron(print_neuron, 0, [1], ['#OFF#'])
        NM.add_default_synapse(print_synapse, print_neuron)

        NM.add_default_neuron(print_capital_neuron, 1, [1,1], [print_synapse, 'use capitals flag S0'])
        NM.add_default_synapse(print_capital_synapse, print_capital_neuron)
        NM.update_synapse_action(print_capital_synapse, action_fn, {'buffer1': global_buffer, 'buffer2': store_buffer, 's': symbol.upper() + infix_str})

        NM.add_default_neuron(print_lower_neuron, 1, [1,1], [print_synapse, 'use capitals flag S0 not'])
        NM.add_default_synapse(print_lower_synapse, print_lower_neuron)
        NM.update_synapse_action(print_lower_synapse, action_fn, {'buffer1': global_buffer, 'buffer2': store_buffer, 's': symbol + infix_str})

    return NM
