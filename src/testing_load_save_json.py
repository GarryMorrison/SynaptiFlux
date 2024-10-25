"""Testing the loading and saving of JSON files into NeuralModules."""
# Author: Garry Morrison
# Created: 2024-10-25
# Updated: 2024-10-25

import synaptiflux as sf

if __name__ == '__main__':
    print("Testing the loading and saving of JSON files into NeuralModules:")

    NM = sf.NeuralModule('JSON module')
    filename = 'machines/greetings.json'
    NM.load_from_json(filename)
    # see what we have:
    print(NM)

