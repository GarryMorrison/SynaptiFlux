"""Parse simple SDB."""
# Author: Garry Morrison
# Created: 2024-10-15
# Updated: 2024-10-18

from .trigger_fn import trigger_list_simm_threshold, trigger_fn_map
from .pooling_fn import pooling_or, pooling_fn_map
from .synapse_fn import synapse_identity, synapse_fn_map
from .action_fn import action_println, action_fn_map
from .misc import cast_value


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

def parse_sp_to_dict(s, cast_values=False):
    """Parse a superposition containing |key: value> pairs into a python dictionary."""
    sp_dict = {}
    for label in parse_sp(s, synapse_number=None)[-1]:
        try:
            key, value = label.split(': ', 1)
        except:
            continue
        if cast_values:
            value = cast_value(value)
        sp_dict[key] = value
    return sp_dict

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


def parse_traditional_if_then_machine(NM, s, verbose=False):
    """Parse traditional if-then machines in the given string and store them in the given neural module."""
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
    # return NM

# add_neuron(self, name, layer, seed_pattern, synapse_labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
# append_neuron_pattern(self, name, seed_pattern, synapse_labels, trigger_fn, trigger_params)
# add_synapse(self, name, axon_name, synapse_fn_type, params, synapse_action_type, action_params)

def process_functions(sp_dict, fn_key, fn_map):
    """Process a function."""
    try:
        fn_name = sp_dict[fn_key]
        fn = fn_map[fn_name]
    except:
        return None
    return fn

def process_if_then_machine_learn_rule(NM, name, operator, ket, seq, verbose=False):
    """Process a single if then machine learn rule."""
    if verbose:
        print(f"\nFound a learn rule:\n    name: {name}\n    operator: {operator}\n    ket: {ket}\n    seq: {seq}")
    sp_dict = parse_sp_to_dict(seq, cast_values=True)
    if operator == 'layer':
        try:
            layer = int(parse_ket(seq, synapse_number=None)[-1])
        except:
            layer = 0
        if verbose:
            print(f"layer: {layer}")
        NM.set_default_layer(layer)
    elif operator == 'trigger_fn':
        trigger_fn = process_functions(sp_dict, "trigger", trigger_fn_map)
        del sp_dict['trigger']
        if verbose:
            print(f"trigger_fn: {trigger_fn}")
            print(f"params: {sp_dict}")
        NM.set_default_trigger(trigger_fn, sp_dict)
    elif operator == 'pooling_fn':
        pooling_fn = process_functions(sp_dict, "pooling", pooling_fn_map)
        del sp_dict['pooling']
        if verbose:
            print(f"pooling_fn: {pooling_fn}")
            print(f"params: {sp_dict}")
        NM.set_default_pooling(pooling_fn, sp_dict)
    elif operator == 'synapse_fn':
        synapse_fn = process_functions(sp_dict, "synapse", synapse_fn_map)
        del sp_dict['synapse']
        if verbose:
            print(f"synapse_fn: {synapse_fn}")
            print(f"params: {sp_dict}")
        NM.set_default_synapse(synapse_fn, sp_dict)
    elif operator == 'action_fn':
        action_fn = process_functions(sp_dict, "action", action_fn_map)
        del sp_dict['action']
        if verbose:
            print(f"action_fn: {action_fn}")
            print(f"params: {sp_dict}")
        NM.set_default_action(action_fn, sp_dict)
    elif operator == 'pattern':
        # layer = 0 # hard code in the layer number for now
        layer = NM.get_default_layer() # use this for now
        synapse_number = 0 # hard code in the synapse number for now
        coeffs, labels = parse_seq(seq, synapse_number=synapse_number)
        if not NM.do_you_know_neuron(name):
            if verbose:
                print(f"Unknown neuron \"{name}\", adding a new neuron to our module.")
            # NM.add_neuron(name, layer, coeffs, labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
            NM.add_default_neuron(name, layer, coeffs, labels)
        else:
            if verbose:
                print(f"Appending pattern to neuron \"{name}\"")
            # NM.append_neuron_pattern(name, coeffs, labels, trigger_fn, trigger_params)
            NM.append_default_neuron_pattern(name, coeffs, labels)
    elif operator.startswith('then-'):
        try:
            synapse_number = int(operator[5:])
        except:
            synapse_number = 0
        if verbose:
            print("found an if-then machine then rule\n") # check the pattern_no_str == `*`?
        synapse_name = f"{name} S{synapse_number}"
        # NM.add_synapse(synapse_name, name, synapse_fn, synapse_params, action_fn, {'s': seq} )
        NM.add_default_synapse(synapse_name, name)
        NM.patch_in_new_synapses()
        if 'action' in sp_dict:
            # print('rule has an action')
            action_fn = process_functions(sp_dict, "action", action_fn_map)
            del sp_dict['action']
            if verbose:
                print(f"action_fn: {action_fn}")
                print(f"params: {sp_dict}")
            NM.update_synapse_action(synapse_name, action_fn, sp_dict)

