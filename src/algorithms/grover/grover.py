# grover.py
# ------------------------------------------------------------
# Quantum Grover Demo using Qiskit
#
# This program builds and simulates Grover’s algorithm on a
# small search space (e.g., 3 qubits = 8 items).
# It uses:
#   - oracle.py to mark the solution state
#   - diffusion.py to amplify the marked state
#   - simulators to visualize amplitude amplification
# ------------------------------------------------------------

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

from .oracle import build_oracle
from .diffusion import build_diffusion

def run_grover():
    # Create a 3-qubit circuit with 3 classical bits
    qc = QuantumCircuit(3, 3)

    # Initialize in uniform superposition
    qc.h([0, 1, 2])

    # Apply oracle (mark |101⟩ for demo)
    qc += build_oracle(3, "101")

    # Apply diffusion operator
    qc += build_diffusion(3)

    # Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])

    # Run on qasm simulator
    qasm = Aer.get_backend('qasm_simulator')
    counts = qasm.run(qc, shots=1024).result().get_counts()

    # Plot histogram
    fig = plot_histogram(counts)
    hist_path = "grover_hist.png"
    fig.savefig(hist_path)
    plt.close(fig)

    return counts, qc.draw(), hist_path
