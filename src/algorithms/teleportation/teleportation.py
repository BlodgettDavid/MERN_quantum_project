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

def run_teleportation():
    """Run the quantum teleportation protocol and return results."""

    os.makedirs("plots/teleportation", exist_ok=True)
    os.makedirs("results/teleportation", exist_ok=True)

    qc = QuantumCircuit(3, 2)
    qc.h(0)
    qc.h(1)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])
    qc.cx(1, 2)
    qc.cz(0, 2)

    sim = Aer.get_backend('statevector_simulator')
    result = sim.run(qc).result()
    state_sv = result.get_statevector()

    state_json = [{"real": complex(ampl).real, "imag": complex(ampl).imag} for ampl in state_sv]

    qasm = Aer.get_backend('qasm_simulator')
    counts = qasm.run(qc, shots=1024).result().get_counts()

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
        "circuit_ascii": circuit_text_ascii,
        "plots": {
            "bloch": f"{base_url}/plots/teleportation/bloch_{timestamp}.png",
            "histogram": f"{base_url}/plots/teleportation/hist_{timestamp}.png"
        },
        "results": {
            "statevector": f"{base_url}/results/teleportation/statevector_{timestamp}.txt",
            "circuit": f"{base_url}/results/teleportation/circuit_{timestamp}.txt"
        },
        "state": state_json
    }