

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



def prod(p1:tuple,p2:tuple):
    v = p1[0] ^ p2[0]
    w = p1[1] ^ p2[1]
    k = 1 - (((p1[0] & p2[1]).bit_count() & 1) << 1)
    return (v, w), k

def comm(p1:tuple, p2:tuple):
    v = p1[0] ^ p2[0]
    w = p1[1] ^ p2[1]
    k = (((p2[0] & p1[1]).bit_count() & 1) << 1) - (((p1[0] & p2[1]).bit_count() & 1) << 1)
    return (v, w), k

def anticomm(p1:tuple, p2:tuple):
    v = p1[0] ^ p2[0]
    w = p1[1] ^ p2[1]
    k = 2- (((p1[0] & p2[1]).bit_count() & 1) << 1) + (((p1[1] & p2[0]).bit_count() & 1) << 1)
    return (v, w), k

def binary_kernel(f, o1:Operator, o2:Operator):
    assert o1.N == o2.N, "Operators must have the same number of qubits"
    d = {}
    for (s1, c1) in zip(o1.strings, o1.coeffs):
        for (s2, c2) in zip(o2.strings, o2.coeffs):
            p, k = f(s1, s2)
            c = c1 * c2 * k
            if p in d:
                d[p] += c
            else:
                d[p] = c
    return operator_from_dict(d, o1.N)

def mul(o1:Operator, o2:Operator):
    return binary_kernel(prod, o1, o2)

def commutator(o1:Operator, o2:Operator):
    return binary_kernel(comm, o1, o2)

def anticommutator(o1:Operator, o2:Operator):
    return binary_kernel(anticomm, o1, o2)
