#!/usr/bin/env python
import pytest
import random
import numpy as np
from numpy.linalg import norm
from paulistrings import *


def test_k_local_part():
    N = 4
    a = rand_local2(N)
    b = rand_local1(N)
    o = a * b
    o1 = k_local_part(o, 1)
    o2 = k_local_part(o, 2)
    o3 = k_local_part(o, 3)
    assert opnorm(o - (o1 + o2 + o3)) < 1e-10


def test_truncate():
    N = 4
    a = rand_local2(N)
    b = rand_local1(N)
    o = a * b
    assert opnorm(o) > opnorm(truncate(o, 2))


def test_cutoff():
    o1 = Operator(4)
    o1 += 5, "XXYY"
    o1 += 2, "1X11"
    o1 += 3, "111Y"
    o1 += 5, "11Y1"
    o1 += 6, "Z111"
    o2 = Operator(4)
    o2 += 5, "XXYY"
    o2 += 5, "11Y1"
    o2 += 6, "Z111"
    assert opnorm(o2 - cutoff(o1, 4)) == 0


def test_trim():
    o1 = Operator(4)
    o1 += 5, "XXYY"
    o1 += 2, "1X11"
    o1 += 3, "111Y"
    o1 += 5, "11Y1"
    o1 += 6, "Z111"
    o2 = Operator(4)
    o2 += 5, "XXYY"
    o2 += 5, "11Y1"
    o2 += 6, "Z111"
    assert opnorm(o2 - trim(o1, 3)) == 0
