"""A quick script to test the parsing of simple SDB."""
# Author: Garry Morrison
# Created: 2024-10-15
# Updated: 2024-10-15

import synaptiflux as sf

def display_parsed_sequence(seq):
    """Display a parsed SDB sequence."""
    print(f"Pattern:\n    coeffs: {seq[0]}\n    synapses: {seq[1]}\n")

def parse_sequence(s):
    """Parse a sequence, and then display it."""
    seq = sf.parse_seq(s, synapse_number=0)
    print(f"Pattern:\n    input: {s}\n    coeffs: {seq[0]}\n    synapses: {seq[1]}\n")

if __name__ == '__main__':
    print("Quick test of parsing simple SDB:")

    # define some kets:
    empty_ket = '  |>   '
    clean_ket = ' |alpha> '
    ket1 = '  2|apples> '
    ket2 = ' 3 |oranges>   '

    # parse them:
    parse_sequence(empty_ket)
    parse_sequence(clean_ket)
    parse_sequence(ket1)
    parse_sequence(ket2)

    # define some superpositions:
    clean_sp = '  |alpha> + |beta> + |gamma>  '
    sp = '  2|a> + 3  |b> + 5|c> +  7 |d>    '

    # parse them:
    parse_sequence(clean_sp)
    parse_sequence(sp)

    # define some sequences:
    empty_ket_seq = ' |a> . |> . |> . |> . |b> . |> . |c> '
    clean_seq = ' |H> . |e> . |l> . |l> . |o> '
    coeff_seq = ' 2|a> . 3 |b> . 5 |c> . 7|d>  '
    sp_seq = ' 2|alpha> + 3|beta> + 5|gamma> . |a> + |b> . 7|x> + 11 |y> + 13 |z>  '
    empty_ket_sp_seq = ' 2|alpha> + 3|beta> + 5|gamma> . |> . |> . |> . |a> + |b> . |> . |> . 7|x> + 11 |y> + 13 |z>  '

    # parse them:
    parse_sequence(empty_ket_seq)
    parse_sequence(clean_seq)
    parse_sequence(coeff_seq)
    parse_sequence(sp_seq)
    parse_sequence(empty_ket_sp_seq)





