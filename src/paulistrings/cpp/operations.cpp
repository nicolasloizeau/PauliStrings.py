
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <complex>
#include <sys/types.h>
#include "types.hpp"
#include <unordered_map>
#include <vector>


// Convert Operator to unordered_map
Dict operator_to_map(const Operator& op) {
    auto strings = op.first.unchecked<2>();
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



std::pair<String,int> string_multiply(const String& p1, const String& p2) {
    uint64_t v = p1.first ^ p2.first;
    uint64_t w = p1.second ^ p2.second;
    int k = 1 - (((__builtin_popcountll(p1.first & p2.second) & 1) << 1));
    return {{v,w}, k};
}

std::pair<String,int> string_commutator(const String& p1, const String& p2) {
    uint64_t v = p1.first ^ p2.first;
    uint64_t w = p1.second ^ p2.second;
    int k = (((__builtin_popcountll(p2.first & p1.second) & 1) << 1)
             - ((__builtin_popcountll(p1.first & p2.second) & 1) << 1));
    return {{v,w}, k};
}

std::pair<String,int> string_anticommutator(const String& p1, const String& p2) {
    uint64_t v = p1.first ^ p2.first;
    uint64_t w = p1.second ^ p2.second;
    int k = 2 - (((__builtin_popcountll(p1.first & p2.second) & 1) << 1))
              + (((__builtin_popcountll(p1.second & p2.first) & 1) << 1));
    return {{v,w}, k};
}

Operator binary_kernel(
    std::pair<String,int> (*f)(const String&, const String&),
    const Operator& o1,
    const Operator& o2
) {
    auto strings1 = o1.first.unchecked<2>();
    auto coeffs1 = o1.second.unchecked<1>();
    auto strings2 = o2.first.unchecked<2>();
    auto coeffs2 = o2.second.unchecked<1>();

    ssize_t N1 = strings1.shape(0);
    ssize_t N2 = strings2.shape(0);

    Dict d;

    for (ssize_t i = 0; i < N1; i++) {
        String p1{strings1(i,0), strings1(i,1)};
        std::complex<double> c1 = coeffs1(i);
        for (ssize_t j = 0; j < N2; j++) {
            String p2{strings2(j,0), strings2(j,1)};
            std::complex<double> c2 = coeffs2(j);
            auto [p, k] = f(p1,p2);
            d[p] += c1 * c2 * double(k);
        }
    }
    return operator_from_map(d);
}



Operator multiply(const Operator& o1, const Operator& o2) {
    return binary_kernel(string_multiply, o1, o2);
}

Operator commutator(const Operator& o1, const Operator& o2) {
    return binary_kernel(string_commutator, o1, o2);
}

Operator anticommutator(const Operator& o1, const Operator& o2) {
    return binary_kernel(string_anticommutator, o1, o2);
}


std::complex<double> trace_product(const Operator& o1, const Operator& o2) {
    auto strings1 = o1.first.unchecked<2>();
    auto coeffs1 = o1.second.unchecked<1>();
    auto strings2 = o2.first.unchecked<2>();
    auto coeffs2 = o2.second.unchecked<1>();

    ssize_t N1 = strings1.shape(0);
    ssize_t N2 = strings2.shape(0);

    // If o1 is smaller, swap
    if (N1 < N2) {
        return trace_product(o2, o1);
    }

    // Check lengths
    if (N1 != coeffs1.shape(0) || N2 != coeffs2.shape(0)) {
        throw std::runtime_error("strings and coefficients must have the same length");
    }

    Dict d = operator_to_map(o2);

    std::complex<double> tr = 0.0;
    for (ssize_t i = 0; i < N1; ++i) {
        String p1{strings1(i,0), strings1(i,1)};
        std::complex<double> c1 = coeffs1(i);
        auto it = d.find(p1);
        if (it == d.end()) continue; // skip if not found
        std::complex<double> c2 = it->second;
        auto [p, k] = string_multiply(p1, p1);
        tr += c1 * c2 * double(k);
    }

    return tr;
}





PYBIND11_MODULE(cpp_operations, m) {
    m.doc() = "C++ operations for pauli strings operators";
    m.def("add", &add, "Addition");
    m.def("multiply", &multiply, "Multiplication");
    m.def("commutator", &commutator, "Commutator");
    m.def("anticommutator", &anticommutator, "Anticommutator");
    m.def("trace_product", &trace_product, "Trace of a product");
}
