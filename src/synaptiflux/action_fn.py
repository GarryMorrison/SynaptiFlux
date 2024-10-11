"""Define some toy actions."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-10-11

from .trigger_fn import trigger_dot_product_threshold
from .pooling_fn import pooling_or
from .synapse_fn import *

def action_null(synapse, value):
    """Do nothing action."""
    return

def action_println(synapse, value, s):
    """Print string action, with new line, if value > 0."""
    if value > 0:
        print(s)

def action_print(synapse, value, s):
    """Print string action, without new line, if value > 0."""
    if value > 0:
        print(s, end='')

def action_print_buffer(synapse, value, buffer):
    """Print the buffer, but leave it unchanged, if value > 0."""
    if value > 0:
        print(buffer)

def action_print_to_buffer(synapse, value, buffer, s):
    """Append the given string to the given buffer, if value > 0."""
    if value > 0:
        buffer.append(s)

def action_print_to_buffers(synapse, value, buffer1, buffer2, s):
    """Append the given string to the given buffers, if value > 0."""
    if value > 0:
        buffer1.append(s)
        buffer2.append(s)

def action_print_to_buffer_flush(synapse, value, buffer, s):
    """Append the given string to the given buffer, then print the buffer, if value > 0."""
    if value > 0:
        buffer.append(s)
        print(buffer)
        buffer.erase()

def action_init_store_buffer(synapse, value, NM, buffer):
    """Initialize the store buffer."""
    if value > 0:
        NM.reset_delay_counter()
        buffer.erase()

def action_store_buffer(synapse, value, NM, buffer):
    """Store the current active synapses as input to a neuron, with output str(buffer)."""
    if value > 0:
        name = NM.get_neuron_name()
        synapse_name = f"{name} S0"
        layers = '*'
        # layers = 1 # hardwire in for now
        delay = NM.get_delay_counter()
        # delay = NM.get_delay_counter() - 1 # for testing purposes
        layer_synapse_dict = NM.get_active_synapses(layers, list(range(delay)))
        layer = sorted(layer_synapse_dict.keys())[-1] # errors out if layers_synapse_dict is empty!
        pattern = sorted(layer_synapse_dict[layer])
        neurons = NM.get_test_neurons(pattern)
        s = "To store:\n"
        s += f"    name: {name}\n"
        s += f"    delay: {delay}\n"
        # for layer in sorted(layer_synapse_dict.keys()):
        #     s += f"    layer: {layer}    {sorted(layer_synapse_dict[layer])}\n"
        s += f"    layer: {layer}    {pattern}\n"
        s += f"    neurons: {neurons}\n"
        s += f"    buffer: {str(buffer)}"
        print(s)
        if len(neurons) > 0:
            print("That pattern already triggers a neuron.")
            return
        print("Will store a neuron and synapse!\n")
        pattern_len = len(pattern)
        compare_pattern = [1] * pattern_len
        threshold = pattern_len
        NM.add_neuron(name, layer + 1, compare_pattern, pattern, trigger_dot_product_threshold, {'threshold': threshold}, pooling_or, {})
        NM.print_neuron(name)
        prefix = "stored sequence: "
        # NM.add_synapse(synapse_name, name, synapse_delayed_identity, {'sign': 1, 'delay': 0}, action_println, {'s': prefix + str(buffer)}) # bugs out due to change in synapse dictionary size!
        # NM.print_synapse(synapse_name)
        NM.reset_delay_counter()
        buffer.erase()


# add_neuron(self, name, layer, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
# add_synapse(self, name, axon_name, synapse_fn_type, params, synapse_action_type, action_params)
