"""A quick test of parsing if-then machines, using our new parse code."""
# Author: Garry Morrison
# Created: 2024-10-15
# Updated: 2024-10-16

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing the parsing of an if-then machine:")

    # define our neural module:
    NM = sf.NeuralModule("if then machine")

    # define our if-then machine to parse:
    s = """

    -- define our default functions and parameters:
    layer |*> => |1>
    trigger_fn |*> => |trigger: simm> + |threshold: 0.98>
    pooling_fn |*> => |pooling: or>
    synapse_fn |*> => |synapse: delayed_identity> + |sign: 1> + |delay: 2>
    action_fn |*> => |action: println> + |s: some unspecified string>


    -- define our if-then machine:
    pattern |neuron 1> => 2|alpha> + 3|beta> + 5|gamma>
    pattern |neuron 1> => 5|x> + 7|y>
    then-0 |neuron 1> => |action: println> + |s: detected neuron 1>


    """

    # print out our machine:
    print(f"Our if-then machine: {s}")

    # parse the machine:
    NM = sf.parse_if_then_machine(NM, s, verbose=True)

    # see what we have:
    print(NM)

    # test our parse sp to dict function:
    # print(sf.parse_sp_to_dict('|trigger: simm> + |threshold: 0.98>'))
    # print(sf.parse_sp_to_dict('|synapse: delayed_identity> + |sign: 1> + |delay: 2>'))
    # print(sf.parse_sp_to_dict('|action: println> + |s: some unspecified string>'))


