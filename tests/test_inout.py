#!/usr/bin/env python
import pytest
import random

from paulistrings import *
from paulistrings.random import rand_local2


def random_string(length):
    pauli_chars = ["1", "X", "Y", "Z"]
    return "".join(random.choice(pauli_chars) for _ in range(length))


def test_print():
    N = 4
    o = Operator(N)
    o += 1.2, "X1YZ"
    o += 0.5, "ZZZZ"
    o += 3, "Y111"
    s = """(3.0 + 0.0j) Y111\n(1.2 + 0.0j) X1YZ\n(0.5 + 0.0j) ZZZZ\n"""
    assert str(o) == s
