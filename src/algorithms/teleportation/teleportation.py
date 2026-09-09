# teleportation.py
# ------------------------------------------------------------
# Quantum Teleportation Demo using Qiskit
#
# This program builds and simulates the quantum teleportation
# protocol. It uses three qubits and two classical bits:
#   - Qubit 0: the state to be teleported
#   - Qubit 1: Alice’s entangled qubit
#   - Qubit 2: Bob’s entangled qubit
#   - Classical bits: store Alice’s measurement results
#
# Steps:
#   1. Build the teleportation circuit (Hadamard, CNOT, CZ gates).
#   2. Run the circuit on the statevector simulator to get the
#      exact quantum state (for Bloch sphere visualization).
#   3. Run the circuit on the qasm simulator with multiple shots
#      to get measurement statistics (for histogram visualization).
#   4. Save plots to disk in plots/, and textual results to
#      results/teleportation/ with timestamped filenames.
#
# Outputs:
#   - Statevector (numerical quantum state)
#   - Circuit diagram (ASCII)
#   - Bloch sphere image (plots/)
#   - Histogram image (plots/)
#   - Statevector text file (results/teleportation/)
#   - Circuit text file (results/teleportation/)
# ------------------------------------------------------------

import os
from datetime import datetime
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_bloch_multivector, plot_histogram
import matplotlib.pyplot as plt

def run_teleportation():
    # Ensure folders exist
    os.makedirs("plots", exist_ok=True)
    os.makedirs("results/teleportation", exist_ok=True)

    # Create a quantum circuit with 3 qubits and 2 classical bits
    qc = QuantumCircuit(3, 2)

    # --- Build the teleportation protocol ---
    qc.h(0)              # Put qubit 0 into superposition (state to teleport)
    qc.h(1)              # Begin entanglement: Hadamard on qubit 1
    qc.cx(1, 2)          # Entangle qubit 1 and qubit 2 (Alice–Bob pair)
    qc.cx(0, 1)          # Bell measurement step: CNOT between qubit 0 and 1
    qc.h(0)              # Bell measurement step: Hadamard on qubit 0
    qc.measure([0,1],[0,1])  # Measure Alice’s two qubits into classical bits
    qc.cx(1, 2)          # Bob’s correction: apply X if Alice’s second bit = 1
    qc.cz(0, 2)          # Bob’s correction: apply Z if Alice’s first bit = 1

    # --- Statevector simulation ---
    sim = Aer.get_backend('statevector_simulator')
    result = sim.run(qc).result()
    state = result.get_statevector()

    # --- Measurement statistics ---
    qasm = Aer.get_backend('qasm_simulator')
    counts = qasm.run(qc, shots=1024).result().get_counts()


    # --- Ensure folders exist ---
    os.makedirs("plots/teleportation", exist_ok=True)
    os.makedirs("results/teleportation", exist_ok=True)

    # --- Timestamp for filenames ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # --- Save plots into plots/teleportation ---
    bloch_path = f"plots/teleportation/bloch_{timestamp}.png"
    hist_path  = f"plots/teleportation/hist_{timestamp}.png"

    fig = plot_bloch_multivector(state)
    fig.savefig(bloch_path)
    plt.close(fig)

    fig2 = plot_histogram(counts)
    fig2.savefig(hist_path)
    plt.close(fig2)

    # --- Save textual results ---
    # --- Save textual results ---
    state_path = f"results/teleportation/statevector_{timestamp}.txt"
    circuit_path = f"results/teleportation/circuit_{timestamp}.txt"

    with open(state_path, "w", encoding="utf-8") as f:
        f.write(str(state))

    # Standard Qiskit 1.4.5 circuit text generation
    circuit_text = str(qc.draw(output="text", fold=-1))

    with open(circuit_path, "w", encoding="utf-8") as f:
        f.write(circuit_text)

    # Return results for GUI display
    return state, circuit_text, bloch_path, hist_path, state_path, circuit_path