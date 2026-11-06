# teleportation.py
# ------------------------------------------------------------
# Quantum Teleportation Demo using Qiskit
# ------------------------------------------------------------

import os
from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from utils.ascii_utils import to_ascii_diagram
from src.base import BaseAlgorithm


def run_teleportation(initial_state="plus", shots=1024):
    """Run the quantum teleportation protocol and return results."""
    os.makedirs("plots/teleportation", exist_ok=True)
    os.makedirs("results/teleportation", exist_ok=True)

    shots = int(shots)

    # 3 Qubits, 2 Classical Bits for Bell measurement
    qc = QuantumCircuit(3, 2)

    # Step 0: State Preparation on Qubit 0
    if initial_state == "plus":
        qc.h(0)
    elif initial_state == "one":
        qc.x(0)
    elif initial_state == "minus":
        qc.x(0)
        qc.h(0)

    # Step 1: Entangle Qubit 1 and Qubit 2 (Bell pair between Alice and Bob)
    qc.h(1)
    qc.cx(1, 2)

    # Step 2: Alice performs Bell measurement on Qubit 0 and 1
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])

    # Step 3: Bob applies conditional gates based on Alice's classical measurement
    qc.cx(1, 2)
    qc.cz(0, 2)

    sim = Aer.get_backend('statevector_simulator')
    result = sim.run(qc).result()
    state_sv = result.get_statevector()

    state_json = [{"real": complex(ampl).real, "imag": complex(ampl).imag} for ampl in state_sv]

    qasm = Aer.get_backend('qasm_simulator')
    counts = qasm.run(qc, shots=shots).result().get_counts()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    bloch_path = f"teleportation/bloch_{timestamp}.png"
    hist_path = f"teleportation/hist_{timestamp}.png"

    fig = plot_bloch_multivector(state_sv)
    fig.savefig(f"plots/{bloch_path}")
    plt.close(fig)

    fig2 = plot_histogram(counts)
    fig2.savefig(f"plots/{hist_path}")
    plt.close(fig2)

    state_path = f"teleportation/statevector_{timestamp}.txt"
    circuit_path = f"teleportation/circuit_{timestamp}.txt"

    with open(f"results/{state_path}", "w", encoding="utf-8") as f:
        for ampl in state_json:
            f.write(f"{ampl['real']} {ampl['imag']}\n")

    circuit_text = str(qc.draw(output="text", fold=-1))
    circuit_text_ascii = to_ascii_diagram(circuit_text)

    with open(f"results/{circuit_path}", "w", encoding="utf-8") as f:
        f.write(circuit_text_ascii)

    base_url = "http://localhost:8000"
    return {
        "algorithm": "teleportation",
        "category": "Teleportation",
        "circuit_ascii": circuit_text_ascii,
        "plots": {
            "bloch": f"{base_url}/plots/teleportation/bloch_{timestamp}.png",
            "histogram": f"{base_url}/plots/teleportation/hist_{timestamp}.png"
        },
        "artifacts": {
            "statevector": f"{base_url}/results/teleportation/statevector_{timestamp}.txt",
            "circuit": f"{base_url}/results/teleportation/circuit_{timestamp}.txt"
        },
        "state": state_json
    }


class TeleportationAlgorithm(BaseAlgorithm):
    @property
    def name(self) -> str:
        return "teleportation"

    @property
    def category(self) -> str:
        return "Teleportation"

    @property
    def description(self) -> str:
        return "Transfers a quantum state from Alice to Bob using an entangled Bell pair and 2 classical bits."

    @property
    def parameters(self) -> list:
        return [
            {
                "name": "initial_state",
                "type": "string",
                "default": "plus",
                "description": "Initial state prep on Qubit 0: 'zero', 'one', 'plus', or 'minus'."
            },
            {
                "name": "shots",
                "type": "integer",
                "default": 1024,
                "description": "Number of execution shots on the QASM simulator."
            }
        ]

    def run(self, **kwargs) -> dict:
        """Executes the Quantum Teleportation protocol and returns the standardized UI payload."""
        return run_teleportation(
            initial_state=kwargs.get("initial_state", "plus"),
            shots=kwargs.get("shots", 1024)
        )