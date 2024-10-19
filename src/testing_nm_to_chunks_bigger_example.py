"""A quick test of outputing neural modules in chunk notation."""
# Author: Garry Morrison
# Created: 2024-10-20
# Updated: 2024-10-20

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing the parsing of an if-then machine in sf chunk notation, then outputing in chunk notation:")

    # define our neural module:
    NM = sf.NeuralModule("SynaptiFlux if then machine")

    # define our if-then machine to parse:
    s = """

    -- define our default functions and parameters using chunk notation:
    as default:
        layer => |3>
        trigger_fn => |trigger: simm> + |threshold: 0.98>
        pooling_fn => |pooling: or>
        synapse_fn => |synapse: identity> + |sign: 1>
        action_fn => |action: null>
    end:

    -- define our greeting machine:
    as neuron |Greeting neuron>:
        pattern => |H> . |e> . |l> . |l> . |o>
        pattern => |H> . |i>
        pattern => |H> . |e> . |y>
        pattern => |M> . |o> . |r> . |n> . |i> . |n> . |g>
    end:

    -- define a null synapse:
    as synapse |Greeting synapse S0 null>:
        axon => |Greeting neuron>
    end:

    -- define a more useful synapse:
    as synapse |Greeting synapse S1>:
        axon => |Greeting neuron>
        action_fn => |action: println> + |s: Greetings!>
    end:

    -- define another if-then machine:
    as neuron |neuron 1>:
        layer => |1>
        pooling_fn => |pooling: sum_mod2>
        trigger_fn => |trigger: simm> + |threshold: 0.75>
        pattern => 2|alpha> + 3|beta>
        pattern => 5|x> + 7|y> + 11|z>
        trigger_fn => |trigger: simm> + |threshold: 0.921>
        pattern => 13|hello> + 17|world>
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
    # print(NM)

    # convert back to chunk notation:
    print("\n---------------------------------\nConverted back to chunk notation:")
    print(NM.as_chunk())

