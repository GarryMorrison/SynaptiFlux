# Welcome to the SynaptiFlux project

The goal of this project is to explore the idea of breaking down the concept of neurons and synapses into abstract and general modular components. Currently this project is just a toy, and is effectively a very verbose system to implement basic logic gates. Perhaps the addition of more interesting components will make this system more interesting?


## Neurons
We break neurons down into the following components:

### triggers and patterns
Each neuron has one or more stored patterns, and a list of synapse labels to measure and create an input list from. For each pattern the trigger function compares the stored pattern with the newly created input pattern, then appends the result to the `pooling_list`, ready for the pooling function to process. Currently we only have one trigger function, the `dot_product_with_threshold`.

### pooling of triggered patterns
We use a specified pooling function to convert the `pooling_list` into a single value. For example, `or`, `xor`, `sum_mod_2`, and so on. Ideally, the output of this function is either 0 or 1, representing the idea that a neural axon is either firing or not firing. In contrast, the synapse value can be any float, including negative values, where negative values usually correspond to an inhibition.

### axon
The axon is a list of 0's and 1's that represents the firing history of the given neuron. At each time step the result of the pooling function is appended to this list.

## Synapses
We break synapses down into the following components:

### synpase function
A function that applies a computation to the axon history of the particular neuron it is connected to. This function has access to the entire history of the axon spike history, allowing for longer time scale properties. The output of this function can be any float value, including negative values (for inhibition). We have this property to encode the fact that a synapse, unlike an axon, is a lot more complex than just on or off.

### synapse action
If the synapse is activated, then the synapse invokes some specified action. Currently we only have 3 actions, but it is a simple matter to add more interesting actions. These are `action_null`, `action_println` and `action_print`. Respectively they do: nothing, print the given string with a newline, print the given string without a newline.

## Sources
We define sources as simple spike histories using python generators. For example, we have `#OFF#` for always off, `#ON#` for always on, `#INIT#` for initially on, then off for the rest of time, `#ALT-N#` for spiking when `time stamp mod N == 0`, and so on.

## Variables
Variables are used in our neural system to link outputs from neural modules, to neuron inputs in another neural module. For example
```
0 neuron S0 delta -> !seq-0!
```
sets the value of `!seq-0!` to the output of the 0 neuron's delta synapse. Likewise
```
!seq-0! -> print h
```
pokes the `print h` neuron with the value of the `!seq-0!` variable. Sources can also be used as inputs to neurons.


## Neural Module
A neural module is a collection of neurons and synapses wired together, to implement some modular function. Each module is roughly equivalent to a function in a regular programming language. 

For example, the sequence module increments through a sequence, and has three inputs: `initialize sequence`, `increment the sequence`, `switch off the sequence`. In the process it steps through the 0 neuron, then the 1 neuron, and so on. Once a neuron is activated it stays active until either the increment command, or the off command is sent. If you require only activation on change in state, then you can use one of the delta synapses, which only activate on state change.

The print symbol module has an input for `use capitals`, and inputs for a variety of symbols. When appropriate symbol neurons are invoked, then the system will print out the appropriate symbol, in the appropriate upper or lower case.

## Neural System
A neural system is a collection of neural modules, with their outputs and inputs wired together via `variables`. For example, the neural system `hello world` wires together a sequence module with a print symbol module to print out the string `Hello World!`. Yes, all very elementary at this stage. Indeed, the hello world example system looks particularly like an elementary assembly language, see below.

---

## Hello World example

Here is the output from our Hello World neural system:
```
SynaptiFlux$ python3 testing_neural_system_printing_hello_world.py
Let's implement 'Hello World!' in a neural system:
Hello World!
Neural System: sequence example system
--------------------------------------

Sources:
    #OFF#: 0 <generator object source_off at 0x7f75c1ab4938>
    #ON#: 1 <generator object source_on at 0x7f75c1ab48e0>
    #INIT#: 0 <generator object source_init at 0x7f75c1ab4990>
    #ALT-1#: 1 <generator object source_alt_N at 0x7f75c1ab49e8>

Variables: ['!seq-0!', '!seq-1!', '!seq-10!', '!seq-11!', '!seq-12!', '!seq-2!', '!seq-3!', '!seq-4!', '!seq-5!', '!seq-6!', '!seq-7!', '!seq-8!', '!seq-9!', '#ALT-1#', '#INIT#', '#OFF#']

Modules:
Module: sequence module
    inputs:
        #INIT# -> init flag   history: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #ALT-1# -> carry flag   history: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        #OFF# -> off flag   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    outputs:
        0 neuron S0 delta -> !seq-0!    history: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        1 neuron S0 delta -> !seq-1!    history: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        2 neuron S0 delta -> !seq-2!    history: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        3 neuron S0 delta -> !seq-3!    history: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        4 neuron S0 delta -> !seq-4!    history: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        5 neuron S0 delta -> !seq-5!    history: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        6 neuron S0 delta -> !seq-6!    history: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        7 neuron S0 delta -> !seq-7!    history: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        8 neuron S0 delta -> !seq-8!    history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        9 neuron S0 delta -> !seq-9!    history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        10 neuron S0 delta -> !seq-10!    history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        11 neuron S0 delta -> !seq-11!    history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        12 neuron S0 delta -> !seq-12!    history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

Module: print alphabet module
    inputs:
        !seq-0! -> use capitals   history: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-0! -> print h   history: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-1! -> print e   history: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-2! -> print l   history: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-3! -> print l   history: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-4! -> print o   history: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-5! -> print     history: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-6! -> use capitals   history: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-6! -> print w   history: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-7! -> print o   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-8! -> print r   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-9! -> print l   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        !seq-10! -> print d   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        !seq-11! -> print !   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        !seq-12! -> print \n   history: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

    outputs:

```
