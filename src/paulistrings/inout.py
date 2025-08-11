

def string_to_vw(pauli: str):
    """
    Convert a Pauli string ('X', 'Y', 'Z' characters) to binary vectors v and w.

    Args:
        pauli: String containing Pauli operators ('X', 'Y', 'Z')

    Returns:
        Tuple of two integers (v, w)
    """
    v = 0
    w = 0
    for k in range(len(pauli)):
        if pauli[k] == 'X':
            w += 2 ** k
        elif pauli[k] == 'Z':
            v += 2 ** k
        elif pauli[k] == 'Y':
            w += 2 ** k
            v += 2 ** k
    c = 1j**pauli.count("Y")
    return v, w, c


def bit(value, position):
    """Check if the bit at position is set (1-indexed)."""
    return (value & (1 << position)) != 0

def vw_to_string(v, w, N):
    """
    Convert binary vectors v and w to a Pauli string representation.

    Args:
        v: Unsigned integer representing first binary vector
        w: Unsigned integer representing second binary vector
        N: Length of the string to generate

    Returns:
        Tuple of (string, phase) where string is the Pauli representation
        and phase is a complex number
    """
    result_string = ""
    phase = complex(1, 0)
    for i in range(N):
        if not bit(v, i) and not bit(w, i):
            result_string += '1'
        elif not bit(v, i) and bit(w, i):
            result_string += 'X'
        elif bit(v, i) and not bit(w, i):
            result_string += 'Z'
        elif bit(v, i) and bit(w, i):
            result_string += 'Y'
            phase *= complex(0, 1)

    return result_string, phase


def local_term_to_str(term, N):
    """
    Convert something like (1, "X", 2, "Z", 3) to "11XZ" with coefficient 1.
    """
    coeff = 1
    if len(term)%2 == 1:
        coeff = term[0]
        term = term[1:]
    s = ["1"] * N
    for i in range(len(term)//2):
        symbol = term[2*i]
        index = term[2*i + 1]
        s[index] = symbol
    return coeff, s
