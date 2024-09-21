"""Implement a general print symbols module."""
# Author: Garry Morrison
# Created: 2024-9-19
# Updated: 2024-9-21

from ..neural_module import NeuralModule
from ..source_fn import *
from ..trigger_fn import *
from ..pooling_fn import *
from ..synapse_fn import *
from ..action_fn import *

def escape_symbol(s):
    """Escape symbols."""
    s = s.replace('\n', '\\n') # more later!
    return s

def module_print_symbols(name, symbols, append_newline):
    """Implement a general print symbols module."""
    NM = NeuralModule(name)

    # set our action function:
    if append_newline:
        action_fn = action_println
    else:
        action_fn = action_print

    # set our sources:
    NM.add_source('#ON#', source_on())
    NM.add_source('#OFF#', source_off())
    NM.add_source('#INIT#', source_init())

    # set our default functions and parameters:
    NM.set_default_trigger(trigger_dot_product_threshold, {'threshold': 1})
    NM.set_default_pooling(pooling_or, {})
    NM.set_default_synapse(synapse_delayed_identity, {'sign': 1, 'delay': 0})
    NM.set_default_action(action_null, {})

    # define our 'use capitals' neuron and synapses:
    NM.add_default_neuron('use capitals', [1], ['#INIT#'])
    NM.add_default_synapse('use capitals S0', 'use capitals')
    NM.add_default_synapse('use capitals S0 not', 'use capitals')
    NM.update_synapse_fn('use capitals S0 not', synapse_delayed_not, {'sign': 1, 'delay': 0})

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
        NM.add_default_neuron(print_neuron, [1], ['#OFF#'])
        NM.add_default_synapse(print_synapse, print_neuron)

        NM.add_default_neuron(print_capital_neuron, [1,1], [print_synapse, 'use capitals S0'])
        NM.add_default_synapse(print_capital_synapse, print_capital_neuron)
        NM.update_synapse_action(print_capital_synapse, action_fn, {'s': symbol.upper()})

        NM.add_default_neuron(print_lower_neuron, [1,1], [print_synapse, 'use capitals S0 not'])
        NM.add_default_synapse(print_lower_synapse, print_lower_neuron)
        NM.update_synapse_action(print_lower_synapse, action_fn, {'s': symbol})

    return NM
