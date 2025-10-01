
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <complex>
#include <sys/types.h>
#include "types.hpp"


// Convert Operator to unordered_map
Dict operator_to_map(const Operator& op) {
    auto strings = op.first.unchecked<2>();   // shape (N,2)
    auto coeffs = op.second.unchecked<1>();
    ssize_t N = strings.shape(0);

    Dict d;
    for (ssize_t i = 0; i < N; i++) {
        d[{strings(i,0), strings(i,1)}] = coeffs(i);
    }
    return d;
}

// Convert map back to Operator
Operator operator_from_map(const Dict d) {
    ssize_t N = d.size();
    UInt strings_out(std::vector<ssize_t>{N,2});
    Complex coeffs_out(std::vector<ssize_t>{N});

    auto s_out = strings_out.mutable_unchecked<2>();
    auto c_out = coeffs_out.mutable_unchecked<1>();

    ssize_t idx = 0;
    for (const auto& kv : d) {
        s_out(idx,0) = kv.first.first;
        s_out(idx,1) = kv.first.second;
        c_out(idx) = kv.second;
        idx++;
    }

    return {strings_out, coeffs_out};
}

// Add two Operators
Operator add(const Operator& o1, const Operator& o2) {
    auto d = operator_to_map(o1);

    // o2: accumulate coefficients
    auto strings2 = o2.first.unchecked<2>();
    auto coeffs2 = o2.second.unchecked<1>();
    ssize_t N2 = strings2.shape(0);

    for (ssize_t i = 0; i < N2; i++) {
        std::pair<uint64_t,uint64_t> key{strings2(i,0), strings2(i,1)};
        d[key] += coeffs2(i);  // adds if exists, or initializes to value
    }

    return operator_from_map(d);
}

PYBIND11_MODULE(cpp_operations, m) {
    m.doc() = "C++ operations for pauli strings operators";
    m.def("add", &add, "Addition");
}
