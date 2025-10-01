from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import sys
import setuptools


import pybind11


ext_modules = [
    Extension(
        "paulistrings.cpp_operations",
        ["src/paulistrings/cpp/operations.cpp"],
        include_dirs=[
            pybind11.get_include(),
        ],
        language="c++",
    ),
]

setup(
    name="paulistrings",
    version="0.1.0",
    description="Quantum many body simulations with Pauli strings",
    author="Nicolas Loizeau",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    install_requires=[
        "numpy",
        "pybind11",
    ],
    zip_safe=False,
)
