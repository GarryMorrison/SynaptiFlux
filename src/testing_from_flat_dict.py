"""Testing the loading of flat JSON into NeuralModules."""
# Author: Garry Morrison
# Created: 2024-10-25
# Updated: 2024-10-30

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing the loading of flat JSON files into NeuralModules:")

    NM0 = sf.NeuralModule('JSON module')
    filename = 'machines/greetings.json'
    NM0.load_from_json(filename)
    # see what we have:
    # print(NM0)
    print(NM0.as_flat_json())
    output_dict = NM0.as_flat_dict()

    NM1 = sf.NeuralModule('as flat dict module')
    NM1.from_dict(output_dict)
    # see what we have:
    print(NM1)
