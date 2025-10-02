from .operators import Operator
import random
from itertools import product




def rand_local2(N:int):
    """
    Random 2-local operator of N qubits.
    """
    o = Operator(N)
    for i, j in product(range(N), range(N)):
        if i != j:
            for k, l in product(['X', 'Y', 'Z'], repeat=2):
                o += random.gauss(0, 1), k, i, l, j
    return o


def rand_local1(N:int):
    """
    Random 1-local operator of N qubits.
    """
    o = Operator(N)
    for i in range(N):
        for k in ['X', 'Y', 'Z']:
            o += random.gauss(0, 1), k, i
    return o
