"""Testing outputing neural modules as dictionaries."""
# Author: Garry Morrison
# Created: 2024-10-24
# Updated: 2024-10-30

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing the conversion of neural modules into dictionaries:\n")

    NM0 = sf.NeuralModule('module 0')
    source_filename0 = 'machines/greetings.chunk'
    # dest_filename0 = 'machines/tmp_0.chunk'
    print(f"loading file: {source_filename0}")
    NM0.load_from_chunk(source_filename0)
    # print(f"saving file: {dest_filename0}")
    # NM0.save_as_chunk(dest_filename0)
    print(NM0)
    print('module.defaults_as_dict():')
    print(NM0.defaults_as_dict())
    print('\n-------------------\nmodule.as_flat_json():')
    print(NM0.as_flat_json())
    print('\n-------------------\nmodule.as_grouped_json():')
    print(NM0.as_grouped_json())

    # save to file:
    dest_filename0 = 'machines/greetings.json'
    print(f"saving file: {dest_filename0}")
    NM0.save_as_json(dest_filename0, grouped=True)

    # print()
    # NM1 = sf.NeuralModule('module 1')
    # source_filename1 = 'machines/Fred.chunk'
    # dest_filename1 = 'machines/tmp_1.chunk'
    # print(f"loading file: {source_filename1}")
    # NM1.load_from_chunk(source_filename1)
    # print(f"saving file: {dest_filename1}")
    # NM1.save_as_chunk(dest_filename1)

