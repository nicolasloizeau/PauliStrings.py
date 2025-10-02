from . import inout
import numbers
import numpy as np


class Operator:
    def __init__(self, N):
        self.N = N
        self.strings = []
        self.coeffs = []

    def add_string_uv(self, u: int, v: int, coeff: complex):
        self.strings.append((u, v))
        self.coeffs.append(coeff)

    def add_string_str(self, s: str, coeff: complex):
        u, v, phase = inout.string_to_vw(s)
        c = coeff * phase
        self.add_string_uv(u, v, c)

    def __add__(self, other):
        """
        Add another object to this operator.

        Parameters
        ----------
        other : str, tuple, Operator, or number
            The object to add to this operator:
              - str: a Pauli string to add with coefficient 1
              - tuple: a Pauli string and coefficient
              - Operator: another Operator instance
              - number: identity operator times a constant

        Returns
        -------
        Operator
            A new operator representing the sum.

        Raises
        ------
        TypeError
            If other cannot be added to an operator
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
            c, s = inout.local_term_to_str(other, self.N)
            o2 = Operator(self.N)
            o2.add_string_str(s, c)
            return self + o2
        elif isinstance(other, Operator):
            from . import operations

            return operations.add(self, other)
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

        Parameters
        ----------
        other : str, tuple, Operator, or number
            The object to subtract from this operator:
              - str: a Pauli string to subtract with coefficient 1
              - tuple: a Pauli string and coefficient
              - Operator: another Operator instance
              - number: identity operator times a constant

        Returns
        -------
        Operator
            A new operator representing the difference.

        Raises
        ------
        TypeError
            If other cannot be subtracted from an operator
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

        Parameters
        ----------
        other : Operator or scalar
            The object to multiply this operator by.

        Returns
        -------
        Operator
            A new Operator representing the product.

        """
        from . import operations

        if isinstance(other, numbers.Number):
            O = Operator(self.N)
            O.strings = self.strings.copy()
            O.coeffs = np.array(self.coeffs) * other
            return O
        elif isinstance(other, Operator):
            return operations.multiply(self, other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        """
        Divide this operator by a scalar.

        Parameters
        ----------
        other : scalar
            The number to divide this operator by.

        Returns
        -------
        Operator
            A new Operator representing the quotient.

        Raises
        ------
        TypeError
            If other is not a number
        ZeroDivisionError
            If other is zero
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
        return inout.operator_to_string(self)

    def __pow__(self, exponent):
        from . import moments
        return moments.power_by_squaring(self, exponent)


def identity(N):
    """Return the identity operator on N qubits."""
    o = Operator(N)
    o.strings = [(0, 0)]
    o.coeffs = [1.0]
    return o
