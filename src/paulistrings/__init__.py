"""Top-level package for PauliStrings.py."""

__author__ = """Nicolas Loizeau"""
__email__ = "nicolasloizeau@gmail.com"
__version__ = "0.1.0"


__all__ = [
    # From operators
    "Operator",
    "identity",
    "copy",
    # From operations
    "commutator",
    "anticommutator",
    "multiply_cpp",
    "add",
    "multiply",
    "opnorm",
    "trace",
    "add_cpp",
    "commutator_cpp",
    "dagger",
    # From truncation
    "truncate",
    "k_local_part",
    "trim",
    "add_noise",
    "cutoff",
    # From random
    "rand_local1",
    "rand_local2",
    # From moments
    "trace_product",
    "trace_product_power",
    # From inout
    "todense",
    # From evolution
    "rk4"
]


from .operators import *
from .operations import commutator, anticommutator, add, multiply, opnorm, trace, dagger
from .operations import multiply_cpp, add_cpp, commutator_cpp
from .random import rand_local1, rand_local2
from .truncation import truncate, k_local_part, trim, add_noise, cutoff
from .moments import trace_product, trace_product_power
from .inout import todense
from .evolution import rk4
