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
        extra_compile_args=["-O3"],
        language="c++",
    ),
]

setup(
    name="paulistrings",
    version="1.0.0",
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
    classifiers=[
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Quantum Computing",
        "Intended Audience :: Science/Research",
    ],
    zip_safe=False,
)
