from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import sys
import setuptools


import pybind11

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

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
    version="0.1.1",
    description="Quantum many body simulations with Pauli strings",
    long_description=long_description,
    long_description_content_type="text/x-rst",
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
    url="https://github.com/nicolasloizeau/PauliStrings.py",
)