def parse_if_then_machine(NM, s, verbose=False):
    """Parse if-then machines in the given string and store them in the given neural module."""
    inside_chunk = False
    chunk_name = ""
    for line in s.splitlines():
        line = line.strip()
        if len(line) == 0 or line.startswith('--'):
            continue
        # print("line:", line)
        if line.startswith('as |') and line.endswith('>:'): # detected a chunk
            inside_chunk = True
            chunk_name = line[3:-1]
            if verbose:
                print(f"\nDetected a chunk, with ket: \"{chunk_name}\"")
            continue
        if line == "end:": # detected the end of a chunk:
            inside_chunk = False
            if verbose:
                print(f"\nEnd of chunk: \"{chunk_name}\"\n")
            chunk_name = ""
            continue
        if inside_chunk:
            try:
                operator, seq = line.split(" => ")
                if not chunk_name.startswith('|') or not chunk_name.endswith('>'):
                    print(f"invalid chunk name: {chunk_name}") # wrap in `if verbose` too? Or should it raise an exception?
                    continue
                name = chunk_name[1:-1]
                process_if_then_machine_learn_rule(NM, name, operator, chunk_name, seq, verbose=verbose)
            except:
                continue
            continue
        try:
            operator, ket, seq = parse_learn_rule(line)
            if not ket.startswith('|') or not ket.endswith('>'):
                print(f"invalid ket: {ket}") # wrap in `if verbose` too? Or should it raise an exception?
                continue
            name = ket[1:-1]
            process_if_then_machine_learn_rule(NM, name, operator, ket, seq, verbose=verbose)
        except:
            continue
    # return NM


def parse_sf_if_then_machine(NM, s, verbose=False):
    """Parse if-then machines in the given string and store them in the given neural module."""
    inside_default_chunk = False
    inside_neuron_chunk = False
    inside_synapse_chunk = False
    chunk_name = ""
    for line in s.splitlines():
        line = line.strip()
        if len(line) == 0 or line.startswith('--'):
            continue
        # print("line:", line)
        if line == "as default:":
            inside_default_chunk = True
            if verbose:
                print("\nStart of a default chunk:")
            continue
        if line.startswith('as neuron |') and line.endswith('>:'): # detected a neuron chunk
            inside_neuron_chunk = True
            chunk_name = line[10:-1]
            if verbose:
                print(f"\nStart of a neuron chunk, with ket: \"{chunk_name}\":")
            continue
        if line.startswith('as synapse |') and line.endswith('>:'): # detected a neuron chunk
            inside_synapse_chunk = True
            chunk_name = line[11:-1]
            if verbose:
                print(f"\nStart of a synapse chunk, with ket: \"{chunk_name}\":")
            continue
        if line == "end:": # detected the end of a chunk:
            if verbose:
                print(f"\nEnd of chunk: \"{chunk_name}\"\n")
            inside_default_chunk = False
            inside_neuron_chunk = False
            inside_synapse_chunk = False
            chunk_name = ""
            continue
        operator, sp = line.split(" => ", 1)
        if inside_default_chunk:
            process_default_chunk_line(NM, operator, sp, verbose)
            continue
        elif inside_neuron_chunk:
            process_neuron_chunk_line(NM, chunk_name, operator, sp, verbose)
            continue
        elif inside_synapse_chunk:
            process_synapse_chunk_line(NM, chunk_name, operator, sp, verbose)
            continue
        continue

