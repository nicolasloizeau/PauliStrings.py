Constructing Operators
======================

Start by importing the PauliStrings module:

.. code-block:: python

    import paulistrings as ps

To construct an operator, first declare an empty operator for :math:`N` qubits:

.. code-block:: python

    H = ps.Operator(N)


.. note::

    ``paulistrings`` supports up to 64 qubits.

You can add a term of the form :math:`J X_i` by doing:

.. code-block:: python

    H += J, "X", i

and a term of the form :math:`J X_i X_j` by doing:

.. code-block:: python

    H += J, "X", i, "X", j

Similarly, to add a term of the form :math:`J X_i X_j X_k`:

.. code-block:: python

    H += J, "X", i, "X", j, "X", k

etc.



1D Transverse Ising Model
-------------------------

Let's construct the Hamiltonian of a `1D transverse Ising model <https://en.wikipedia.org/wiki/Transverse-field_Ising_model>`_:

.. math::

    H = -J \left( \sum_{\langle i,j \rangle} Z_i Z_j + g \sum_i X_i \right)

Here is a Python function to build the Hamiltonian for a 1D transverse Ising model with periodic boundary conditions:

.. code-block:: python

    import paulistrings as ps

    def ising1D(N, J, g):
        H = ps.Operator(N)
        for j in range(N - 1):
            H += "Z", j, "Z", j + 1
        H += "Z", 0, "Z", N - 1  # periodic boundary condition
        for j in range(N):
            H += g, "X", j
        return -J * H

.. note::

    In Python, qubit indices start at 0 (unlike Julia, which starts at 1).

Operators can be printed in string format using the ``print`` function:

.. code-block:: python

    print(ising1D(3, 1, 0.5))
