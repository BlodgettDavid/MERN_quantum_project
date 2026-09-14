from qiskit import QuantumCircuit

def build_diffusion(n_qubits, mode="noancilla"):
    """
    Build a generalized diffusion operator (inversion about the mean).
    mode can be 'noancilla', 'recursion', or 'v-chain' depending on Qiskit mcx support.
    """
    qc = QuantumCircuit(n_qubits)

    # Apply H and X to all qubits
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))

    # Multi-controlled Z on last qubit
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1, mode=mode)
    qc.h(n_qubits - 1)

    # Undo X and H
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))

    return qc