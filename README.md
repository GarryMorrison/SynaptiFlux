# Welcome to the SynaptiFlux project
The goal of this project is to explore the idea of breaking down the concept of neurons and synapses into abstract and general modular components. Currently this project is just a toy, and is effectively a very verbose system to implement basic logic gates. Perhaps the addition of more interesting components will make this system more useful?

This project has 4 main components, `neurons`, `synapses`, `neural modules` and `neural systems`, and a collection of smaller components. We will briefly introduce these main components, and then we will go into more detail, using examples, a little further down this document.

## Neurons
Neurons process incoming patterns, constructed from the output of synapses, or simple sources, and stores the binary result in a corresponding axon (or more accurately appends to the end of the axon list).

## Synapses
Synapses read a corresponding axon spike history and calculates a corresponding output. Further if a condition is satisfied the synapse can optionally invoke an action, such as printing a specified string.

## Neural modules
Neural modules are a collection of neurons and synapses wired together to perform some desired function. For example counting a sequence, or printing symbols. Eventually we would like to implement more interesting modules.

## Neural systems
Neural systems are a collection of neural modules, wired together using so called variables. The value of synapses, or optionally sources, are read from a module and stored in, for now global, variables. The value of variables are then "poked" into specified neurons. The modules are then updated one time step, and then the above steps are repeated.

### What is a neuron poke?
We use so called `neuron pokes` to set a neuron's output to 1, for one time step, independent of that neurons inputs at that time step. We do not currently support poking 0's, which would set the neuron's output to 0 independent of the neuron's inputs. We may implement this feature later if deemed interesting or useful.

## Naming conventions
* **sources** start and end with # char, all characters are upper case, separated by dashes. Eg, #ALT-4#
* **variable names** start and end with ! char, character case is arbitrary, separated by dashes. Eg, !seq-2!
* **neuron labels** are arbitrary strings
* **synapse labels** are neuron labels followed by Sn (where n is the synapse number), followed by an optional modifier such as `not` or `delta`. Eg, `3 neuron S0` or `3 neuron S0 delta`

---
# Examples
We now provide some examples and go into a little more depth about the relevant components.

## Neurons
Here is the output from two sample neurons:
```
$ python3 testing_neuron.py
Let's implement a couple of sample neurons:
Neuron: first neuron
    pooling: <function pooling_or at 0x7f64552f86a8>
    params: {}
    patterns: 3
        0    trigger: <function trigger_dot_product_threshold at 0x7f64552f8620>
        0    params: {'threshold': 1}
        0    [0, 1, 2, 3]
        0    ['alpha S0', 'beta S0', 'gamma S0', 'delta S0']

        1    trigger: <function trigger_dot_product_threshold at 0x7f64552f8620>
        1    params: {'threshold': 1}
        1    [7, 7, 7]
        1    ['X S0', 'Y S0', 'Z S0']

        2    trigger: <function trigger_dot_product_threshold at 0x7f64552f8620>
        2    params: {'threshold': 1}
        2    [3, 5, 2]
        2    ['u S0', 'v S0', 'w S0']

    axon: [0, 1]

Neuron: second neuron
    pooling: <function pooling_or at 0x7f64552f86a8>
    params: {}
    patterns: 1
        0    trigger: <function trigger_dot_product_threshold at 0x7f64552f8620>
        0    params: {'threshold': 1}
        0    [1, 1, 1, 1, 1]
        0    ['a S0', 'b S0', 'c S0', 'd S0', 'e S0']

    axon: [1, 1, 0, 1, 0]
```
Each neuron has a string label, here `first neuron` and `second neuron`, a pooling function, an axon history, and a collection of patterns, each of which has a trigger function, a stored pattern, and a list of synapse labels used to build the neurons input.

* **synapse list** is a list of synapse labels used to construct the `neural input pattern`.
* **neural input pattern** is a list of float values, measured from the corresponding synapses, specified in the `synapse list`.
* **stored pattern** is a list of float values with the same length as the `synapse list`.
* **trigger function** applies a specified function to the `neural input pattern` and the `stored pattern`, and computes a float output. Currently we only have the `dot_product` function.
* **pooling list** is a list of float values, with length equal to the number of patterns. These values are the outputs from the `trigger functions`.
* **pooling function** maps the `pooling list` to a single binary value. For example, `or`, `xor` or `sum_mod_2`. The purpose of the pooling feature is so that more than one incoming pattern can influence the firing of a given neuron.
* **axon** at each time step the result of the `pooling function` is appended to the axon history


