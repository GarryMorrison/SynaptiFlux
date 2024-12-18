"""Load and run map files given on the command line."""
# Author: Garry Morrison
# Created: 2024-11-6
# Updated: 2024-11-14

import sys
import ast
from pathlib import Path
import synaptiflux as sf

def main():
    """The main body of code."""
    if len(sys.argv) < 2:
        print('Please provide at least one map file to process.')
        sys.exit(1)
    for filename in sys.argv[1:]:
        filepath = Path(filename)
        stem = filepath.stem
        print(f'Loading {filename}')
        # print(f'stem: {stem}')
        NM = sf.NeuralModule(stem) # initialize our neural module
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0 or line.startswith('--'): # either empty or comment line, so continue the loop
                    continue
                # print(f'line: {line}')
                if line == 'print:': # print an empty line
                    print()
                elif line.startswith('print: '): # print a string
                    print(line[7:])
                elif line.startswith('poke: '): # poke list in SDB sequence style
                    poke_list = sf.parse_sdb_sequence_to_poke_list(line[6:])
                    # print(f'poke: {line[6:]}')
                    print(f'poke-list: {poke_list}')
                    NM.poke_neuron_sequence(poke_list)
                elif line.startswith('poke-list: '): # poke list in Python list style
                    poke_list = ast.literal_eval(line[11:])
                    print(f'poke-list: {poke_list}')
                    NM.poke_neuron_sequence(poke_list)
                elif line.startswith('poke-string: '): # poke a string, converted to a list of characters
                    poke_list = list(line[13:])
                    print(f'poke-list: {poke_list}')
                    NM.poke_neuron_sequence(poke_list)
                elif line.startswith('update: '): # update the system by the given integer number of time steps
                    try:
                        steps = int(line[8:])
                    except Exception as e:
                        print(e)
                        continue
                    print(f'update: {steps}')
                    NM.update_system(steps)
                elif line == 'print-global-sequences:': # print our NM global sequences
                    NM.print_global_sequences(layers=None) # None param for now
                elif line == 'print-neural-module:': # print out our full neural module
                    print(NM)
                elif line == 'exit:': # exit the current map file
                    print(f'Exiting {filename}')
                    break
                else:
                    NM.from_map(line, verbose=False)


if __name__ == '__main__':
    main()
