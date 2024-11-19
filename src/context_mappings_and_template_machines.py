"""Testing my context mapping and template machines idea, with respect to SynaptiFlux."""
# Author: Garry Morrison
# Created: 2024-11-19
# Updated: 2024-11-19

import itertools
import synaptiflux as sf

def generate_ngrams(s, n):
    """Split the text 's' on space char, and generate ngrams of length n."""
    words = s.split()
    for i in range(len(words) - n + 1):
        yield words[i:i + n]

def sequence_to_gaps(seq):
    """Map a given sequence to a sequence with gaps."""
    replace_elt = None
    result_set = set()
    index_set = set()
    # for num_empty in range(len(seq) + 1):
    for num_empty in range(1, len(seq)):
        for indices in itertools.combinations(range(len(seq)), num_empty):
            seq1 = seq[:]
            for idx in indices:
                seq1[idx] = replace_elt
            index_tup = tuple(x for x in seq1 if x != replace_elt)
            tup = tuple(seq1)
            result_set.add(tup)
            index_set.add(index_tup)
    return result_set, index_set



def main():
    """Our main testing function."""
    print("Testing my context mapping and template machines ideas ...")
    # ngram size:
    ngram_size = 3
    # test string:
    s = "a b c d e f"
    # initialize the generator:
    ngram_generator = generate_ngrams(s, ngram_size)
    # see what we have:
    print('ngrams:')
    for ngram in ngram_generator:
        print(ngram)

    # test sequence:
    seq = [0,1,2,3,4]
    # build gap sequences:
    result_set, index_set = sequence_to_gaps(seq)
    print('\ngap sequences, result_set:')
    # see what we have:
    for r in result_set:
        print(r)
    print('\ngap sequences, index_set:')
    # see what we have:
    for r in index_set:
        print(r)


if __name__ == '__main__':
    main()