## Synapses
Here is the output from three sample synapses:
```
$ python3 testing_synapse.py
Let's implement a couple of sample synapses:
Synapse: alpha S0
    source axon: alpha
    type: <function synapse_identity at 0x7f960f5b0e18>
    params: {'sign': 1}
    action: <function action_null at 0x7f960f5b8400>
    action params: {}
    spike history: [0, 5, 8, 3, 0, 1]

Synapse: beta S0
    source axon: beta
    type: <function synapse_delayed_identity at 0x7f960f5b0ea0>
    params: {'sign': 1, 'delay': 3}
    action: <function action_println at 0x7f960f5b8488>
    action params: {'s': 'beta activated!'}
    spike history: [0, 0, 0]

Synapse: gamma S0
    source axon: gamma
    type: <function synapse_delayed_identity at 0x7f960f5b0ea0>
    params: {'sign': -1, 'delay': 2}
    action: <function action_null at 0x7f960f5b8400>
    action params: {}
    spike history: [0, 0, 0]
```
The components are
* **synapse name** is some string label for the given synapse, using the synapse naming convention given above.
* **source axon** is the source axon for this synapse.
* **synapse function** applies a specified function to the axon list, and returns a float. Negative values for inhibition.
* **action function** if a condition is met, optionally invoke an action. Currently we only have print and println.
* **spike history** is the spike history of the given synapse. Note that neurons only read the last value in this list, and do not have full access to this list. The full list is given for human consumption.

## Neural modules
Here is a module that computes prime vs not prime for integers less than 25:
```
$ python3 testing_prime_spike_history_using_sources.py
Testing prime spike history using sources:
not prime
not prime
prime
prime
not prime
prime
not prime
prime
not prime
not prime
not prime
prime
not prime
prime
not prime
not prime
not prime
prime
not prime
prime
not prime
not prime
not prime
prime
not prime
Neural Module: Prime numbers less than 25
-----------------------------------------

Default functions and parameters:
    trigger: None
    params: {}

    pooling: None
    params: {}

    synapse: None
    params: {}

    action: None
    params: {}

Sources:
    #INIT#: 0 <generator object source_init at 0x7fd8e3bf27d8>
    #INIT-1#: 0 <generator object source_init_N at 0x7fd8e3bf2830>
    #INIT-2#: 0 <generator object source_init_N at 0x7fd8e3bf2888>
    #INIT-3#: 0 <generator object source_init_N at 0x7fd8e3bf28e0>
    #INIT-5#: 0 <generator object source_init_N at 0x7fd8e3bf2938>
    #ALT-2#: 0 <generator object source_alt_N at 0x7fd8e3bf2990>
    #ALT-3#: 0 <generator object source_alt_N at 0x7fd8e3bf29e8>
    #ALT-5#: 1 <generator object source_alt_N at 0x7fd8e3bf2a40>

Neurons:
    poked neurons: set()

Neuron: not prime
    pooling: <function pooling_or at 0x7fd8e3bf86a8>
    params: {}
    patterns: 1
        0    trigger: <function trigger_dot_product_threshold at 0x7fd8e3bf8620>
        0    params: {'threshold': 1}
        0    [-10, -10, -10, 1, 1, 1, 1]
        0    ['#INIT-2#', '#INIT-3#', '#INIT-5#', '#INIT-1#', '#ALT-2#', '#ALT-3#', '#ALT-5#']

    axon: [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]

Synapses:
Synapse: not prime S0
    source axon: not prime
    type: <function synapse_delayed_identity at 0x7fd8e3befea0>
    params: {'sign': 1, 'delay': 0}
    action: <function action_println at 0x7fd8e3bf8488>
    action params: {'s': 'not prime'}
    spike history: [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]

Synapse: not prime S0 not
    source axon: not prime
    type: <function synapse_delayed_not at 0x7fd8e3beff28>
    params: {'sign': 1, 'delay': 0}
    action: <function action_println at 0x7fd8e3bf8488>
    action params: {'s': 'prime'}
    spike history: [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0]


Neurons: ['not prime']

Synapses: ['not prime S0', 'not prime S0 not']
```
* **default functions** are a set of default functions used to simplify the code required to add neurons and synapses to the module. 
* **sources** a list of defined sources for this module
* **poked neurons** a set of neurons that will be poked in the current time step
* **neurons** the set of neurons defined in this module
* **synpases** the set of synapses defined in this module

