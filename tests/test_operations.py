#!/usr/bin/env python
import pytest
import random
import numpy as np
from numpy.linalg import norm

from paulistrings import *


o1 = Operator(4)
o1 += 1, "XXYY"
o1 += 2, "X", 1
o1 += 3, "Y", 3
o2 = Operator(4)
o2 += 4, "XXYY"
o2 += 5, "Y", 2
o2 += 6, "Z", 0


def test_add():
    o3 = o1+o2
    assert o3.N == 4
    assert o3.strings == [(12, 15), (0, 2), (8, 8), (4, 4), (1, 0)]
    assert o3.coeffs == [(-5+0j), (2+0j), 3j, 5j, (6+0j)]


def test_sub():
    o3 = o1-o2
    assert o3.N == 4
    assert o3.strings == [(12, 15), (0, 2), (8, 8), (4, 4), (1, 0)]
    assert o3.coeffs == [(3+0j), (2+0j), 3j, (-0-5j), (-6-0j)]
