

from .operators import Operator

def operator_from_dict(d, N):
    o = Operator(N)
    o.strings = list(d.keys())
    o.coeffs = list(d.values())
    return o


def add(o1:Operator, o2:Operator):
    assert o1.N == o2.N, "Operators must have the same number of qubits"
    d = dict(zip(o1.strings, o1.coeffs))
    for s, c in zip(o2.strings, o2.coeffs):
        if s in d:
            d[s] += c
        else:
            d[s] = c
    return operator_from_dict(d, o1.N)
