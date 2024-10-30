"""A script to convert back and forth between chunk and JSON representations of neural modules."""
# Author: Garry Morrison
# Created: 2024-10-30
# Updated: 2024-10-30

import argparse
from pathlib import Path
import synaptiflux as sf

def main():
    parser = argparse.ArgumentParser(description='Convert between chunk and JSON formats.')

    # Create mutually exclusive group for chunk and json
    format_group = parser.add_mutually_exclusive_group(required=True)
    format_group.add_argument('-c', '--chunk', action='store_true', help='Indicate chunk format')
    format_group.add_argument('-j', '--json', action='store_true', help='Indicate JSON format')

    # Create another mutually exclusive group for flat and group, but only for json
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('-f', '--flat', action='store_true', help='Indicate flat format')
    output_group.add_argument('-g', '--group', action='store_true', help='Indicate group format')

    # Capture additional parameters
    parser.add_argument('params', nargs='+', help='At least one additional parameter to process')

    # Parse the arguments
    args = parser.parse_args()

    # Use the parsed arguments
    print(f'Chunk: {args.chunk}')
    print(f'JSON: {args.json}')
    print(f'Flat: {args.flat}')
    print(f'Group: {args.group}')
    print(f'Additional parameters: {args.params}')

    # Set the destination extension:
    if args.json:
        destination_ext = '.json'
    else:
        destination_ext = '.chunk'

    # Set grouped vs flat representation:
    grouped = True
    if args.flat:
        grouped = False

    # Walk our filename parameters:
    for filename in args.params:
        source_path = Path(filename)
        source_ext = source_path.suffix
        source_stem = source_path.stem
        destination_path = source_path.with_suffix(destination_ext)

        # Print what we know:
        print(f'\nsource: {source_path}')
        print(f'destination: {destination_path}')
        print(f'convert: {source_ext} -> {destination_ext}')
        print(f'grouped: {grouped}')
        print(f'module name: {source_stem}')

        # Now load the module:
        NM = sf.NeuralModule(source_stem)
        print(f'Loading file: {source_path}')
        if source_ext == '.chunk':
            NM.load_from_chunk(source_path)
        elif source_ext == '.json':
            NM.load_from_json(source_path)
        else:
            print(f'Unrecognized extension: {source_ext}')
            sys.exit(1)

        # Now save the module:
        print(f'Saving file: {destination_path}')
        if destination_ext == '.chunk':
            NM.save_as_chunk(destination_path, grouped=grouped)
        elif destination_ext == '.json':
            NM.save_as_json(destination_path, grouped=grouped)
        else:
            print(f'Unrecognized extension: {destination_ext}')
            sys.exit(1)


if __name__ == "__main__":
    print('A script to convert between chunk and JSON representations of neural modules.\n')
    main()

