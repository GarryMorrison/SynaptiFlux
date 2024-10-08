"""A quick test of the FnBuffer class."""
# Author: Garry Morrison
# Created: 2024-10-8
# Updated: 2024-10-8


import synaptiflux as sf

if __name__ == '__main__':
    print("Testing FnBuffer class:")

    # initialize the function buffer:
    fn_buffer = sf.FnBuffer()

    # dummy parameters:
    synapse = {}
    value = 1

    # populate the buffer:
    fn_buffer.append(sf.action_print, {'synapse': synapse, 'value': value, 's': 'Hello'})
    fn_buffer.append(sf.action_print, {'synapse': synapse, 'value': value, 's': ' '})
    fn_buffer.append(sf.action_println, {'synapse': synapse, 'value': value, 's': 'World!'})

    # see what we have:
    print(fn_buffer)

    # invoke it:
    fn_buffer.invoke()

    # erase it:
    fn_buffer.erase()

    # check that it is empty:
    print(fn_buffer)
