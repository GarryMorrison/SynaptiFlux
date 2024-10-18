"""A quick test of outputing neural modules in chunk notation."""
# Author: Garry Morrison
# Created: 2024-10-19
# Updated: 2024-10-19

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing the parsing of an if-then machine in sf chunk notation, then outputing in chunk notation:")

    # define our neural module:
    NM = sf.NeuralModule("SynaptiFlux if then machine")

    # define our if-then machine to parse:
    s = """

    -- define our default functions and parameters using chunk notation:
    as default:
        layer => |1>
        trigger_fn => |trigger: simm> + |threshold: 0.98>
        pooling_fn => |pooling: or>
        synapse_fn => |synapse: delayed_identity> + |sign: 1> + |delay: 2>
        action_fn => |action: println> + |s: some unspecified string>
    end:


    -- define our if-then machine:
    as neuron |neuron 1>:
        layer => |3>
        pooling_fn => |pooling: sum_mod2>
        trigger_fn => |trigger: simm> + |threshold: 0.75>
        pattern => 2|alpha> + 3|beta>
        trigger_fn => |trigger: simm> + |threshold: 0.5>
        pattern => 5|x> + 7|y> + 11|z>
    end:

    -- define a synapse:
    as synapse |neuron 1 S0 not>:
        axon => |neuron 1>
        synapse_fn => |synapse: delayed_not> + |sign: 1> + |delay: 0>
        action_fn => |action: println> + |s: synapse activated by not of neuron 1>
    end:

    """

    # print out our machine:
    print(f"Our if-then machine: {s}")

    # parse the machine:
    sf.parse_sf_if_then_machine(NM, s, verbose=False)

    # see what we have:
    print(NM)

    # convert back to chunk notation:
    print("\n---------------------------------\nConverted back to chunk notation:")
    print(NM.as_chunk())

