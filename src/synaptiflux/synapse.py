"""Implement a single synapse."""
# Author: Garry Morrison
# Created: 2024-9-18
# Updated: 2024-10-11

class Synapse:
    """Implements a single reductionist synapse."""
    def __init__(self, name, axon_name, synapse_fn_type, params, synapse_action_type, action_params):
        if not isinstance(axon_name, str):
            raise TypeError('axon_name must be type string')
        self.name = name
        self.axon_name = axon_name
        self.layer = -1
        self.synapse_fn = synapse_fn_type
        self.params = params # rename this to self.synapse_params?
        self.spike_history = []
        self.action_fn = synapse_action_type
        self.action_params = action_params

    def get_parent_axon_name(self):
        """Return the name of the parent axon/neuron."""
        return self.axon_name

    def get_layer(self):
        """Return the synapse layer number."""
        return self.layer

    def set_layer(self, n):
        """Set the synapse layer number."""
        self.layer = n

    def read_synapse(self, delay):
        """Read and return the current value of the synapse, with the current delay."""
        if delay < 0: # we can't see into the future!
            return 0
        if len(self.spike_history) <= delay:
            return 0
        return self.spike_history[- 1 - delay]

    def update_fn(self, synapse_fn, synapse_params):
        """Update the synapse function."""
        self.synapse_fn = synapse_fn
        self.params = synapse_params

    def update_action(self, action_fn, action_params):
        """Update the synapse action."""
        self.action_fn = action_fn
        self.action_params = action_params

    def append_to_history(self, value):
        """Append to the spike history list, just used for testing."""
        self.spike_history.append(value)

    def get_spike_history_len(self):
        """Return the length of the current spike history."""
        return len(self.spike_history)

    def set_spike_history(self, spike_history):
        """Set the spike history. Eg, used if adding a new synapse part way through a run."""
        self.spike_history = spike_history

    def update_spike_history(self, neurons):
        """Given a dictionary of neurons, calculate and update the spike history list.
        Followed by applying the desired action.
        """
        if self.axon_name not in neurons:
            self.spike_history.append(0)
            self.action_fn(self, 0, **self.action_params) # do we want this, or comment it out?
            return
        value = self.synapse_fn(neurons[self.axon_name].axon, **self.params)
        self.spike_history.append(value)
        self.action_fn(self, value, **self.action_params)

    def __str__(self):
        s = f"Synapse: {self.name}\n"
        s += f"    source axon: {self.axon_name}\n"
        s += f"    source layer: {self.layer}\n"
        s += f"    type: {self.synapse_fn}\n"
        s += f"    params: {self.params}\n"
        s += f"    action: {self.action_fn}\n"
        s += f"    action params: {self.action_params}\n"
        s += f"    spike history: {self.spike_history}\n"
        return s


