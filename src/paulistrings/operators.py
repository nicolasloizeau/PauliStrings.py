from . import inout
import numbers
import numpy as np


class Operator:
    def __init__(self, N):
        self.N = N
        self.strings = []
        self.coeffs = []

    def add_string_uv(self, u:int, v:int, coeff:complex):
        self.strings.append((u, v))
        self.coeffs.append(coeff)

    def add_string_str(self, s:str, coeff:complex):
        u,v,phase = inout.string_to_vw(s)
        c = coeff * phase
        self.add_string_uv(u,v, c)


    def __add__(self, other):
        if isinstance(other, str):
            self.add_string_str(other, 1)
            return self
        elif isinstance(other, tuple) and len(other) == 2 and isinstance(other[0], numbers.Number) and isinstance(other[1], str):
            self.add_string_str(other[1], other[0])
            return self
        elif isinstance(other, tuple):
            c, s = inout.local_term_to_str(other, self.N)
            self.add_string_str(s, c)
            return self
        elif isinstance(other, Operator):
            from . import operations
            return operations.add(self, other)
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Operator' and '{type(other).__name__}'")

    def __neg__(self):
        O = Operator(self.N)
        O.strings = self.strings.copy()
        O.coeffs = -np.array(self.coeffs)
        return O

    def __sub__(self, other):
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
            return operations.mul(self, other)

    def __rmul__(self, other):
        return self * other

    def __str__(self):
        s = ""
        for (u, v), coeff in zip(self.strings, self.coeffs):
            string, phase = inout.vw_to_string(u, v, self.N)
            s += f"{coeff/phase} {string}\n"
        return s
