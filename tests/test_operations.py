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
o_sum = Operator(4)
o_sum += 5, "XXYY"
o_sum += 2, "1X11"
o_sum += 3, "111Y"
o_sum += 5, "11Y1"
o_sum += 6, "Z111"
o_diff = Operator(4)
o_diff -= 3, "XXYY"
o_diff += 2, "1X11"
o_diff += 3, "111Y"
o_diff -= 5, "11Y1"
o_diff -= 6, "Z111"


def test_add():
    o3 = o1 + o2
    assert o3.N == 4
    assert opnorm(o_sum - o3) == 0


def test_sub():
    o3 = o1 - o2
    assert o3.N == 4
    assert opnorm(o_diff - o3) == 0


def test_opnorm():
    assert abs(opnorm(o1) - np.sqrt(trace(o1 * dagger(o1)))) < 1e-10


def test_trace():
    c = random.random()
    assert trace(o1 + c) == c * 2**o1.N


def test_dagger():
    o = rand_local2(4)
    assert opnorm(dagger(dagger(o)) - o) < 1e-10

def test_identity():
    o = identity(4)
    assert o.N == 4
    assert len(o.strings) == 1
    assert trace(o) == 2**4

def test_product_np():
    t = np.linspace(0, 1, 5)
    s = 0
    for ti in t:
        s += trace(ti*o1)
    assert s==0


def test_commutator():
    a = rand_local2(4)
    b = rand_local2(4)
    c = commutator(a, b)
    d = a * b - b * a
    assert opnorm(c - d) < 1e-10
    a = Operator(4)
    a += 1, "X", 0
    b = Operator(4)
    b += 1, "Y", 0
    c = commutator(a, b)
    d = a * b - b * a
    assert opnorm(c - d) < 1e-10

def test_trivial():
    o1 = Operator(4)
    o2 = Operator(4)
    o3 = rand_local2(4)
    assert trace(o1*o2) == 0
    assert opnorm(o1) == 0
    assert opnorm(o2) == 0
    assert opnorm(o1+o2) == 0
    assert opnorm(o1*o3) == 0
    assert opnorm(o2*o3) == 0
    assert opnorm(o1-o2) == 0
    assert opnorm(commutator(o1,o2)) == 0
