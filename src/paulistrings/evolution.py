
from .operators import Operator
from .operations import *
from .truncation import trim


def f_unitary(H, O, s, hbar):
    """
    Compute the generator for unitary evolution: s * [H, O] / hbar
    """
    return s * commutator(H, O) / hbar


def rk4(H, O, dt, hbar=1.0, heisenberg=True, M=2**20, keep=None):
    """
    Single step of Runge–Kutta-4 with time-independent Hamiltonian.
    Returns O(t+dt).

    Parameters
    ----------
    H : Operator
        Hamiltonian
    O : Operator
        Observable or density matrix
    dt : float
        Time step
    hbar : float, optional
        Planck constant (default 1)
    heisenberg : bool, optional
        If True, evolve in Heisenberg picture (default True)
    M : int, optional
        Number of strings to keep (default 2**20)
    keep : Operator, optional
        Strings to always keep (default: identity operator)

    Returns
    -------
    Operator
        The evolved operator O(t+dt)
    """
    dt = float(dt)
    if keep is None:
        keep = Operator(O.N)
    s = 1j if heisenberg else -1j
    k1 = f_unitary(H, O, s, hbar)
    k1 = trim(k1, M, keep=keep)
    k2 = f_unitary(H, O + dt * k1 / 2, s, hbar)
    k2 = trim(k2, M, keep=keep)
    k3 = f_unitary(H, O + dt * k2 / 2, s, hbar)
    k3 = trim(k3, M, keep=keep)
    k4 = f_unitary(H, O + dt * k3, s, hbar)
    k4 = trim(k4, M, keep=keep)
    return O + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6
