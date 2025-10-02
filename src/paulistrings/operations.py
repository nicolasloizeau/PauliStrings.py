from .operators import Operator
from . import cpp_operations
import numpy as np
from hmac import new


def opnorm(o: Operator):
    """
    Frobenius norm of an operator
    """
    return np.linalg.norm(o.coeffs) * (2 ** (o.N / 2))


def trace(o: Operator):
    """
    Trace of an operator
    """
    return o.coeffs[np.all(o.strings == 0, axis=1)].sum() * 2**o.N


def operator_from_dict(d, N):
    o = Operator(N)
    o.strings = np.array(list(d.keys()), dtype=np.uint64)
    o.coeffs = np.array(list(d.values()))
    return o


def operator_to_dict(o: Operator):
    strings = [tuple(s) for s in o.strings]
    coeffs = o.coeffs
    return dict(zip(strings, coeffs))


def add(o1: Operator, o2: Operator):
    assert o1.N == o2.N, "Operators must have the same number of qubits"
    d = operator_to_dict(o1)
    for s, c in zip(o2.strings, o2.coeffs):
        s = tuple(s)
        if s in d:
            d[s] += c
        else:
            d[s] = c
    return operator_from_dict(d, o1.N)


def string_multiply(p1: tuple, p2: tuple):
    v = p1[0] ^ p2[0]
    w = p1[1] ^ p2[1]
    k = 1 - (((p1[0] & p2[1]).bit_count() & 1) << 1)
    return (v, w), k


def string_commutator(p1: tuple, p2: tuple):
    v = p1[0] ^ p2[0]
    w = p1[1] ^ p2[1]
    k = (((p2[0] & p1[1]).bit_count() & 1) << 1) - (((p1[0] & p2[1]).bit_count() & 1) << 1)
    return (v, w), k


def string_anticommutator(p1: tuple, p2: tuple):
    v = p1[0] ^ p2[0]
    w = p1[1] ^ p2[1]
    k = 2 - (((p1[0] & p2[1]).bit_count() & 1) << 1) + (((p1[1] & p2[0]).bit_count() & 1) << 1)
    return (v, w), k


def binary_kernel(f, o1: Operator, o2: Operator):
    assert o1.N == o2.N, "Operators must have the same number of qubits"
    d = {}
    for s1, c1 in zip(o1.strings, o1.coeffs):
        for s2, c2 in zip(o2.strings, o2.coeffs):
            p, k = f(s1, s2)
            c = c1 * c2 * k
            if p in d:
                d[p] += c
            else:
                d[p] = c
    return operator_from_dict(d, o1.N)


def multiply(o1: Operator, o2: Operator):
    return binary_kernel(string_multiply, o1, o2)


def commutator(o1: Operator, o2: Operator):
    strings, coeffs = cpp_operations.commutator(cpp_operator(o1), cpp_operator(o2))
    return new_operator(o1.N, strings, coeffs)


def anticommutator(o1: Operator, o2: Operator):
    strings, coeffs = cpp_operations.anticommutator(cpp_operator(o1), cpp_operator(o2))
    return new_operator(o1.N, strings, coeffs)


def cpp_operator(op):
    strings = np.array(op.strings, dtype=np.uint64)
    coeffs = np.array(op.coeffs, dtype=np.complex128)
    return (strings, coeffs)

def new_operator(N, strings, coeffs):
    o = Operator(N)
    o.strings = np.array(strings, dtype=np.uint64)
    o.coeffs = np.array(coeffs)
    return o

def multiply_cpp(o1: Operator, o2: Operator):
    if len(o1) == 0 or len(o2) == 0:
        return Operator(o1.N)
    strings, coeffs = cpp_operations.multiply(cpp_operator(o1), cpp_operator(o2))
    return new_operator(o1.N, strings, coeffs)


def commutator_cpp(o1: Operator, o2: Operator):
    strings, coeffs = cpp_operations.commutator(cpp_operator(o1), cpp_operator(o2))
    return new_operator(o1.N, strings, coeffs)


def add_cpp(o1: Operator, o2: Operator):
    if len(o1) == 0:
        return o2
    if len(o2) == 0:
        return o1
    strings, coeffs = cpp_operations.add(cpp_operator(o1), cpp_operator(o2))
    return new_operator(o1.N, strings, coeffs)


def pauli_weight(string):
    v, w = string
    return (v | w).bit_count()


def ycount(string: tuple) -> int:
    """Count the number of Y operators in a Pauli string."""
    v, w = string
    return (v & w).bit_count()


def dagger(o: Operator) -> Operator:
    """Hermitian conjugate (dagger) of an operator."""
    o2 = Operator(o.N)
    o2.strings = o.strings.copy()
    o2.coeffs = np.copy(o.coeffs)
    for i in range(len(o2.strings)):
        sign = 1 - ((ycount(o2.strings[i]) & 1) << 1)  # Computes 1 or -1 based on Y count
        o2.coeffs[i] = sign * np.conj(o2.coeffs[i])
    return o2
