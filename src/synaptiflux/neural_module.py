"""Implement a neural module."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-10-24

import json
from collections import defaultdict
from .neuron import Neuron
from .synapse import Synapse
from .parse_simple_sdb import sp_dict_to_sp, parse_sf_if_then_machine
from .trigger_fn import trigger_inverse_fn_map
from .pooling_fn import pooling_inverse_fn_map
from .synapse_fn import synapse_inverse_fn_map
from .action_fn import action_inverse_fn_map

def process_layers(synapses, layers):
    """Given a synapses dict, and layers, return valid layers.

    layers:
        None -> off
        '*' -> all
        int -> given layer
        list[int] -> given layers

    returns: list[int] of sorted layers
    """
    if layers is None:
        return []
    if isinstance(layers, str):
        if layers == '*':
            layers_list = set()
            for label, synapse in synapses.items():
                layers_list.add(synapse.get_layer())
            return sorted(layers_list)
        return []
    elif isinstance(layers, int):
        return [layers]
    elif isinstance(layers, list):
        return sorted(layers)
    return []


def display_layer_synapse_dict(layer_synapse_dict, prefix="    "):
    """Maps a layers_synapse dictionary to a string for display."""
    s = ""
    for layer in sorted(layer_synapse_dict.keys()):
        s += f"{prefix}layer: {layer}    {sorted(layer_synapse_dict[layer])}\n"
    return s


class NeuralModule:
    """Implement a neuron and synapse module."""
    def __init__(self, name):
        self.name = name
        self.neuron_name_index = 0
        self.delay_counter = 0
        self.sources = {}
        self.current_sources_state = {}
        self.latent_neurons = {}
        self.neurons = {}
        self.current_poked_neurons = set()
        self.new_synapses = {} # rename to latent_synapses?
        self.synapses = {}
        self.default_layer = 0
        self.default_trigger_fn = None
        self.default_trigger_params = {}
        self.default_pooling_fn = None
        self.default_pooling_params = {}
        self.default_synapse_fn = None
        self.default_synapse_params = {}
        self.default_action_fn = None
        self.default_action_params = {}

    def do_you_know_neuron(self, name):
        """Return's True/False if a neuron with the given name is known to the module."""
        return name in self.neurons

    def do_you_know_synapse(self, name):
        """Return's True/False if a synapse with the given name is known to the module."""
        return name in self.synapses

    def get_neuron_name(self):
        """Return a unique neuron name, and check it doesn't already exist."""
        name = f"N{self.neuron_name_index}"
        while name in self.neurons:
            self.neuron_name_index += 1 # this is the increment approach, the other possible one is random integers.
            name = f"N{self.neuron_name_index}"
        self.neuron_name_index += 1 # maybe not needed if neuron is added with the given name.
        return name

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

    def set_delay_counter(self, n):
        """Set our delay counter."""
        self.delay_counter = n

    def get_delay_counter(self):
        """Get the delay counter."""
        return self.delay_counter

    def increment_delay_counter(self):
        """Increment the delay counter by 1."""
        self.delay_counter += 1

    def reset_delay_counter(self):
        """Reset the delay counter to 0."""
        self.delay_counter = 0

    def set_default_layer(self, n):
        """Set the default layer."""
        self.default_layer = n

    def get_default_layer(self):
        """Get the default layer."""
        return self.default_layer

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

    def update_neuron_trigger(self, name, pattern_no, trigger_fn, trigger_params):
        """Update the trigger function for a neuron's pattern."""
        if name not in self.neurons:
            return
        self.neurons[name].update_trigger(pattern_no, trigger_fn, trigger_params)

    def add_latent_neuron_layer(self, name, layer):
        """Add a latent neuron's layer number."""
        if name not in self.latent_neurons:
            self.latent_neurons[name] = {}
        self.latent_neurons[name]['layer'] = layer

    def add_latent_neuron_pooling(self, name, pooling_fn, pooling_params):
        """Add a latent neuron's pooling function."""
        if name not in self.latent_neurons:
            self.latent_neurons[name] = {}
        self.latent_neurons[name]['pooling_fn'] = pooling_fn
        self.latent_neurons[name]['pooling_params'] = pooling_params

    def add_latent_neuron_trigger(self, name, trigger_fn, trigger_params):
        """Add a latent neuron's trigger function."""
        if name not in self.latent_neurons:
            self.latent_neurons[name] = {}
        self.latent_neurons[name]['trigger_fn'] = trigger_fn
        self.latent_neurons[name]['trigger_params'] = trigger_params

    def add_latent_neuron_pattern(self, name, seed_pattern, synapse_labels): # test this beasty!!
        """Add a latent neuron to the module."""
        if name not in self.latent_neurons:
            if name not in self.neurons:
                layer = self.get_default_layer()
                self.add_default_neuron(name, layer, seed_pattern, synapse_labels)
            else:
                self.append_default_neuron_pattern(name, seed_pattern, synapse_labels)
        else:
            if 'layer' in self.latent_neurons[name]:
                layer = self.latent_neurons[name]['layer']
            else:
                layer = self.get_default_layer()

            if 'pooling_fn' in self.latent_neurons[name]:
                pooling_fn = self.latent_neurons[name]['pooling_fn']
            else:
                pooling_fn = self.default_pooling_fn
            if 'pooling_params' in self.latent_neurons[name]:
                pooling_params = self.latent_neurons[name]['pooling_params']
            else:
                pooling_params = self.default_pooling_params

            if 'trigger_fn' in self.latent_neurons[name]:
                trigger_fn = self.latent_neurons[name]['trigger_fn']
            else:
                trigger_fn = self.default_pooling_fn
            if 'trigger_params' in self.latent_neurons[name]:
                trigger_params = self.latent_neurons[name]['trigger_params']
            else:
                trigger_params = self.default_trigger_params

            # now build our neuron:
            if name not in self.neurons:
                self.add_neuron(name, layer, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
            else:
                self.append_neuron_pattern(name, seed_pattern, synapse_labels, trigger_fn, trigger_params)


    def clear_latent_neurons(self):
        """Clear our latent neurons."""
        self.latent_neurons.clear()

    def add_synapse(self, name, axon_name, synapse_fn_type, params, synapse_action_type, action_params):
        """Add a synapse to our system."""
        synapse = Synapse(name, axon_name, synapse_fn_type, params, synapse_action_type, action_params)
        if axon_name in self.neurons:
           layer = self.neurons[axon_name].get_layer()
           synapse.set_layer(layer)
        # self.synapses[name] = synapse
        self.new_synapses[name] = synapse # does this break anything?

    def add_default_synapse(self, name, axon_name):
        """Add a default synapse to our system."""
        synapse = Synapse(name, axon_name, self.default_synapse_fn, self.default_synapse_params, self.default_action_fn, self.default_action_params)
        if axon_name in self.neurons:
           layer = self.neurons[axon_name].get_layer()
           synapse.set_layer(layer)
        # self.synapses[name] = synapse
        self.new_synapses[name] = synapse

    def update_synapse_fn(self, name, synapse_fn, synapse_params):
        """Update the synapse function for a synapse."""
        if name not in self.synapses:
            if name in self.new_synapses:
                self.new_synapses[name].update_fn(synapse_fn, synapse_params)
                return
        self.synapses[name].update_fn(synapse_fn, synapse_params)

    def update_synapse_action(self, name, action_fn, action_params):
        """Update the synapse action for a synapse."""
        if name not in self.synapses:
            if name in self.new_synapses:
                self.new_synapses[name].update_action(action_fn, action_params)
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

    def patch_in_new_synapses(self):
        """Patch in new synapses."""
        spike_history_len = 0
        for label, synapse in self.synapses.items():
            spike_history_len = synapse.get_spike_history_len()
            break
        for label, synapse in self.new_synapses.items(): # patch in the new synapses:
            synapse.set_spike_history([0]*spike_history_len)
            self.synapses[label] = synapse
        self.new_synapses.clear()

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

    def get_active_synapses(self, layers, delays):
        """Return the layers_synapse_dict of relevant current active synapses."""
        layer_synapse_dict = {}
        layers = set(process_layers(self.synapses, layers))
        if isinstance(delays, int):
            delays = {delays}
        elif isinstance(delays, list):
            delays = set(delays)
        else:
            delays = set()
        # print('layers', layers) # comment out later
        # print('delays', delays) # comment out later
        for label, synapse in self.synapses.items():
            layer = synapse.get_layer()
            if layer in layers:
                if layer not in layer_synapse_dict: # use defaultdict(set)?
                    layer_synapse_dict[layer] = set()
                for delay in delays:
                    value = self.synapses[label].read_synapse(delay)
                    if value != 0:
                        s = f"{label} D{delay}"
                        layer_synapse_dict[layer].add(s)
        return layer_synapse_dict

    def update_system(self, steps):
        """Update our system."""
        for _ in range(steps):
            self.patch_in_new_synapses()
            self.update_neurons()
            self.update_synapses()
            self.update_sources()
            self.increment_delay_counter() # here or at the start of this sequence of methods?

    def get_test_neurons(self, pattern):
        """Given a pattern, return a sorted list of neuron names that are triggered by that pattern."""
        # print(f"Inside NM.get_test_neurons() with pattern: {pattern}")
        # self.patch_in_new_synapses() # does this work or bug out?
        neurons = set()
        for name, neuron in self.neurons.items():
            # value = neuron.test_pattern(self.synapses, pattern)
            value = neuron.test_pattern(pattern)
            if value:
                neurons.add(name)
        return sorted(neurons)

    def activation_report(self, activation_threshold):
        """Return an activation report as a string."""
        # Build the dictionary
        # activation_neuron_dict = {} # maybe defaultdict instead?
        activation_neuron_dict = defaultdict(list)
        for name, neuron in self.neurons.items():
            activation = neuron.get_activation_count()
            if activation >= activation_threshold:
                # if activation not in activation_neuron_dict:
                #     activation_neuron_dict[activation] = []
                activation_neuron_dict[activation].append(name)
        # Convert to a string:
        s = "Activation report:\n"
        for activation in sorted(activation_neuron_dict.keys(), reverse=True):
            s += f"    {activation}    {sorted(activation_neuron_dict[activation])}\n"
        return s

    def prune(self, activation_threshold):
        """Prune all neurons with activation less than the given threshold, and corresponding synapses."""
        prune_neuron_set = set()
        for name, neuron in self.neurons.items():
            if neuron.get_activation_count() < activation_threshold:
                prune_neuron_set.add(name)
        for name in prune_neuron_set:
                self.erase_neuron(name)
        prune_synapse_set = set()
        for label, synapse in self.synapses.items():
            if synapse.axon_name in prune_neuron_set:
                prune_synapse_set.add(label)
        for label in prune_synapse_set:
            self.erase_synapse(label)

    def erase_neuron(self, name):
        """Erase the neuron from the module with the given name."""
        # print(f"Erasing neuron {name}")
        del self.neurons[name] # Is this sufficient, or do we need to tweak other dictionaries too?

    def erase_synapse(self, name):
        """Erase the synapse from the module with the given name."""
        # print(f"Erasing synapse {name}")
        del self.synapses[name] # Is this sufficient, or do we need to tweak other dictionaries too?

    def as_chunk(self):
        """Output the neural module in chunk notation."""
        trigger_dict = {}
        pooling_dict = {}
        synapse_dict = {}
        action_dict = {}

        trigger_dict['trigger'] = trigger_inverse_fn_map[self.default_trigger_fn.__name__]
        trigger_dict.update(self.default_trigger_params)

        pooling_dict['pooling'] = pooling_inverse_fn_map[self.default_pooling_fn.__name__]
        pooling_dict.update(self.default_pooling_params)

        synapse_dict['synapse'] = synapse_inverse_fn_map[self.default_synapse_fn.__name__]
        synapse_dict.update(self.default_synapse_params)

        action_dict['action'] = action_inverse_fn_map[self.default_action_fn.__name__]
        action_dict.update(self.default_action_params)
        s = "\nas default:\n"
        s += f"    layer => |{self.default_layer}>\n"
        s += f"    trigger_fn => {sp_dict_to_sp(trigger_dict)}\n"
        s += f"    pooling_fn => {sp_dict_to_sp(pooling_dict)}\n"
        s += f"    synapse_fn => {sp_dict_to_sp(synapse_dict)}\n"
        s += f"    action_fn => {sp_dict_to_sp(action_dict)}\n"
        s += "end:\n"
        layer_neuron_set = defaultdict(set) # maybe put this somewhere else?
        for neuron_name, neuron in self.neurons.items():
            layer = neuron.get_layer()
            layer_neuron_set[layer].add(neuron_name)

        neuron_synapse_set = defaultdict(set) # this might be better off doing somewhere else, not every time as_chunk() is called?
        for synapse_name, synapse in self.synapses.items(): # also, synapses without corresponding neurons are not displayed
            neuron_name = synapse.get_parent_axon_name()
            neuron_synapse_set[neuron_name].add(synapse_name)

        for layer in sorted(layer_neuron_set.keys()):
            for neuron_name in layer_neuron_set[layer]:
                neuron = self.neurons[neuron_name]
                s += neuron.as_chunk(self.default_layer, self.default_trigger_fn, self.default_trigger_params, self.default_pooling_fn, self.default_pooling_params)
                for synapse_name in neuron_synapse_set[neuron_name]:
                    synapse = self.synapses[synapse_name]
                    s += synapse.as_chunk(self.default_synapse_fn, self.default_synapse_params, self.default_action_fn, self.default_action_params)

        # for neuron_name, neuron in self.neurons.items():
        #     s += neuron.as_chunk(self.default_layer, self.default_trigger_fn, self.default_trigger_params, self.default_pooling_fn, self.default_pooling_params)
        #     for synapse_name in neuron_synapse_set[neuron_name]:
        #         synapse = self.synapses[synapse_name]
        #         s += synapse.as_chunk(self.default_synapse_fn, self.default_synapse_params, self.default_action_fn, self.default_action_params)

        # for name, synapse in self.synapses.items():
        #     s += synapse.as_chunk(self.default_synapse_fn, self.default_synapse_params, self.default_action_fn, self.default_action_params)
        return s

    def from_chunk(self, s):
        """Import chunk string into the neural module."""
        parse_sf_if_then_machine(self, s, verbose=False)

    def save_chunks(self, filename):
        """Save the neural module to a file, with the given filename."""
        with open(filename, 'w') as f:
            f.write(self.as_chunk())

    def load_chunks(self, filename):
        """Load the given file into the neural module."""
        with open(filename, 'r') as f:
            s = f.read()
            # parse_sf_if_then_machine(self, s, verbose=False)
            self.from_chunk(s)

    def defaults_as_dict(self):
        """Convert default settings to a python dictionary."""
        default_dict = {}
        trigger_dict = {}
        pooling_dict = {}
        synapse_dict = {}
        action_dict = {}

        # build our dictionaries:
        trigger_dict['trigger'] = trigger_inverse_fn_map[self.default_trigger_fn.__name__]
        trigger_dict.update(self.default_trigger_params)

        pooling_dict['pooling'] = pooling_inverse_fn_map[self.default_pooling_fn.__name__]
        pooling_dict.update(self.default_pooling_params)

        synapse_dict['synapse'] = synapse_inverse_fn_map[self.default_synapse_fn.__name__]
        synapse_dict.update(self.default_synapse_params)

        action_dict['action'] = action_inverse_fn_map[self.default_action_fn.__name__]
        action_dict.update(self.default_action_params)

        # populate our dictionary:
        default_dict['layer'] = self.default_layer
        default_dict['pooling_fn'] = pooling_dict
        default_dict['trigger_fn'] = trigger_dict
        default_dict['synapse_fn'] = synapse_dict
        default_dict['action_fn'] = action_dict
        # return default_dict
        return json.dumps(default_dict, indent=4)

    def print_neuron(self, name):
        """Print the named neuron."""
        if name not in self.neurons:
            return
        print(self.neurons[name])

    def print_synapse(self, name):
        """Print the named synapse."""
        if name not in self.synapses:
            if name in self.new_synapses:
                print(self.new_synapses[name])
                return
        print(self.synapses[name])

    def str_default_fns(self):
        """Return default functions as a string."""
        s = "\nDefault functions and parameters:\n"
        s += f"    layer: {self.default_layer}\n\n"
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
        s += display_layer_synapse_dict(layer_neuron_dict)
        # for layer in sorted(layer_neuron_dict.keys()):
        #     s += f"    layer: {layer}    {sorted(layer_neuron_dict[layer])}\n"
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
        s += display_layer_synapse_dict(layer_synapse_dict)
        # for layer in sorted(layer_synapse_dict.keys()):
        #     s += f"    layer: {layer}    {sorted(layer_synapse_dict[layer])}\n"
        return s

    def __str__(self):
        s = f"Neural Module: {self.name}\n"
        header_len = len(s) - 1
        s += "-" * header_len + "\n"
        # s += f"Neurons: {set(self.neurons.keys())}\n"
        # s += f"Synapses: {set(self.synapses.keys())}\n"
        s += f"\nDelay counter: {self.delay_counter}\n"
        s += self.str_default_fns()
        s += self.str_sources()
        s += self.str_neurons()
        s += self.str_synapses()
        s += self.str_neuron_layers()
        s += self.str_synapse_layers()
        # s += f"\nNeurons: {sorted(self.neurons.keys())}\n"
        # s += f"\nSynapses: {sorted(self.synapses.keys())}\n"
        return s


