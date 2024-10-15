"""Parse simple SDB."""
# Author: Garry Morrison
# Created: 2024-10-15
# Updated: 2024-10-15

from .trigger_fn import trigger_list_simm_threshold
from .pooling_fn import pooling_or
from .synapse_fn import synapse_identity
from .action_fn import action_println


def parse_ket(s, synapse_number=None):
    """Parse a SDB ket."""
    s = s.strip()
    s = s.rstrip('>')
    coeff_str, label = s.split('|')
    if len(label) == 0: # detected an empty ket
        return 1, ''
    try:
        coeff = float(coeff_str)
    except ValueError:
        coeff = 1
    if synapse_number is None:
        return coeff, label
    return coeff, f"{label} S{synapse_number}"

def parse_sp(s, synapse_number=None): # superpositions do not require synapse numbers.
    """Parse a SDB superposition."""
    kets = [parse_ket(x, synapse_number) for x in s.split(' + ')]
    coeffs = [x[0] for x in kets]
    labels = [x[1] for x in kets]
    return coeffs, labels

def parse_seq(s, synapse_number): # sequences require synapse numbers.
    """Parse a SDB sequence."""
    sps = [parse_sp(x, synapse_number) for x in s.split(' . ')]
    full_coeffs = []
    full_labels = []
    for k in range(len(sps)):
        delay = len(sps) - k - 1
        coeffs, labels = sps[k]
        # delay_labels = [f"{x} D{delay}" for x in labels if len(x) > 0]
        # full_coeffs += coeffs
        # full_labels += delay_labels
        for idx in range(len(labels)): # handle empty ket's in sequences, is there a cleaner way?
            if len(labels[idx]) == 0:
                continue
            full_coeffs.append(coeffs[idx])
            full_labels.append(f"{labels[idx]} D{delay}")
    return full_coeffs, full_labels

def parse_learn_rule(s):
    """Parse a simple SDB learn rule."""
    op_ket, seq = s.split(" => ")
    op, ket =  op_ket.split(" ", 1)
    return op, ket, seq

def parse_if_then_machine(NM, s, verbose=False):
    """Parse if-then machines in the given string and store them in the given neural module."""
    pattern_op = "pattern"
    then_op = "then"
    threshold = 0.98

    layer = 0 # hard code in the layer number for now
    synapse_number = 0 # hard code in the synapse number for now

    trigger_fn = trigger_list_simm_threshold
    trigger_params = {'threshold': threshold}

    pooling_fn = pooling_or
    pooling_params = {}

    synapse_fn = synapse_identity
    synapse_params = {'sign': 1}

    action_fn = action_println
    action_params = {'s': 'some string'}

    for line in s.splitlines():
        line = line.strip()
        if len(line) == 0 or line.startswith('--'):
            continue
        # print("line:", line)
        try:
            operator, ket, seq = parse_learn_rule(line)
        except:
            continue
        if not ket.startswith('|') or not ket.endswith('>'):
            print(f"invalid ket: {ket}") # wrap in `if verbose` too? Or should it raise an exception?
            continue
        label = ket[1:-1]
        name, pattern_no_str = label.rsplit(": ", 1) # do something with `pattern_no_str`??
        if verbose:
            print(f"Found a learn rule:\n    name: {name}\n    operator: {operator}\n    ket: {ket}\n    seq: {seq}\n")
        if operator == pattern_op:
            if verbose:
                print("found an if-then machine pattern rule")
            coeffs, labels = parse_seq(seq, synapse_number=synapse_number)
            if not NM.do_you_know_neuron(name):
                if verbose:
                    print(f"Unknown neuron \"{name}\", adding a new one to our module.\n")
                NM.add_neuron(name, layer, coeffs, labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
            else:
                if verbose:
                    print(f"Appending pattern to neuron \"{name}\"\n")
                NM.append_neuron_pattern(name, coeffs, labels, trigger_fn, trigger_params)
        if operator == then_op:
            if verbose:
                print("found an if-then machine then rule\n") # check the pattern_no_str == `*`?
            synapse_name = f"{name} S0"
            NM.add_synapse(synapse_name, name, synapse_fn, synapse_params, action_fn, {'s': seq} )
            NM.patch_in_new_synapses()
    return NM

# add_neuron(self, name, layer, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
# append_neuron_pattern(self, name, seed_pattern, synapse_labels, trigger_fn, trigger_params)
# add_synapse(self, name, axon_name, synapse_fn_type, params, synapse_action_type, action_params)
