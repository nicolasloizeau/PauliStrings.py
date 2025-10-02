Getting started
================

Installation
-------------
Install from github::

    pip install git+https://github.com/nicolasloizeau/paulistrings.py.git


Creating Operators
-----------------

Import the library and initialize an operator of 4 qubits:

.. code-block:: python

    import paulistrings as ps
    H = ps.Operator(4)

Add Pauli strings to the operator:

.. code-block:: python

    H += "XYZ1"
    H += "1YZY"
    print(H)

.. code-block:: none

    (1.0 + 0.0j) XYZ1
    (1.0 + 0.0j) 1YZY

Add a Pauli string with a coefficient:

.. code-block:: python

    # Coefficients can be complex
    H = ps.Operator(4)
    H += -1.2, "XXXZ"

.. code-block:: none

    (1.0 + 0.0j) XYZ1
    (1.0 + 0.0j) 1YZY
    (-1.2 + 0.0j) XXXZ

Add a 2-qubit string coupling qubits i and j with X and Y:

.. code-block:: python

    i, j = 0, 2  # example qubit indices
    H += 2.0, "X", i, "Y", j  # with coefficient=2
    H += "X", i, "Y", j       # with coefficient=1

Add a 1-qubit string:

.. code-block:: python

    i = 1  # example qubit index
    H += 2.0, "Z", i  # with coefficient=2
    H += "Z", i # with coefficient=1


Basic Operations
-----------------
Operators support standard arithmetic operations with other operators and numbers:

.. code-block:: python

    # Multiplication
    H3 = H1 * H2

    # Addition and subtraction
    H3 = H1 + H2
    H3 = H1 - H2

    # Scalar operations
    H3 = H1 + 2  # Adding a scalar (equivalent to adding identity times scalar)
    H = 5 * H    # Multiply operator by a scalar

Common operations on operators:

.. code-block:: python

    # Trace of an operator
    trace = ps.trace(H)

    # Frobenius norm
    norm = ps.opnorm(H)

    # Number of terms in the operator
    num_terms = len(H)  # or len(H.coeffs)

    # Commutator [H1, H2] = H1*H2 - H2*H1
    # This is more efficient than computing H1*H2 - H2*H1 directly
    comm = ps.commutator(H1, H2)



Contributing, Contact
----------------------
Contributions are welcome! Feel free to open a pull request if you'd like to contribute code or documentation.
For bugs and feature requests, please [open an issue](https://github.com/nicolasloizeau/PauliStrings.py/issues).
For questions, you can either contact `nicolas.loizeau@nbi.ku.dk` or start a new [discussion](https://github.com/nicolasloizeau/PauliStrings.py/discussions) in the repository.


Citation
---------

.. code-block:: bibtex

    @Article{Loizeau2025,
    	title={{Quantum many-body simulations with PauliStrings.jl}},
    	author={Nicolas Loizeau and J. Clayton Peacock and Dries Sels},
    	journal={SciPost Phys. Codebases},
    	pages={54},
    	year={2025},
    	publisher={SciPost},
    	doi={10.21468/SciPostPhysCodeb.54},
    	url={https://scipost.org/10.21468/SciPostPhysCodeb.54},
    }

    @Article{Loizeau2025,
    	title={{Codebase release 1.5 for PauliStrings.jl}},
    	author={Nicolas Loizeau and J. Clayton Peacock and Dries Sels},
    	journal={SciPost Phys. Codebases},
    	pages={54-r1.5},
    	year={2025},
    	publisher={SciPost},
    	doi={10.21468/SciPostPhysCodeb.54-r1.5},
    	url={https://scipost.org/10.21468/SciPostPhysCodeb.54-r1.5},
    }
