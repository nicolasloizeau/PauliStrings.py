import pytest
import random
import numpy as np
from numpy.linalg import norm
from paulistrings import *


def test_trace_product():
    N = 4
    o1 = rand_local2(N)
    o2 = rand_local2(N)
    assert abs(trace_product(o1, o2) - trace(o1*o2)) < 1e-10
    assert abs(trace_product_power(o1, 2, o2, 2) - trace(o1**2*o2**2)) < 1e-10
    o = Operator(4)
    assert trace_product(o, o) == 0

def test_pow():
    o = rand_local2(4)
    assert opnorm(o*o*o - o**3) < 1e-10
    assert opnorm(o*o*o*o - o**4) < 1e-8
    o = Operator(4)
    assert opnorm(o**4) == 0
