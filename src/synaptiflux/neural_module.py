"""Implement a neural module."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-11-10

import json
from collections import defaultdict, deque
from .neuron import Neuron
from .synapse import Synapse
from .parse_simple_sdb import sp_dict_to_sp, parse_sf_if_then_machine, parse_seq, parse_sp, strip_delay, strip_synapse, extract_delay_number
from .trigger_fn import trigger_inverse_fn_map, trigger_fn_map, trigger_list_simm_threshold, trigger_list_min_simm_threshold
from .pooling_fn import pooling_inverse_fn_map, pooling_fn_map, pooling_or
from .synapse_fn import synapse_inverse_fn_map, synapse_fn_map, synapse_identity, synapse_delayed_identity
from .action_fn import action_inverse_fn_map, action_fn_map, action_println, action_time_step_println, action_time_step_coeff_println, action_layer_time_step_coeff_println

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
        self.time_step_counter = 0
        self.delay_counter = 0
        self.sources = {}
        self.current_sources_state = {}
        self.latent_neurons = {}
        self.neurons = {}
        self.current_poked_neurons = set()
        self.poke_neuron_sequence_buffer = deque()
        self.new_synapses = {} # rename to latent_synapses?
        self.synapses = {}
        self.synapse_alias_dict = defaultdict(set)
        self.default_layer = 0
        self.default_trigger_fn = None
        self.default_trigger_params = {}
        self.default_pooling_fn = None
        self.default_pooling_params = {}
        self.default_synapse_fn = None
        self.default_synapse_params = {}
        self.default_action_fn = None
        self.default_action_params = {}

    def __setitem__(self, key, value):
        """Add a neuron or synapse to the module."""
        if isinstance(value, Neuron):
            self.neurons[key] = value
        elif isinstance(value, Synapse):
            self.synapses[key] = value
        else:
            raise TypeError(f"Value must be either a Neuron or Synapse, not type: {type(value).__name__}")

    def __getitem__(self, key):
        """Return a neuron or synapse from the module for the given name."""
        if key in self.neurons:
            return self.neurons[key]
        elif key in self.synapses:
            return self.synapses[key]
        # elif key in self.new_synapses: # not sure if we want to enable this or not?
        #     return self.new_synapses[key]
        raise KeyError(f"No neuron or synapse with the name: {key}")

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

    def update_synapse_layers(self):
        """Update our synapse layers."""
        for synapse_name, synapse in self.synapses.items():
            neuron_name = strip_synapse(synapse_name)
            layer = self.neurons[neuron_name].get_layer()
            synapse.set_layer(layer)

    # Do we want default layers too?

    def get_time_step(self):
        """Get the current time step."""
        return self.time_step_counter

    def set_time_step(self, n):
        """Set the current time step."""
        self.time_step_counter = n

    def reset_time_step(self):
        """Reset the current time step."""
        self.time_step_counter = 0

    def increment_time_step(self):
        """Increment the current time step."""
        self.time_step_counter += 1

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

    def add_synapse_alias(self, source_synapse_name, destination_synapse_name):
        """Add a synapse alias, where source synapses rewrite to destination synapses."""
        self.synapse_alias_dict[destination_synapse_name].add(source_synapse_name)

    def add_synapse(self, name, axon_name, synapse_fn_type, params, synapse_action_type, action_params):
        """Add a synapse to our system."""
        synapse = Synapse(name, axon_name, synapse_fn_type, params, synapse_action_type, action_params)
        if axon_name in self.neurons:
           layer = self.neurons[axon_name].get_layer()
           synapse.set_layer(layer)
        # self.synapses[name] = synapse
        self.new_synapses[name] = synapse # does this break anything?
        self.add_synapse_alias(name, name)

    def add_default_synapse(self, name, axon_name):
        """Add a default synapse to our system."""
        synapse = Synapse(name, axon_name, self.default_synapse_fn, self.default_synapse_params, self.default_action_fn, self.default_action_params)
        if axon_name in self.neurons:
           layer = self.neurons[axon_name].get_layer()
           synapse.set_layer(layer)
        # self.synapses[name] = synapse
        self.new_synapses[name] = synapse
        self.add_synapse_alias(name, name)

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
            neuron.update_axon(self.current_sources_state, self.synapses, poked, self.synapse_alias_dict)
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

    def poke_neuron_sequence(self, seq):
        """Poke neurons in a sequence, one each time step."""
        self.poke_neuron_sequence_buffer.extend(seq)

    def update_poked_neuron_set(self):
        """Update the poked neuron set with values from the poked neuron sequence buffer."""
        if self.poke_neuron_sequence_buffer: # check not empty:
            next_value = self.poke_neuron_sequence_buffer.popleft()
            if isinstance(next_value, list):
                self.poke_neurons(next_value)
            else:
                self.poke_neuron(next_value)

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
            self.update_poked_neuron_set()
            self.update_neurons()
            self.update_synapses()
            self.update_sources()
            self.increment_time_step()
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

    def as_chunk(self, grouped=True):
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

        if grouped: # grouped output mode:
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
        else: # flat mode:
            for neuron_name, neuron in self.neurons.items():
                s += neuron.as_chunk(self.default_layer, self.default_trigger_fn, self.default_trigger_params, self.default_pooling_fn, self.default_pooling_params)
            for name, synapse in self.synapses.items():
                s += synapse.as_chunk(self.default_synapse_fn, self.default_synapse_params, self.default_action_fn, self.default_action_params)
        return s

    def from_chunk(self, input_chunks):
        """Import chunk string into the neural module."""
        parse_sf_if_then_machine(self, input_chunks, verbose=False)

    def save_as_chunk(self, filename, grouped=True):
        """Save the neural module to a file using chunk notation, with the given filename."""
        with open(filename, 'w') as f:
            f.write(self.as_chunk())
            # f.write(self.as_chunk(grouped))

    def load_from_chunk(self, filename):
        """Load the given file of chunks into the neural module."""
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
        if self.default_trigger_fn is None:
            trigger_dict = None
        else:
            trigger_dict['trigger'] = trigger_inverse_fn_map[self.default_trigger_fn.__name__]
            trigger_dict.update(self.default_trigger_params)

        if self.default_pooling_fn is None:
            pooling_dict = None
        else:
            pooling_dict['pooling'] = pooling_inverse_fn_map[self.default_pooling_fn.__name__]
            pooling_dict.update(self.default_pooling_params)

        if self.default_synapse_fn is None:
            synapse_dict = None
        else:
            synapse_dict['synapse'] = synapse_inverse_fn_map[self.default_synapse_fn.__name__]
            synapse_dict.update(self.default_synapse_params)

        if self.default_action_fn is None:
            action_dict = None
        else:
            action_dict['action'] = action_inverse_fn_map[self.default_action_fn.__name__]
            action_dict.update(self.default_action_params)

        # populate our dictionary:
        default_dict['layer'] = self.default_layer
        default_dict['pooling_fn'] = pooling_dict
        default_dict['trigger_fn'] = trigger_dict
        default_dict['synapse_fn'] = synapse_dict
        default_dict['action_fn'] = action_dict
        return default_dict
        # return json.dumps(default_dict, indent=4)

    def as_flat_dict(self):
        """Output the module as a flat Python dictionary."""
        output_dict = {}
        output_dict['defaults'] = self.defaults_as_dict()
        output_dict['neurons'] = [neuron.as_dict() for name, neuron in self.neurons.items()]
        output_dict['synapses'] = [synapse.as_dict() for name, synapse in self.synapses.items()]
        # return json.dumps(output_dict, indent=4)
        return output_dict

    def as_flat_json(self):
        """Output the module as a flat JSON string."""
        return json.dumps(self.as_flat_dict(), indent=4)

    def as_grouped_dict(self):
        """Output the module as a Python dictionary, with neurons and corresponding synapses in groups."""
        output_dict = {}
        layer_neuron_set = defaultdict(set) # maybe put this somewhere else?
        for neuron_name, neuron in self.neurons.items():
            layer = neuron.get_layer()
            layer_neuron_set[layer].add(neuron_name)

        neuron_synapse_set = defaultdict(set) # this might be better off doing somewhere else, not every time as_chunk() is called?
        for synapse_name, synapse in self.synapses.items(): # also, synapses without corresponding neurons are not displayed
            neuron_name = synapse.get_parent_axon_name()
            neuron_synapse_set[neuron_name].add(synapse_name)

        neuron_synapse_groups = []
        for layer in sorted(layer_neuron_set.keys()):
            for neuron_name in layer_neuron_set[layer]:
                neuron_synapse_dict = {}
                neuron = self.neurons[neuron_name]
                neuron_synapse_dict['neuron'] = neuron.as_dict()
                synapses = []
                for synapse_name in neuron_synapse_set[neuron_name]:
                    synapse = self.synapses[synapse_name]
                    synapses.append(synapse.as_dict())
                neuron_synapse_dict['synapses'] = synapses
                neuron_synapse_groups.append(neuron_synapse_dict)
        output_dict['defaults'] = self.defaults_as_dict()
        output_dict['neuron_synapse_groups'] = neuron_synapse_groups
        return output_dict

    def as_grouped_json(self):
        """Output the module as a JSON string, with neurons and corresponding synapses in groups."""
        return json.dumps(self.as_grouped_dict(), indent=4)

    def save_as_json(self, filename, grouped=True):
        """Save the module as json to a file."""
        output_dict = {}
        if grouped:
            output_dict['json_type'] = 'grouped'
            output_dict.update(self.as_grouped_dict())
        else:
            output_dict['json_type'] = 'flat'
            output_dict.update(self.as_flat_dict())
        with open(filename, 'w') as f:
            json.dump(output_dict, f, indent=4)
        # with open(filename, 'w', encoding='utf-8') as f: # UTF-8 version
        #     json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_json(self, filename):
        """Load the json file into the module."""
        with open(filename, 'r') as f:
            input_dict = json.load(f)
            json_type = input_dict['json_type']
            print(f"JSON type: {json_type}")
            defaults_dict = input_dict['defaults']
            # print(json.dumps(defaults_dict, indent=4))
            self.defaults_from_dict(defaults_dict) # load the defaults here, or in from_grouped_dict and from_dict??
            del input_dict['defaults']
            if json_type == 'grouped':
                self.from_grouped_dict(input_dict)
            elif json_type == 'flat':
                self.from_flat_dict(input_dict)

    def defaults_from_dict(self, defaults_dict):
        """Load defaults into the neural module from the given dictionary."""
        for key, value in defaults_dict.items():
            if key == 'layer':
                try:
                    layer = int(value)
                    self.set_default_layer(layer)
                except:
                    continue
            elif key == 'pooling_fn':
                try:
                    pooling_fn_str = value['pooling']
                    pooling_fn = pooling_fn_map[pooling_fn_str]
                    del value['pooling']
                    self.set_default_pooling(pooling_fn, value)
                except:
                    continue
            elif key == 'trigger_fn':
                try:
                    trigger_fn_str = value['trigger']
                    trigger_fn = trigger_fn_map[trigger_fn_str]
                    del value['trigger']
                    self.set_default_trigger(trigger_fn, value)
                except:
                    continue
            elif key == 'synapse_fn':
                try:
                    synapse_fn_str = value['synapse']
                    synapse_fn = synapse_fn_map[synapse_fn_str]
                    del value['synapse']
                    self.set_default_synapse(synapse_fn, value)
                except:
                    continue
            elif key == 'action_fn':
                try:
                    action_fn_str = value['action']
                    action_fn = action_fn_map[action_fn_str]
                    del value['action']
                    self.set_default_action(action_fn, value)
                except:
                    continue

    def from_grouped_dict(self, input_dict):
        """Load the given 'grouped' dictionary into the neural module."""
        try:
            # defaults_dict = input_dict['defaults'] # enable this?
            # self.defaults_from_dict(defaults_dict)
            neuron_synapse_groups = input_dict['neuron_synapse_groups']
            # print(json.dumps(neuron_synapse_groups, indent=4))
            for group_dict in neuron_synapse_groups:
                # print(json.dumps(group_dict, indent=4))
                neuron_dict = group_dict['neuron']
                synapses = group_dict['synapses']
                neuron = Neuron.from_dict(neuron_dict)
                # print(neuron)
                self[neuron.name] = neuron # wrap .name in a get method call?
                for synapse_dict in synapses:
                    synapse = Synapse.from_dict(synapse_dict)
                    # print(synapse)
                    self[synapse.name] = synapse # wrap .name in a get method call?
                # break # for testing only, delete later!
        except Exception as e:
            print(e)

    def from_flat_dict(self, input_dict):
        """Load the given 'flat' dictionary into the neural module."""
        try:
            # defaults_dict = input_dict['defaults'] # enable this?
            # self.defaults_from_dict(defaults_dict)
            neurons = input_dict['neurons']
            for neuron_dict in neurons:
                neuron = Neuron.from_dict(neuron_dict)
                self[neuron.name] = neuron
            synapses = input_dict['synapses']
            for synapse_dict in synapses:
                synapse = Synapse.from_dict(synapse_dict)
                self[synapse.name] = synapse
        except Exception as e:
            print(e)

    def from_map(self, s, verbose=False):
        """Load the map string s into the neural module."""
        # set some defaults:
        layer = 0
        synapse_number = 0
        for line in s.splitlines():
            line = line.strip()
            if len(line) == 0 or line.startswith('--'):
                continue
            if verbose:
                print(f'\nline: {line}')
            synapse_neuron = False
            neuron_synapse = False
            # parse them:
            try:
                pattern, neurons = line.split(' => ', 1)
                coeffs, synapse_labels = parse_seq(pattern, synapse_number=synapse_number)
                neuron_names = parse_sp(neurons)[1]
                clean_synapse_labels = [strip_delay(s) for s in synapse_labels]
                # max_layer = max(self.synapses[synapse_name].get_layer() for synapse_name in clean_synapse_labels) # unknown synapses break this!
                synapse_neuron = True
            except Exception as e:
                try:
                    neurons, pattern = line.split(' |=> ', 1)
                    neuron_names = parse_sp(neurons)[1]
                    coeffs, synapse_labels = parse_seq(pattern, synapse_number=synapse_number, reverse=False)
                    clean_synapse_labels = [strip_delay(s) for s in synapse_labels]
                    clean_neuron_labels = [strip_synapse(s) for s in clean_synapse_labels]
                    synapse_delays = [extract_delay_number(s) for s in synapse_labels]
                    neuron_synapse = True
                except Exception as e:
                    print(e)
                    continue
            if synapse_neuron:
                if verbose:
                    print(f'\npattern: {pattern}')
                    print(f'neurons: {neurons}')
                    print(f'coeffs: {coeffs}')
                    print(f'synapse_labels: {synapse_labels}')
                    print(f'clean_synapse_labels: {clean_synapse_labels}')
                    print(f'neuron_names: {neuron_names}')
                    # print(f'max_layer: {max_layer}') # we don't have enough info at this stage to know this
                # now build the neurons:
                for neuron_name in neuron_names:
                    if not self.do_you_know_neuron(neuron_name):
                        if verbose:
                            print(f'Unknown neuron: "{neuron_name}", adding it')
                        # self.add_neuron(self, name, layer, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
                        self.add_neuron(neuron_name, layer, coeffs, synapse_labels, trigger_list_min_simm_threshold, {'threshold': 0.98}, pooling_or, {})
                    else:
                        if verbose:
                            print(f'Known neuron: "{neuron_name}", appending to it')
                        # append_neuron_pattern(self, name, seed_pattern, synapse_labels, trigger_fn, trigger_params)
                        self.append_neuron_pattern(neuron_name, coeffs, synapse_labels, trigger_list_min_simm_threshold, {'threshold': 0.98}) # test this code section
                    synapse_name = f'{neuron_name} S0' # hardwire in synapse number here for now.
                    if not self.do_you_know_synapse(synapse_name):
                        # self.add_synapse(self, name, axon_name, synapse_fn_type, params, synapse_action_type, action_params)
                        # self.add_synapse(synapse_name, neuron_name, synapse_identity, {'sign': 1}, action_println, {'s': neuron_name})
                        self.add_synapse(synapse_name, neuron_name, synapse_identity, {'sign': 1}, action_layer_time_step_coeff_println, {'s': neuron_name, 'NM': self}) # does this work?? Yup!
                        self.patch_in_new_synapses() # is this the best place for this?
                # initialize neuron_layer_dict:
                # neuron_layer_dict = defaultdict(int)
                # now build the unknown synapses:
                for synapse_name in clean_synapse_labels:
                    neuron_name = strip_synapse(synapse_name)
                    if not self.do_you_know_synapse(synapse_name):
                        if verbose:
                            print(f'Unknown synapse: "{synapse_name}"')
                        # neuron_name = strip_synapse(synapse_name)
                        self.add_neuron(neuron_name, layer, [1], ['#OFF#'], trigger_list_min_simm_threshold, {'threshold': 0.98}, pooling_or, {})
                        # self.add_synapse(synapse_name, neuron_name, synapse_identity, {'sign': 1}, action_println, {'s': neuron_name})
                        self.add_synapse(synapse_name, neuron_name, synapse_identity, {'sign': 1}, action_layer_time_step_coeff_println, {'s': neuron_name, 'NM': self}) # does this work?? Yup!
                        self.patch_in_new_synapses() # is this the best place for this?
                    # neuron_layer_dict[neuron_name] = max(neuron_layer_dict[neuron_name], self.synapses[synapse_name].get_layer())
                # now write the neuron layers to our neurons:
                # for neuron_name, layer in neuron_layer_dict.items(): # do we need to write synapse layers too?
                #     # self[neuron_name].set_layer(layer + 1)
                #     self.neurons[neuron_name].set_layer(layer + 1)
                # now write the neuron layers to our synapses:
                # for synapse_name in clean_synapse_labels:
                #     neuron_name = strip_synapse(synapse_name)
                #     layer = self.neurons[neuron_name].get_layer()
                #     self.synapses[synapse_name].set_layer(layer)
                max_layer = max(self.synapses[synapse_name].get_layer() for synapse_name in clean_synapse_labels)
                if verbose:
                    print(f'max_layer: {max_layer}')
                for neuron_name in neuron_names:
                    self.neurons[neuron_name].set_layer(max_layer + 1)
                self.update_synapse_layers()
            if neuron_synapse:
                if verbose:
                    print(f'\nneurons: {neurons}')
                    print(f'neuron_names: {neuron_names}')
                    print(f'pattern: {pattern}')
                    print(f'coeffs: {coeffs}')
                    print(f'synapse_labels: {synapse_labels}')
                    print(f'synapse_delays: {synapse_delays}')
                    print(f'clean_synapse_labels: {clean_synapse_labels}')
                    print(f'clean_neuron_labels: {clean_neuron_labels}')
                # build our RHS neurons:
                for neuron_name in clean_neuron_labels:
                    if not self.do_you_know_neuron(neuron_name):
                        if verbose:
                            print(f'Unknown neuron: "{neuron_name}", adding it')
                        # self.add_neuron(self, name, layer, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
                        self.add_neuron(neuron_name, layer, [1], ['#OFF#'], trigger_list_min_simm_threshold, {'threshold': 0.98}, pooling_or, {})
                        synapse_name = f'{neuron_name} S{synapse_number}'
                        if not self.do_you_know_synapse(synapse_name):
                            if verbose:
                                print(f'Unknown synapse: "{synapse_name}", adding it')
                            self.add_synapse(synapse_name, neuron_name, synapse_identity, {'sign': 1}, action_layer_time_step_coeff_println, {'s': neuron_name, 'NM': self}) # does this work?? Yup!
                            self.patch_in_new_synapses() # is this the best place for this?
                    # else:
                    #     if verbose:
                    #         print(f'Known neuron: "{neuron_name}", appending to it')
                    #     # append_neuron_pattern(self, name, seed_pattern, synapse_labels, trigger_fn, trigger_params)
                    #     self.append_neuron_pattern(neuron_name, [1], ['#OFF'], trigger_list_simm_threshold, {'threshold': 0.98}) # test this code section
                # now build the LHS neurons:
                for neuron_name in neuron_names:
                    if not self.do_you_know_neuron(neuron_name):
                        if verbose:
                            print(f'Unknown neuron: "{neuron_name}", adding it')
                        # self.add_neuron(self, name, layer, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
                        self.add_neuron(neuron_name, layer, [1], ['#OFF#'], trigger_list_min_simm_threshold, {'threshold': 0.98}, pooling_or, {})
                    # else:
                    #     if verbose:
                    #         print(f'Known neuron: "{neuron_name}", appending to it')
                    #     # append_neuron_pattern(self, name, seed_pattern, synapse_labels, trigger_fn, trigger_params)
                    #     self.append_neuron_pattern(neuron_name, [1], ['#OFF#'], trigger_list_simm_threshold, {'threshold': 0.98}) # test this code section
                    for idx in range(len(synapse_labels)):
                        synapse_name = f'{neuron_name} S{idx}' # yeah, currently stomps on existing synapses! TODO: fix later!
                        sign = coeffs[idx]
                        delay = synapse_delays[idx]
                        alias = clean_neuron_labels[idx]
                        alias_synapse = f'{alias} S0'
                        if verbose:
                            print(f'Adding synapse: "{synapse_name}", sign: {sign}, delay: {delay} -> "{alias_synapse}"')
                        # self.add_synapse(synapse_name, neuron_name, synapse_delayed_identity, {'sign': sign, 'delay': delay}, action_time_step_println, {'s': neuron_name, 'NM': self})
                        self.add_synapse(synapse_name, neuron_name, synapse_delayed_identity, {'sign': sign, 'delay': delay}, action_layer_time_step_coeff_println, {'s': alias, 'NM': self})
                        self.patch_in_new_synapses() # is this the best place for this?
                        self.add_synapse_alias(synapse_name, alias_synapse)
        # self.update_synapse_layers()

    def load_from_map(self, filename, verbose=False):
        """Load the map file into the neural module."""
        with open(filename, 'r') as f:
            self.from_map(f.read(), verbose)

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
        s += f"    poked neurons: {self.current_poked_neurons}\n"
        s += f"    poked sequence buffer: {self.poke_neuron_sequence_buffer}\n\n"
        for label, neuron in self.neurons.items():
            s += f"{neuron}\n"
        return s

    def str_synapses(self):
        """Return synapses as a string."""
        s = "Synapses:\n"
        s += "    aliases:\n"
        for label, alias_set in self.synapse_alias_dict.items():
            s += f'        "{label}" <- {alias_set}\n'
        s += '\n'
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


