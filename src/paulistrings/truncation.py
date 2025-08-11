

from .operators import Operator

def cutoff(o:Operator, epsilon:float):
    """Remove all terms with weight < epsilon

    Parameters
    ----------
    o: Operator
        The input operator to filter.
    epsilon: float
        The cutoff threshold. Terms with coefficients whose
        absolute value is less than this will be removed.

    Returns
    --------
        Operator

    """
    o2 = Operator(o.N)
    for s, c in zip(o.strings, o.coeffs):
        if abs(c) >= epsilon:
            o2.strings.append(s)
            o2.coeffs.append(c)
    return o2