## Neural systems
Finally, we provide a full `neural system`:
```
$ python3 testing_neural_system_printing_hello_world.py
Let's implement 'Hello World!' in a neural system:
Hello World!
Neural System: sequence example system
--------------------------------------

Sources:
    #OFF#: 0 <generator object source_off at 0x7f38d6bf3a40>
    #ON#: 1 <generator object source_on at 0x7f38d6bf39e8>
    #INIT#: 0 <generator object source_init at 0x7f38d6bf3a98>
    #ALT-1#: 1 <generator object source_alt_N at 0x7f38d6bf3af0>

Variables: ['!seq-0!', '!seq-1!', '!seq-10!', '!seq-11!', '!seq-12!', '!seq-2!', '!seq-3!', '!seq-4!', '!seq-5!', '!seq-6!', '!seq-7!', '!seq-8!', '!seq-9!', '#ALT-1#', '#INIT#', '#OFF#']

Modules:
Module: sequence module
    inputs:
        #INIT# -> "init flag"   history: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #ALT-1# -> "carry flag"   history: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        #OFF# -> "off flag"   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    outputs:
        "0 neuron S0 delta" -> !seq-0!    history: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        "1 neuron S0 delta" -> !seq-1!    history: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        "2 neuron S0 delta" -> !seq-2!    history: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        "3 neuron S0 delta" -> !seq-3!    history: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        "4 neuron S0 delta" -> !seq-4!    history: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        "5 neuron S0 delta" -> !seq-5!    history: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        "6 neuron S0 delta" -> !seq-6!    history: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        "7 neuron S0 delta" -> !seq-7!    history: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        "8 neuron S0 delta" -> !seq-8!    history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        "9 neuron S0 delta" -> !seq-9!    history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        "10 neuron S0 delta" -> !seq-10!    history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        "11 neuron S0 delta" -> !seq-11!    history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        "12 neuron S0 delta" -> !seq-12!    history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

Module: print alphabet module
    inputs:
        !seq-0! -> "use capitals"   history: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-0! -> "print h"   history: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-1! -> "print e"   history: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-2! -> "print l"   history: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-3! -> "print l"   history: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-4! -> "print o"   history: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-5! -> "print  "   history: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-6! -> "use capitals"   history: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-6! -> "print w"   history: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-7! -> "print o"   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-8! -> "print r"   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-9! -> "print l"   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-10! -> "print d"   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        !seq-11! -> "print !"   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        !seq-12! -> "print \n"   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

    outputs:
```
* **sources** a list of sources for this system
* **variables** a list of the variables used by this system
* **modules** the set of modules in this system
  * **inputs** are a mapping from sources, or variables, to the inputs of neurons. The history is given for human consumption, and is not used by the back end code at all.
  * **outputs** are a mapping from synapses to variables
  


---
## Project Layout:
```
.
├── LICENSE
├── README.md
└── src
    ├── synaptiflux
    │   ├── __init__.py
    │   ├── action_fn.py
    │   ├── modules
    │   │   ├── __init__.py
    │   │   ├── module_print_symbols.py
    │   │   └── module_sequence.py
    │   ├── neural_module.py
    │   ├── neural_system.py
    │   ├── neuron.py
    │   ├── pooling_fn.py
    │   ├── source_fn.py
    │   ├── synapse.py
    │   ├── synapse_fn.py
    │   └── trigger_fn.py
    ├── testing_Jacob_neural_module.py
    ├── testing_counting_digits.py
    ├── testing_counting_digits_using_defaults.py
    ├── testing_default_options.py
    ├── testing_empty_synapse_bug.py
    ├── testing_neural_system.py
    ├── testing_neural_system_printing.py
    ├── testing_neural_system_printing_hello_world.py
    ├── testing_neuron.py
    ├── testing_prime_spike_history.py
    ├── testing_prime_spike_history_using_sources.py
    ├── testing_print_alphabet.py
    ├── testing_sf_print_symbols_module.py
    ├── testing_sf_sequence_module.py
    └── testing_synapse.py
```

