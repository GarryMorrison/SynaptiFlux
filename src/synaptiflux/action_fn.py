"""Define some toy actions."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-10-10

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
        # layers = '*'
        layers = 1 # hardwire in for now
        delay = NM.get_delay_counter()
        # delay = NM.get_delay_counter() - 1 # for testing purposes
        layer_synapse_dict = NM.get_active_synapses(layers, list(range(delay)))
        s = "To store:\n"
        s += f"    delay: {delay}\n"
        for layer in sorted(layer_synapse_dict.keys()):
            s += f"    layer: {layer}    {sorted(layer_synapse_dict[layer])}\n"
        s += f"    buffer: {str(buffer)}\n"
        print(s)
        NM.reset_delay_counter()
        buffer.erase()
