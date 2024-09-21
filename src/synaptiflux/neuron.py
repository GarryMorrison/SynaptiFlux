"""Implement a single reductionist neuron."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-9-18

class Neuron:
    """Implements a single reductionist neuron."""
    def __init__(self, name, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params):
        if len(seed_pattern) != len(synapse_labels):
            print(f"Unable to create the neuron \"{name}\".")
            print(f"Patterns and labels must be the same length. {len(seed_pattern)} != {len(synapse_labels)}")
            self.valid = False
            return
        self.name = name
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

    def update_axon(self, current_sources, synapses, poked):
        """Calculate and then update our axon list."""
        if not self.valid:
            print("Invalid neuron")
            return
        if poked:
            self.axon.append(1)
            return
        pooling_list = []
        for k in range(self.pattern_count):
            input_pattern = []
            # value = 0 # Nope, buggy!
            for label in self.pattern_labels[k]:
                value = 0
                if label in current_sources:
                    value = current_sources[label]
                elif label in synapses:
                    if len(synapses[label].spike_history) > 0: # replace with synapse.read_synapse()?
                        value = synapses[label].spike_history[-1]
                input_pattern.append(value)
            fn = self.trigger_fn[k]
            # print(f"{self.name} pattern: {input_pattern}")
            result = fn(self.pattern[k], input_pattern, **self.trigger_params[k])
            pooling_list.append(result)
        # print(f"{self.name} pooling: {pooling_list}")
        axon_value = self.pooling_fn(pooling_list)
        self.axon.append(axon_value)

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

    def __str__(self):
        if not self.valid:
            print("Invalid neuron")
            return ""
        s = f"Neuron: {self.name}\n"
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


