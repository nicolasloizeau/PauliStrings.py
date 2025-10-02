from .operators import Operator
from .operations import *


def cutoff(o: Operator, epsilon: float):
    """Remove all terms with weight < epsilon."""
    strings = []
    coeffs = []
    for s, c in zip(o.strings, o.coeffs):
        if abs(c) >= epsilon:
            strings.append(s)
            coeffs.append(c)
    return new_operator(o.N, strings, coeffs)


def truncate(o: Operator, max_length: int) -> Operator:
    """Remove all terms with Pauli lenght > max_length."""
    filtered_strings = []
    filtered_coeffs = []
    for string, coeff in zip(o.strings, o.coeffs):
        if pauli_weight(string) <= max_length:
            filtered_strings.append(string)
            filtered_coeffs.append(coeff)
    o2 = Operator(o.N)
    o2.strings = np.array(filtered_strings)
    o2.coeffs = np.array(filtered_coeffs)
    return o2


def k_local_part(o: Operator, k: int, atmost: bool = False) -> Operator:
    """
    Return the k-local part of an operator (terms with exactly k or at-most k non-unit Paulis).
    """
    filtered_strings = []
    filtered_coeffs = []
    for string, coeff in zip(o.strings, o.coeffs):
        weight = pauli_weight(string)
        if weight == k or (atmost and weight <= k):
            filtered_strings.append(string)
            filtered_coeffs.append(coeff)
    o2 = Operator(o.N)
    o2.strings = np.array(filtered_strings)
    o2.coeffs = np.array(filtered_coeffs)
    return o2


def trim(o: Operator, nterms: int, keep: Operator = None) -> Operator:
    """Keep the nterms Pauli terms with largest absolute coefficients.
    If keep is provided, ensure that all terms in keep are included in the output operator.
    """
    if keep is None:
        keep = Operator(0)

    # If operator already has fewer strings than max_strings, return a copy
    if len(o.strings) <= nterms:
        o2 = Operator(o.N)
        o2.strings = np.copy(o.strings)
        o2.coeffs = np.copy(o.coeffs)
        return o2

    # Get indices of the largest coefficients by absolute value
    coeff_abs = np.abs(o.coeffs)
    indices = np.argsort(coeff_abs)[-nterms:]  # Get indices of max_strings largest values

    # Add strings from keep operator if they exist in o but weren't selected
    if len(keep.strings) > 0:
        for keep_string in keep.strings:
            # Find if the keep_string exists in o.strings
            matches = np.all(o.strings == keep_string, axis=1)
            if np.any(matches):
                idx = np.where(matches)[0][0]
                if idx not in indices:
                    indices = np.append(indices, idx)

    # Create new trimmed operator
    o2 = Operator(o.N)
    o2.strings = o.strings[indices]
    o2.coeffs = o.coeffs[indices]

    return o2


def add_noise(o: Operator, g: float) -> Operator:
    """Add depolarizing noise that make the long string decays.
    g is the noise amplitude. Each string is multiplied by exp(-g * w), where w is the number of non-identity Paulis in the string.
    """

    # Create new operator
    o2 = Operator(o.N)
    o2.strings = np.copy(o.strings)
    o2.coeffs = np.copy(o.coeffs)
    # Apply noise to each coefficient based on its Pauli weight
    for i in range(len(o2.strings)):
        weight = pauli_weight(o2.strings[i])
        o2.coeffs[i] *= np.exp(-weight * g)
    return o2
