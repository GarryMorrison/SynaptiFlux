"""Implement a neural module."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-10-5

from .neuron import Neuron
from .synapse import Synapse

class NeuralModule:
    """Implement a neuron and synapse module."""
    def __init__(self, name):
        self.name = name
        self.sources = {}
        self.current_sources_state = {}
        self.neurons = {}
        self.current_poked_neurons = set()
        self.synapses = {}
        self.default_trigger_fn = None
        self.default_trigger_params = {}
        self.default_pooling_fn = None
        self.default_pooling_params = {}
        self.default_synapse_fn = None
        self.default_synapse_params = {}
        self.default_action_fn = None
        self.default_action_params = {}

    def set_neuron_layer(self, name, n): # not sure how useful this method is, since we set the neuron layer on construction.
        """Set the named neuron's layer."""
        if name in self.neurons:
            self.neurons[name].set_layer(n)

    def get_neuron_layer(self, name):
        """Get the named neuron's layer."""
        if name in self.neurons:
            return self.neurons[name].get_layer()
        return -1 # maybe change this later?

    # Do we want default layers too?

    def set_default_trigger(self, fn, params):
        """Set the default trigger."""
        self.default_trigger_fn = fn
        self.default_trigger_params = params

    def set_default_pooling(self, fn, params):
        """Set the default pooling."""
        self.default_pooling_fn = fn
        self.default_pooling_params = params

    def set_default_synapse(self, fn, params):
        """Set the default synapse."""
        self.default_synapse_fn = fn
        self.default_synapse_params = params

    def set_default_action(self, fn, params):
        """Set the default action."""
        self.default_action_fn = fn
        self.default_action_params = params

    def add_source(self, name, source_fn):
        """Add a source to our system."""
        self.sources[name] = source_fn
        self.current_sources_state[name] = next(self.sources[name])

    def add_neuron(self, name, layer, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params):
        """Add a neuron to our system."""
        neuron = Neuron(name, layer, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
        self.neurons[name] = neuron

    # append_pattern(self, seed_pattern, synapse_labels, trigger_fn, trigger_params)
    def append_neuron_pattern(self, name, seed_pattern, synapse_labels, trigger_fn, trigger_params):
        """Append a pattern to an existing neuron in our system."""
        if name not in self.neurons:
            return
        self.neurons[name].append_pattern(seed_pattern, synapse_labels, trigger_fn, trigger_params)

    def add_default_neuron(self, name, layer, seed_pattern, synapse_labels):
        """Add a default neuron to our system."""
        neuron = Neuron(name, layer, seed_pattern, synapse_labels, self.default_trigger_fn, self.default_trigger_params, self.default_pooling_fn, self.default_pooling_params)
        self.neurons[name] = neuron

    def append_default_neuron_pattern(self, name, seed_pattern, synapse_labels):
        """Append a default pattern to an existing neuron in our system."""
        if name not in self.neurons:
            return
        self.neurons[name].append_pattern(seed_pattern, synapse_labels, self.default_trigger_fn, self.default_trigger_params)

    def update_neuron_pooling(self, name, pooling_fn, pooling_params):
        """Update the pooling function for a neuron."""
        if name not in self.neurons:
            return
        self.neurons[name].update_pooling(pooling_fn, pooling_params)

    def update_neuron_trigger(self, name, pattern_no, pooling_fn, pooling_params):
        """Update the trigger function for a neuron's pattern."""
        if name not in self.neurons:
            return
        self.neurons[name].update_trigger(pattern_no, pooling_fn, pooling_params)

    def add_synapse(self, name, axon_name, synapse_fn_type, params, synapse_action_type, action_params):
        """Add a synapse to our system."""
        synapse = Synapse(name, axon_name, synapse_fn_type, params, synapse_action_type, action_params)
        if axon_name in self.neurons:
           layer = self.neurons[axon_name].get_layer()
           synapse.set_layer(layer)
        self.synapses[name] = synapse

    def add_default_synapse(self, name, axon_name):
        """Add a default synapse to our system."""
        synapse = Synapse(name, axon_name, self.default_synapse_fn, self.default_synapse_params, self.default_action_fn, self.default_action_params)
        if axon_name in self.neurons:
           layer = self.neurons[axon_name].get_layer()
           synapse.set_layer(layer)
        self.synapses[name] = synapse

    def update_synapse_fn(self, name, synapse_fn, synapse_params):
        """Update the synapse function for a synapse."""
        if name not in self.synapses:
            return
        self.synapses[name].update_fn(synapse_fn, synapse_params)

    def update_synapse_action(self, name, action_fn, action_params):
        """Update the synapse action for a synapse."""
        if name not in self.synapses:
            return
        self.synapses[name].update_action(action_fn, action_params)

    def test_source(self, name, steps):
        """Test a given source."""
        gen = self.sources[name]
        for _ in range(steps):
            print(next(gen))

    def update_sources(self):
        """Update our sources."""
        for label, source in self.sources.items():
            self.current_sources_state[label] = next(self.sources[label])

    def update_neurons(self):
        """Update our neurons."""
        for label, neuron in self.neurons.items(): # update_axon(self, current_sources, synapses)
            poked = False
            if label in self.current_poked_neurons:
                poked = True
            neuron.update_axon(self.current_sources_state, self.synapses, poked)
        self.current_poked_neurons.clear()

    def update_synapses(self):
        """Update our synapses."""
        for label, synapse in self.synapses.items(): # update_spike_history(self, neurons)
            synapse.update_spike_history(self.neurons)

#     def poke_neuron(self, name): # shift below update_system?
#         """Poke a single neuron."""
#         if name not in self.neurons:
#             return
#         self.neurons[name].poke_neuron()
#         self.update_synapses() # Is this correct? Do we also need to update sources?
#
#     def poke_neurons(self, names): # shift below update_system?
#         """Poke each of the neurons in the list of neuron names."""
#         for name in names:
#             self.neurons[name].poke_neuron() # add a check that name is in self.neurons
#         self.update_synapses() # Is this correct? Do we also need to update sources?

    def poke_neuron(self, name):
        """Poke a single neuron."""
        self.current_poked_neurons.add(name)

    def poke_neurons(self, names):
        """Poke each of the neurons in the list of neuron names."""
        for name in names:
            self.current_poked_neurons.add(name)

#     def read_synapse(self, name):
#         """Read a single synapse."""
#         if name not in self.synapses:
#             return 0
#         return self.synapses[name].read_synapse()

    def read_synapse(self, name):
        """Extract delay, and then read a single synapse."""
        if name not in self.synapses:
            try:
                label, delay_str = name.rsplit(" D", 1)
                delay = int(delay_str)
            except ValueError:
                label = name
                delay = 0
            if label not in self.synapses: # do we want silent fail when referenced synapse is not defined?
                return 0
            return self.synapses[label].read_synapse(delay)
        else:
            return self.synapses[name].read_synapse(0) # Is this correct for when have explicit synapse with delay? Test it!

    def update_system(self, steps):
        """Update our system."""
        for _ in range(steps):
            self.update_neurons()
            self.update_synapses()
            self.update_sources()

    def str_default_fns(self):
        """Return default functions as a string."""
        s = "\nDefault functions and parameters:\n"
        s += f"    trigger: {self.default_trigger_fn}\n"
        s += f"    params: {self.default_trigger_params}\n"
        s += f"\n    pooling: {self.default_pooling_fn}\n"
        s += f"    params: {self.default_pooling_params}\n"
        s += f"\n    synapse: {self.default_synapse_fn}\n"
        s += f"    params: {self.default_synapse_params}\n"
        s += f"\n    action: {self.default_action_fn}\n"
        s += f"    params: {self.default_action_params}\n"
        return s

    def str_sources(self):
        """Return sources as a string."""
        s = "\nSources:\n"
        for label, source in self.sources.items():
            s += f"    {label}: {self.current_sources_state[label]} {source}\n"
        return s

    def str_neurons(self):
        """Return neurons as a string."""
        s = "\nNeurons:\n"
        s += f"    poked neurons: {self.current_poked_neurons}\n\n"
        for label, neuron in self.neurons.items():
            s += f"{neuron}\n"
        return s

    def str_synapses(self):
        """Return synapses as a string."""
        s = "Synapses:\n"
        for label, synapse in self.synapses.items():
            s += f"{synapse}\n"
        return s

    def str_neuron_layers(self):
        """Return neuron's layers."""
        layer_neuron_dict = {}
        for label, neuron in self.neurons.items():
            layer = neuron.get_layer()
            if layer not in layer_neuron_dict: # use default dict instead?
                layer_neuron_dict[layer] = set()
            layer_neuron_dict[layer].add(label)
        s = "\nNeurons:\n"
        for layer in sorted(layer_neuron_dict.keys()):
            s += f"    layer: {layer}    {sorted(layer_neuron_dict[layer])}\n"
        return s

    def str_synapse_layers(self):
        """Return synapse's layers."""
        layer_synapse_dict = {}
        for label, synapse in self.synapses.items():
            layer = synapse.get_layer()
            if layer not in layer_synapse_dict: # use default dict instead?
                layer_synapse_dict[layer] = set()
            layer_synapse_dict[layer].add(label)
        s = "\nSynapses:\n"
        for layer in sorted(layer_synapse_dict.keys()):
            s += f"    layer: {layer}    {sorted(layer_synapse_dict[layer])}\n"
        return s

    def __str__(self):
        s = f"Neural Module: {self.name}\n"
        header_len = len(s) - 1
        s += "-" * header_len + "\n"
        # s += f"Neurons: {set(self.neurons.keys())}\n"
        # s += f"Synapses: {set(self.synapses.keys())}\n"
        s += self.str_default_fns()
        s += self.str_sources()
        s += self.str_neurons()
        s += self.str_synapses()
        s += self.str_neuron_layers()
        s += self.str_synapse_layers()
        # s += f"\nNeurons: {sorted(self.neurons.keys())}\n"
        # s += f"\nSynapses: {sorted(self.synapses.keys())}\n"
        return s


