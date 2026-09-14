from qiskit import QuantumCircuit

def build_oracle(n_qubits, marked_state="101"):
    qc = QuantumCircuit(n_qubits)
    # Flip qubits where marked_state has '0'
    for i, bit in enumerate(marked_state):
        if bit == "0":
            qc.x(i)
    # Multi-controlled Z on last qubit
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)
    # Undo flips
    for i, bit in enumerate(marked_state):
        if bit == "0":
            qc.x(i)
    return qc