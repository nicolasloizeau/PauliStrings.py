#!/usr/bin/env python
import pytest
import random

from paulistrings import *



def random_string(length):
    pauli_chars = ['1', 'X', 'Y', 'Z']
    return ''.join(random.choice(pauli_chars) for _ in range(length))

def test_print():
    N = 4
    M = 20
    o = Operator(N)
    coeffs = [random.randint(1, 10) for _ in range(M)]
    strings = [random_string(N) for _ in range(M)]
    for k in range(M):
        o += (coeffs[k], strings[k])
    output = str(o)
    output = output.replace("-0j", "+0j")
    expected_output = ""
    for k in range(M):
        coeff = coeffs[k]
        string = strings[k]
        expected_output += f"({coeff}+0j) {string}\n"
    assert output == expected_output
