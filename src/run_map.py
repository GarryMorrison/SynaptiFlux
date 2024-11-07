"""Load and run map files given on the command line."""
# Author: Garry Morrison
# Created: 2024-11-6
# Updated: 2024-11-7

import sys
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
        NM = sf.NeuralModule(stem)
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if len(line) == 0 or line.startswith('--'):
                    continue
                # print(f'line: {line}')
                if line == 'print:':
                    print()
                elif line.startswith('print: '):
                    print(line[7:])
                elif line.startswith('poke: '):
                    poke_list = sf.parse_sdb_sequence_to_poke_list(line[6:])
                    # print(f'poke: {line[6:]}')
                    print(f'poke_list: {poke_list}')
                    NM.poke_neuron_sequence(poke_list)
                elif line.startswith('update: '):
                    try:
                        steps = int(line[8:])
                    except Exception as e:
                        print(e)
                        continue
                    print(f'update: {steps}')
                    NM.update_system(steps)
                elif line == 'exit:':
                    print(f'Exiting {filename}')
                    break
                else:
                    NM.from_map(line, verbose=False)


if __name__ == '__main__':
    main()
