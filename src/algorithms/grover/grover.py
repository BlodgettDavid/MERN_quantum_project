# grover.py
# ------------------------------------------------------------
# Quantum Grover Demo using Qiskit
# ------------------------------------------------------------

import os
from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector

from .oracle import build_oracle
from .diffusion import build_diffusion
from utils.ascii_utils import to_ascii_diagram

def run_grover():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs("results/grover", exist_ok=True)
    os.makedirs("plots/grover", exist_ok=True)

    qc = QuantumCircuit(3, 3)
    qc.h([0, 1, 2])
    qc.compose(build_oracle(3, "101"), inplace=True)
    qc.compose(build_diffusion(3), inplace=True)
    qc.measure([0, 1, 2], [0, 1, 2])

    sv_backend = Aer.get_backend("statevector_simulator")
    state = sv_backend.run(qc.remove_final_measurements(inplace=False)).result().get_statevector()

    state_json = [{"real": complex(ampl).real, "imag": complex(ampl).imag} for ampl in state]

    qasm_backend = Aer.get_backend("qasm_simulator")
    counts = qasm_backend.run(qc, shots=1024).result().get_counts()
    
    bloch_path = f"grover/bloch_{timestamp}.png"
    fig = plot_bloch_multivector(state)
    fig.savefig(f"plots/{bloch_path}")
    plt.close(fig)
    
    hist_path = f"grover/hist_{timestamp}.png"
    fig2 = plot_histogram(counts)
    fig2.savefig(f"plots/{hist_path}")
    plt.close(fig2)

    state_path = f"grover/statevector_{timestamp}.txt"
    with open(f"results/{state_path}", "w", encoding="utf-8") as f:
        for ampl in state_json:
            f.write(f"{ampl['real']} {ampl['imag']}\n")

    circuit_text = qc.draw(output="text", fold=-1).__str__()
    circuit_text_ascii = to_ascii_diagram(circuit_text)

    circuit_path = f"grover/circuit_{timestamp}.txt"
    with open(f"results/{circuit_path}", "w", encoding="utf-8") as f:
        f.write(circuit_text_ascii)

    base_url = "http://localhost:8000"
    return {
        "algorithm": "grover",
        "circuit_ascii": circuit_text_ascii,
        "plots": {
            "bloch": f"{base_url}/plots/grover/bloch_{timestamp}.png",
            "histogram": f"{base_url}/plots/grover/hist_{timestamp}.png"
        },
        "results": {
            "statevector": f"{base_url}/results/grover/statevector_{timestamp}.txt",
            "circuit": f"{base_url}/results/grover/circuit_{timestamp}.txt"
        },
        "state": state_json
    }