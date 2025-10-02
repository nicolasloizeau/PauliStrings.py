
import numbers
import numpy as np



class Operator:
    __array_priority__ = 1000 # to ensure that numpy operations call our methods
    def __init__(self, N):
        self.N = N
        self.strings = np.empty((0, 2))
        self.coeffs = np.empty(0, dtype=complex)

    def add_string_uv(self, u: int, v: int, coeff: complex):
        if len(self.strings) == 0:
            self.strings = np.array([(u, v)], dtype=np.uint64)
            self.coeffs = np.array([coeff])
        else:
            self.strings = np.vstack((np.array(self.strings), np.array((u, v))))
            self.coeffs = np.append(np.array(self.coeffs), coeff)


    def add_string_str(self, s: str, coeff: complex):
        from . import inout
        u, v, phase = inout.string_to_vw(s)
        c = coeff * phase
        self.add_string_uv(u, v, c)

    def __add__(self, other):
        """
        Add another object to this operator.
        other can be a string, a tuple (string, coeff), another Operator, or a number (will add identity times other).
        """
        if isinstance(other, str):
            self.add_string_str(other, 1)
            return self
        elif (
            isinstance(other, tuple)
            and len(other) == 2
            and isinstance(other[0], numbers.Number)
            and isinstance(other[1], str)
        ):
            o2 = Operator(self.N)
            o2.add_string_str(other[1], other[0])
            return self + o2
        elif isinstance(other, tuple):
            from . import inout
            c, s = inout.local_term_to_str(other, self.N)
            o2 = Operator(self.N)
            o2.add_string_str(s, c)
            return self + o2
        elif isinstance(other, Operator):
            from . import operations

            return operations.add_cpp(self, other)
        elif isinstance(other, numbers.Number):
            return self + identity(self.N) * other

        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Operator' and '{type(other).__name__}'")

    def __neg__(self):
        O = Operator(self.N)
        O.strings = self.strings.copy()
        O.coeffs = -np.array(self.coeffs)
        return O

    def __sub__(self, other):
        """
        Subtract another object from this operator.
        """
        if isinstance(other, Operator):
            return self + -other
        elif isinstance(other, str):
            self.add_string_str(other, -1)
            return self
        elif isinstance(other, tuple):
            O = Operator(self.N)
            O += other
            return self + -O
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Operator' and '{type(other).__name__}'")

    def __mul__(self, other):
        """
        Multiply this operator by another object.
        Other can be a scalar or another Operator.
        """
        from . import operations

        if isinstance(other, numbers.Number):
            O = Operator(self.N)
            O.strings = self.strings.copy()
            O.coeffs = np.array(self.coeffs) * other
            return O
        elif isinstance(other, Operator):
            return operations.multiply_cpp(self, other)
        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Operator' and '{type(other).__name__}'")

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        """
        Divide this operator by a scalar.
        """
        if isinstance(other, numbers.Number):
            if other == 0:
                raise ZeroDivisionError("Division by zero")
            O = Operator(self.N)
            O.strings = self.strings.copy()
            O.coeffs = np.array(self.coeffs) / other
            return O
        else:
            raise TypeError(f"unsupported operand type(s) for /: 'Operator' and '{type(other).__name__}'")

    def __str__(self):
        from . import inout
        return inout.operator_to_string(self)

    def __pow__(self, exponent):
        from . import moments
        return moments.power_by_squaring(self, exponent)

    def __array__(self):
        """Convert the operator to a dense numpy array: numpy.array(o)"""
        from . import inout
        return inout.todense(self)

    def __len__(self):
        return len(self.strings)


def identity(N):
    """Return the identity operator on N qubits."""
    o = Operator(N)
    o.strings = np.array([(0, 0)], dtype=np.uint64)
    o.coeffs = np.array([1.0])
    return o

def copy(o:Operator):
    """Return a copy of the operator."""
    O = Operator(o.N)
    O.strings = np.array(o.strings, dtype=np.uint64)
    O.coeffs = np.array(o.coeffs)
    return O
