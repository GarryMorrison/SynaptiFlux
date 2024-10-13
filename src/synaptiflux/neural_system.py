"""Implement a neural system, which is a collection of neural modules."""
# Author: Garry Morrison
# Created: 2024-9-19
# Updated: 2024-10-8

from .neural_module import NeuralModule, display_layer_synapse_dict

class NeuralSystem:
    """Implement a collection of neural modules."""
    def __init__(self, name):
        self.name = name
        self.sources = {}
        self.current_sources_state = {}
        # self.current_inputs_state = {}
        self.current_outputs_state = {}
        self.variables = set()            # testing. They seem to work
        self.variables_history = {}       # testing
        self.variables_current_state = {} # testing
        self.modules = {}
        self.module_inputs = {}           # comment out?
        self.module_outputs = {}
        self.module_inputs_history = {}   # comment out?
        self.module_outputs_history = {}
        self.show_active_synapses = False
        self.active_synapses_layers = '*'
        # self.active_synapses_layers = 1
        self.active_synapses_delays = 0
        # self.active_synapses_delays = [0,1,2,3,4]
        self.active_synapses_prefix = "        "
        self.active_synapses_strings = {}

    def enable_active_synapses(self, value):
        """Enable or disable active synapses in the neural module display."""
        self.show_active_synapses = value

    def set_active_synapses_layers(self, layers):
        """Set the active synapses layers parameter."""
        self.active_synapses_layers = layers

    def set_active_synapses_delays(self, delays):
        """Set the active synapses delays parameter."""
        self.active_synapses_delays = delays

    def set_active_synapses_prefix(self, prefix):
        """Set the active synapses print prefix."""
        self.active_synapses_prefix = prefix

    def get_active_synapses_layers(self, layers):
        """Get the active synapses layers parameter."""
        return self.active_synapses_layers

    def get_active_synapses_delays(self, delays):
        """Get the active synapses delays parameter."""
        return self.active_synapses_delays

    def get_active_synapses_prefix(self, prefix):
        """Get the active synapses print prefix."""
        return self.active_synapses_prefix

    def add_source(self, name, source_fn):
        """Add a source to our system."""
        self.sources[name] = source_fn
        self.current_sources_state[name] = next(self.sources[name])