def process_default_chunk_line(NM, operator, sp, verbose=False):
    """Process a single line of a default chunk."""
    if verbose:
        print(f"\nChunk line:\n    operator: {operator}\n    sp: {sp}")
    if operator == 'layer':
        try:
            layer = int(parse_ket(sp, synapse_number=None)[-1])
        except:
            layer = 0
        if verbose:
            print("Parsed result:")
            print(f"    layer: {layer}")
        NM.set_default_layer(layer)
        return
    sp_dict = parse_sp_to_dict(sp, cast_values=True)
    if operator == 'trigger_fn':
        trigger_fn = process_functions(sp_dict, "trigger", trigger_fn_map)
        del sp_dict['trigger']
        if verbose:
            print("Parsed result:")
            print(f"    trigger_fn: {trigger_fn}")
            print(f"    params: {sp_dict}")
        NM.set_default_trigger(trigger_fn, sp_dict)
    elif operator == 'pooling_fn':
        pooling_fn = process_functions(sp_dict, "pooling", pooling_fn_map)
        del sp_dict['pooling']
        if verbose:
            print("Parsed result:")
            print(f"    pooling_fn: {pooling_fn}")
            print(f"    params: {sp_dict}")
        NM.set_default_pooling(pooling_fn, sp_dict)
    elif operator == 'synapse_fn':
        synapse_fn = process_functions(sp_dict, "synapse", synapse_fn_map)
        del sp_dict['synapse']
        if verbose:
            print("Parsed result:")
            print(f"    synapse_fn: {synapse_fn}")
            print(f"    params: {sp_dict}")
        NM.set_default_synapse(synapse_fn, sp_dict)
    elif operator == 'action_fn':
        action_fn = process_functions(sp_dict, "action", action_fn_map)
        del sp_dict['action']
        if verbose:
            print("Parsed result:")
            print(f"    action_fn: {action_fn}")
            print(f"    params: {sp_dict}")
        NM.set_default_action(action_fn, sp_dict)


def process_neuron_chunk_line(NM, chunk_name, operator, sp, verbose=False):
    """Process a single line of a neuron chunk."""
    if verbose:
        print(f"\nChunk line:\n    name: {chunk_name}\n    operator: {operator}\n    sp: {sp}")
    try:
        neuron_name = parse_ket(chunk_name)[-1]
    except:
        return
    if operator == 'pattern':
        # layer = 0 # hard code in the layer number for now
        layer = NM.get_default_layer() # use this for now
        synapse_number = 0 # hard code in the synapse number for now
        coeffs, labels = parse_seq(sp, synapse_number=synapse_number)
        if verbose:
            print(f"Parsed result:\n    coeffs: {coeffs}\n    labels: {labels}")
        if not NM.do_you_know_neuron(neuron_name):
            if verbose:
                print(f"Unknown neuron \"{neuron_name}\", adding a new neuron to our module.")
            # NM.add_neuron(name, layer, coeffs, labels, trigger_fn, trigger_params, pooling_fn, pooling_params)
            NM.add_default_neuron(neuron_name, layer, coeffs, labels)
        else:
            if verbose:
                print(f"Appending pattern to neuron \"{neuron_name}\"")
            # NM.append_neuron_pattern(name, coeffs, labels, trigger_fn, trigger_params)
            NM.append_default_neuron_pattern(neuron_name, coeffs, labels)

def process_synapse_chunk_line(NM, chunk_name, operator, sp, verbose=False):
    """Process a single line of a synapse chunk."""
    if verbose:
        print(f"\nChunk line:\n    name: {chunk_name}\n    operator: {operator}\n    sp: {sp}")
    try:
        synapse_name = parse_ket(chunk_name)[-1]
    except:
        return
    if operator == 'axon':
        try:
            # synapse_name = parse_ket(chunk_name)[-1]
            axon_name = parse_ket(sp)[-1]
            NM.add_default_synapse(synapse_name, axon_name)
            NM.patch_in_new_synapses()
            if verbose:
                print(f"Parsed result:\n    axon_name: {axon_name}")
        except:
            return
        return
    sp_dict = parse_sp_to_dict(sp, cast_values=True)
    if operator == 'synapse_fn':
        synapse_fn = process_functions(sp_dict, "synapse", synapse_fn_map)
        del sp_dict['synapse']
        if verbose:
            print("Parsed result:")
            print(f"    synapse_fn: {synapse_fn}")
            print(f"    params: {sp_dict}")
        NM.update_synapse_fn(synapse_name, synapse_fn, sp_dict)
    elif operator == 'action_fn':
        action_fn = process_functions(sp_dict, "action", action_fn_map)
        del sp_dict['action']
        if verbose:
            print("Parsed result:")
            print(f"    action_fn: {action_fn}")
            print(f"    params: {sp_dict}")
        NM.update_synapse_action(synapse_name, action_fn, sp_dict)
