from .operators import Operator
from .operations import *
from . import cpp_operations



def trace_product(o1: Operator, o2: Operator):
    """equivalent to trace(o1*o2) but faster"""
    assert o1.N == o2.N
    return cpp_operations.trace_product(cpp_operator(o1), cpp_operator(o2)) * 2**o1.N


def trace_product_power(A: Operator, k: int, B: Operator, l: int):
    """equivalent to trace(A**k * B**l) but faster"""
    assert type(A) == type(B)
    m = (k + l) // 2
    n = k + l - m

    if k < m:
        C = (A ** k) * (B ** (m - k))
        D = B ** n
    elif k > m:
        C = A ** m
        D = (A ** (k - m)) * (B ** l)
    else:
        C = A ** k
        D = B ** l

    return trace_product(C, D)

def power_by_squaring(o:Operator, n):
    assert n >= 0
    if n == 0:
        return identity(o.N)
    elif n == 1:
        return o
    elif n % 2 == 0:
        return power_by_squaring(o * o, n // 2)
    else:
        return o * power_by_squaring(o * o, (n - 1) // 2)