#     def update_sources(self):
#         """Update our sources."""
#         for label, source in self.sources.items():
#             self.current_sources_state[label] = next(self.sources[label])

    def register_module(self, name, module):
        """Register a new module in our system."""
        self.modules[name] = module
        self.module_inputs[name] = []
        self.module_outputs[name] = []
        self.module_inputs_history[name] = {}
        self.module_outputs_history[name] = {}
        # if self.show_active_synapses:
        #     self.active_synapses_strings[name] = ""
        self.active_synapses_strings[name] = ""

    def register_module_input(self, name, input, neuron):
        """Register a new input for a given module in our system."""
        if name not in self.modules:
            return # raise exception?
        self.module_inputs[name].append([input, neuron])
        if input not in self.module_inputs_history[name]:
            self.module_inputs_history[name][input] = []
        if input not in self.variables:
            self.variables.add(input)
            self.variables_history[input] = []
            self.variables_current_state[input] = 0

    def register_module_inputs(self, name, list_input_neuron_pairs):
        """Register a list of new inputs for a given module in our system."""
        if name not in self.modules:
            return # raise exception?
        for pair in list_input_neuron_pairs:
            self.module_inputs[name].append(pair)
            if pair[1] not in self.module_inputs_history[name]: # swap pair[1] with pair[0]?
                self.module_inputs_history[name][pair[1]] = []
            if pair[0] not in self.variables:
                self.variables.add(pair[0])
                self.variables_history[pair[0]] = []
                self.variables_current_state[pair[0]] = 0

    def register_module_output(self, name, synapse, output):
        """Register a new output for a given module in our system."""
        if name not in self.modules:
            return # raise exception?
        self.module_outputs[name].append([synapse, output])
        if output not in self.module_outputs_history[name]:
            self.current_outputs_state[output] = 0 # self.current_inputs_state, or self.current_outputs_state?
            self.module_outputs_history[name][output] = []
        if output not in self.variables:
            self.variables.add(output)
            self.variables_history[output] = []
            self.variables_current_state[output] = 0

    def register_module_outputs(self, name, list_synapse_output_pairs):
        """Register a list of new outputs for a given module in our system."""
        if name not in self.modules:
            return # raise exception?
        for pair in list_synapse_output_pairs:
            self.module_outputs[name].append(pair)
            if pair[1] not in self.module_inputs_history[name]:
                self.current_outputs_state[pair[1]] = 0
                self.module_outputs_history[name][pair[1]] = []
            if pair[1] not in self.variables:
                self.variables.add(pair[1])
                self.variables_history[pair[1]] = []
                self.variables_current_state[pair[1]] = 0

    def update_inputs(self):
        """Update our inputs."""
        for name, module in self.modules.items():
            for input, neuron in self.module_inputs[name]:
                value = 0
                if input in self.sources:
                    value = self.current_sources_state[input]
                elif input in self.current_outputs_state:
                    value = self.current_outputs_state[input]
                # self.module_inputs_history[name][neuron].append(value) # comment out later!
                self.variables_current_state[input] = value
                if value > 0:
                    module.poke_neuron(neuron)
        for input in self.variables:
            self.variables_history[input].append(self.variables_current_state[input])

    def update_modules(self):
        """Update our modules."""
        for name, module in self.modules.items():
            module.update_system(1)

    def update_outputs(self):
        """Update our outputs."""
        for name, module in self.modules.items():
            for synapse, output in self.module_outputs[name]:
                 value = module.read_synapse(synapse)
                 self.current_outputs_state[output] = value
                 self.module_outputs_history[name][output].append(value)

    def update_sources(self):
        """Update our sources."""
        for label, source in self.sources.items():
            self.current_sources_state[label] = next(self.sources[label])

    def update_active_synapses(self):
        """Update our active synapses string."""
        if not self.show_active_synapses:
            return
        layers = self.active_synapses_layers
        delays = self.active_synapses_delays
        prefix = self.active_synapses_prefix
        for name, module in self.modules.items():
            layer_synapse_dict = module.get_active_synapses(layers, delays)
            s = display_layer_synapse_dict(layer_synapse_dict, prefix)
            self.active_synapses_strings[name] += s + "\n"

    def update_system(self, steps):
        """Update the system for steps."""
        for _ in range(steps):
            self.update_inputs()
            self.update_modules()
            self.update_outputs()
            self.update_sources()
            self.update_active_synapses()

    def str_sources(self):
        """Return sources as a string."""
        s = "\nSources:\n"
        for label, source in self.sources.items():
            s += f"    {label}: {self.current_sources_state[label]} {source}\n"
        return s

    def __str__(self):
        s = f"Neural System: {self.name}\n"
        header_len = len(s) - 1
        s += "-" * header_len + "\n"
        s += self.str_sources()
        # s += f"\nVariables: {sorted(self.variables)}\n"
        s += f"\nChannels: {sorted(self.variables)}\n"
        s += "\nModules:\n"
        # for name, module in self.modules.items():
        for name in self.modules.keys():
             s += f"Module: {name}\n"
             s += f"    delay counter: {self.modules[name].get_delay_counter()}\n\n"
             s += f"    inputs:\n"
             for input, neuron in self.module_inputs[name]:
                 # s += f"        {input} -> {neuron}   history: {self.module_inputs_history[name][neuron]}\n"
                 s += f"        {input} -> \"{neuron}\"   history: {self.variables_history[input]}\n"
             s += f"\n    outputs:\n"
             for synapse, output in self.module_outputs[name]:
                 s += f"        \"{synapse}\" -> {output}    history: {self.module_outputs_history[name][output]}\n"
             s += "\n"
             if self.show_active_synapses:
                 s += f"    active synapses:\n"
                 s += f"{self.active_synapses_strings[name]}\n"
        return s
