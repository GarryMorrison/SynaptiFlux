"""Parse simple SDB."""
# Author: Garry Morrison
# Created: 2024-10-15
# Updated: 2024-10-15

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
