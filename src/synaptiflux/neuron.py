"""Implement a single reductionist neuron."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-11-8

from .parse_simple_sdb import sp_dict_to_sp, coeff_labels_to_sp
from .pooling_fn import pooling_inverse_fn_map, pooling_fn_map
from .trigger_fn import trigger_inverse_fn_map, trigger_fn_map

class Neuron:
    """Implements a single reductionist neuron."""
    def __init__(self, name, layer, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params):
        if len(seed_pattern) != len(synapse_labels):
            print(f"Unable to create the neuron \"{name}\".")
            print(f"Patterns and labels must be the same length. {len(seed_pattern)} != {len(synapse_labels)}")
            self.valid = False
            return
        self.name = name
        self.layer = layer
        self.activation_count = 0
        self.pattern_count = 0
        self.pattern = {}
        self.pattern_labels = {}
        self.trigger_fn = {}
        self.trigger_params = {}
        self.pooling_fn = pooling_fn
        self.pooling_params = pooling_params
        self.axon = []
        self.pattern[self.pattern_count] = seed_pattern
        self.pattern_labels[self.pattern_count] = synapse_labels
        self.trigger_fn[self.pattern_count] = trigger_fn
        self.trigger_params[self.pattern_count] = trigger_params
        self.pattern_count += 1
        self.valid = True

    def set_layer(self, n):
        """Set the neuron's layer."""
        self.layer = n

    def get_layer(self):
        """Get the neuron's layer."""
        return self.layer

    def increment_activation_count(self):
        """Increase the activation count by 1."""
        self.activation_count += 1

    def set_activation_count(self, n):
        """Set the activation count to n."""
        self.activation_count = n

    def get_activation_count(self):
        """Get the activation count."""
        return self.activation_count

    def append_pattern(self, seed_pattern, synapse_labels, trigger_fn, trigger_params):
        """Adds another pattern to a neuron."""
        if not self.valid:
            print("Invalid neuron")
            return
        if len(seed_pattern) != len(synapse_labels):
            print(f"Unable to append pattern to the neuron \"{self.name}\".")
            print(f"Patterns and labels must be the same length. {len(seed_pattern)} != {len(synapse_labels)}")
            return
        self.pattern[self.pattern_count] = seed_pattern
        self.pattern_labels[self.pattern_count] = synapse_labels
        self.trigger_fn[self.pattern_count] = trigger_fn
        self.trigger_params[self.pattern_count] = trigger_params
        self.pattern_count += 1

    def update_pattern(self, pattern_number, seed_pattern, synapse_labels):
        """Updates an existing pattern. Pattern numbers start from 0, not 1."""
        if not self.valid:
            print("Invalid neuron")
            return
        if pattern_number >= self.pattern_count:
            print(f"Invalid pattern number {pattern_number}.")
            return
        if len(seed_pattern) != len(synapse_labels):
            print(f"Unable to append pattern to the neuron \"{self.name}\".")
            print(f"Patterns and labels must be the same length. {len(seed_pattern)} != {len(synapse_labels)}")
            return
        self.pattern[pattern_number] = seed_pattern
        self.pattern_labels[pattern_number] = synapse_labels

    def poke_neuron(self):
        """Sets the last element of the axon list to 1."""
        if not self.valid:
            print("Invalid neuron")
            return
        if len(self.axon) == 0: # maybe do something different if the axon list is empty?
            return
        self.axon[-1] = 1

    def append_to_axon(self, value):
        """Appends a value to the axon list.
        Later this will be auto-activated based on the input to the neuron.
        For now it is activated manually.
        """
        if not self.valid:
            print("Invalid neuron")
            return
        self.axon.append(value)

    def update_axon(self, current_sources, synapses, poked, synapse_alias_dict):
        """Calculate and then update our axon list."""
        if not self.valid:
            print("Invalid neuron")
            return
        if poked:
            self.axon.append(1)
            self.activation_count += 1
            return
        pooling_list = []
        for k in range(self.pattern_count):
            input_pattern = []
            for label in self.pattern_labels[k]:
                value = 0
                if label in current_sources:
                    value = current_sources[label]
                # elif label in synapses:
                #     if len(synapses[label].spike_history) > 0: # replace with synapse.read_synapse()?
                #         value = synapses[label].spike_history[-1]
                else:
                    delay = 0
                    if label not in synapses:
                        try:
                            label, delay_str = label.rsplit(" D", 1)
                            delay = int(delay_str)
                        except ValueError:
                            delay = 0
                    # if label in synapses:
                    #     value = synapses[label].read_synapse(delay)
                    if label in synapse_alias_dict:
                        # value = max(synapses[sublabel].read_synapse(delay) for sublabel in synapse_alias_dict[label])
                        value = sum(synapses[sublabel].read_synapse(delay) for sublabel in synapse_alias_dict[label]) # testing max vs sum
                input_pattern.append(value)
            fn = self.trigger_fn[k]
            # print(f"{self.name} pattern: {input_pattern}")
            result = fn(self.pattern[k], input_pattern, **self.trigger_params[k])
            pooling_list.append(result)
        # print(f"{self.name} pooling: {pooling_list}")
        axon_value = self.pooling_fn(pooling_list)
        self.axon.append(axon_value)
        if axon_value != 0: # != 0, vs > 0?
            self.activation_count += 1

    def update_pooling(self, pooling_fn, pooling_params):
        """Update the neuron's pooling function and parameters."""
        self.pooling_fn = pooling_fn
        self.pooling_params = pooling_params

    def update_trigger(self, pattern_no, trigger_fn, trigger_params):
        """Update the neuron's trigger function and parameters for a particular pattern number."""
        if pattern_no < 0 or pattern_no >= self.pattern_count:
            return
        self.trigger_fn[pattern_no] = trigger_fn
        self.trigger_params[pattern_no] = trigger_params

    # def test_pattern(self, synapses, pattern): # later remove synapses parameter. No longer needed!
    def test_pattern(self, pattern):
        """Feed a pattern into a neuron, and test if it triggers or not, using the trigger function."""
        for k in range(self.pattern_count):
            input_pattern = []
            for label in self.pattern_labels[k]:
                value = 0
                # delay = 0
                # new_label = label
                # if label not in synapses:
                #     try:
                #         new_label, delay_str = label.rsplit(" D", 1)
                #         delay = int(delay_str)
                #     except ValueError:
                #         delay = 0
                # if label in synapses or new_label in synapses:
                #     # value = synapses[label].read_synapse(delay)
                #     if label in pattern or new_label in pattern:
                #         value = 1
                if label in pattern:
                    value = 1
                input_pattern.append(value)
            fn = self.trigger_fn[k]
            result = fn(self.pattern[k], input_pattern, **self.trigger_params[k])
            if result != 0:
                return True
        return False

    def as_chunk(self, default_layer=None, default_trigger_fn=None, default_trigger_params=None, default_pooling_fn=None, default_pooling_params=None):
        """Output the neuron in chunk notation."""
        s = f"\nas neuron |{self.name}>:\n"
        if self.layer != default_layer:
            s += f"    layer => |{self.layer}>\n"
        if self.pooling_fn != default_pooling_fn or self.pooling_params != default_pooling_params:
            pooling_dict = {}
            pooling_dict['pooling'] = pooling_inverse_fn_map[self.pooling_fn.__name__]
            pooling_dict.update(self.pooling_params)
            s += f"    pooling => {sp_dict_to_sp(pooling_dict)}\n"
        latent_trigger_fn = None
        latent_trigger_params = {}
        for k in range(self.pattern_count):
            update_trigger_fn = False
            if latent_trigger_fn is None:
                if self.trigger_fn[k] != default_trigger_fn or self.trigger_params[k] != default_trigger_params:
                    update_trigger_fn = True
            else:
                if self.trigger_fn[k] != latent_trigger_fn or self.trigger_params[k] != latent_trigger_params:
                    update_trigger_fn = True
            if update_trigger_fn:
                latent_trigger_fn = self.trigger_fn[k]
                latent_trigger_params = self.trigger_params[k]
                trigger_dict = {}
                trigger_dict['trigger'] = trigger_inverse_fn_map[self.trigger_fn[k].__name__]
                trigger_dict.update(self.trigger_params[k])
                s += f"    trigger_fn => {sp_dict_to_sp(trigger_dict)}\n"
            s += f"    pattern => {coeff_labels_to_sp(self.pattern[k], self.pattern_labels[k])}\n"
        s += "end:\n"
        return s

    def as_dict(self):
        """Ouput the neuron as a Python dictionary."""
        output_dict = {}

        pooling_dict = {}
        pooling_dict['pooling'] = pooling_inverse_fn_map[self.pooling_fn.__name__]
        pooling_dict.update(self.pooling_params)

        patterns = []
        for k in range(self.pattern_count):
            pattern_dict = {}
            trigger_dict = {}
            trigger_dict['trigger'] = trigger_inverse_fn_map[self.trigger_fn[k].__name__]
            trigger_dict.update(self.trigger_params[k])
            pattern_dict['trigger_fn'] = trigger_dict
            pattern_dict['coeffs'] = self.pattern[k]
            pattern_dict['synapse_labels'] = self.pattern_labels[k]
            patterns.append(pattern_dict)

        output_dict['name'] = self.name
        output_dict['layer'] = self.layer
        output_dict['activation_count'] = self.activation_count
        output_dict['pooling_fn'] = pooling_dict
        output_dict['patterns'] = patterns
        return output_dict

    @classmethod
    def from_dict(cls, neuron_dict):
        """Create the neuron from the given Python dictionary."""
        constructed_neuron = cls('', 0, [], [], None, {}, None, {}) # do we need "constructed_neuron" here, or can we just use cls?
        for key, value in neuron_dict.items():
            try:
                if key == 'name':
                    constructed_neuron.name = value
                elif key == 'layer':
                    try:
                        layer = int(value)
                    except:
                        layer = 0
                    constructed_neuron.layer = layer
                elif key == 'activation_count':
                    try:
                        activation_count = int(value)
                    except:
                        activation_count = 0
                    constructed_neuron.activation_count = activation_count
                elif key == 'pooling_fn':
                    try:
                        pooling_fn_str = value['pooling']
                        pooling_fn = pooling_fn_map[pooling_fn_str]
                        del value['pooling']
                        constructed_neuron.pooling_fn = pooling_fn
                        constructed_neuron.pooling_params = value
                    except Exception as e:
                        print(e)
                        # continue
                elif key == 'patterns':
                    try:
                        pattern_count = len(value)  # value == patterns list
                        constructed_neuron.pattern_count = pattern_count
                        # print(f"pattern count: {pattern_count}")
                        for k in range(pattern_count):
                            pattern = value[k]
                            # print(f"\n pattern: {value[k]}")
                            try:
                                for pattern_key, pattern_value in pattern.items():
                                    if pattern_key == 'trigger_fn':
                                        trigger_fn_str = pattern_value['trigger']
                                        trigger_fn = trigger_fn_map[trigger_fn_str]
                                        del pattern_value['trigger']
                                        # print(f"trigger_fn_str: {trigger_fn_str}, trigger_fn: {trigger_fn}")
                                        constructed_neuron.trigger_fn[k] = trigger_fn
                                        constructed_neuron.trigger_params[k] = pattern_value
                                    elif pattern_key == 'coeffs':
                                        constructed_neuron.pattern[k] = pattern_value
                                    elif pattern_key == 'synapse_labels':
                                        constructed_neuron.pattern_labels[k] = pattern_value
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)

            except Exception as e:
                print(e)
                continue
        return constructed_neuron

    def apply_operator(self, pattern_number, operator, params):
        """Apply the operator with params to the given pattern number."""
        if pattern_number >= self.pattern_count:
            return # no matching pattern, so return
        coeffs = self.pattern[pattern_number]
        labels = self.pattern_labels[pattern_number]
        new_coeffs, new_labels = operator(coeffs, labels, **params)
        self.pattern[pattern_number] = new_coeffs
        self.pattern_labels[pattern_number] = new_labels

    def __str__(self):
        if not self.valid:
            print("Invalid neuron")
            return ""
        s = f"Neuron: {self.name}\n"
        s += f"    layer: {self.layer}\n"
        s += f"    activation count: {self.activation_count}\n"
        s += f"    pooling: {self.pooling_fn}\n"
        s += f"    params: {self.pooling_params}\n"
        s += f"    patterns: {self.pattern_count}\n"
        for k in range(self.pattern_count):
            s += f"        {k}    trigger: {self.trigger_fn[k]}\n"
            s += f"        {k}    params: {self.trigger_params[k]}\n"
            s += f"        {k}    {self.pattern[k]}\n"
            s += f"        {k}    {self.pattern_labels[k]}\n\n"
        s += f"    axon: {self.axon}\n"
        return s


