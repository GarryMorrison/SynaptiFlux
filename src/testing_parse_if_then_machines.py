"""A quick test of parsing if-then machines, using our new parse code."""
# Author: Garry Morrison
# Created: 2024-10-15
# Updated: 2024-10-15

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing the parsing of an if-then machine:")

    # define our neural module:
    NM = sf.NeuralModule("if then machine")

    # define our if-then machine to parse:
    s = """

    -- our greetings if-then machine:
    pattern |node: 1: 1> => |H> . |e> . |l> . |l> . |o>
    pattern |node: 1: 2> => |H> . |e> . |y>
    pattern |node: 1: 3> => |H> . |i>
    pattern |node: 1: 4> => |G> . |'> . |d> . |a> . |y>
    pattern |node: 1: 5> => |M> . |o> . |r> . |n> . |i> . |n> . |g>
    then |node: 1: *> => |Greetings!>

    """

    # print out our machine:
    print(f"Our if-then machine: {s}")

    # parse the machine:
    NM = sf.parse_if_then_machine(NM, s, verbose=True)

    # see what we have:
    print(NM)
