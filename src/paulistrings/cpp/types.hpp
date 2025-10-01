// types.hpp
#pragma once

#include <pybind11/numpy.h>
#include <complex>
#include <utility>
#include <unordered_map>

namespace py = pybind11;

// a list of pairs of uint64 representing Pauli strings
using UInt = py::array_t<uint64_t, py::array::c_style | py::array::forcecast>;

// a list of complex coefficients
using Complex = py::array_t<std::complex<double>, py::array::c_style | py::array::forcecast>;

// An operator is represented as a pair (strings, coeffs)
using Operator = std::pair<UInt, Complex>;

using String = std::pair<uint64_t,uint64_t>;

// Hash for a pair of uint64_t
struct PairHash {
    std::size_t operator()(const String& p) const {
        return std::hash<uint64_t>{}(p.first) ^ (std::hash<uint64_t>{}(p.second) << 1);
    }
};

// A Pauli strings dictionary: keys are pairs of uint64 (the strings), values are complex coefficients
using Dict = std::unordered_map<String, std::complex<double>, PairHash>;
