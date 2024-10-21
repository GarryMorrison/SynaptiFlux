"""Testing the loading and saving of our chunk machines."""
# Author: Garry Morrison
# Created: 2024-10-22
# Updated: 2024-10-22

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing the loading and saving of our chunk machines:\n")

    NM0 = sf.NeuralModule('module 0')
    source_filename0 = 'machines/greetings.chunk'
    dest_filename0 = 'machines/tmp_0.chunk'
    print(f"loading file: {source_filename0}")
    NM0.load_chunks(source_filename0)
    print(f"saving file: {dest_filename0}")
    NM0.save_chunks(dest_filename0)

    print()
    NM1 = sf.NeuralModule('module 1')
    source_filename1 = 'machines/Fred.chunk'
    dest_filename1 = 'machines/tmp_1.chunk'
    print(f"loading file: {source_filename1}")
    NM1.load_chunks(source_filename1)
    print(f"saving file: {dest_filename1}")
    NM1.save_chunks(dest_filename1)

