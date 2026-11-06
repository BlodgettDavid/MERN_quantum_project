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
from src.base import BaseAlgorithm


def run_grover(target_state="101", num_qubits=3, shots=1024):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs("results/grover", exist_ok=True)
    os.makedirs("plots/grover", exist_ok=True)

    # Cast inputs in case string numbers are passed in via query parameters
    num_qubits = int(num_qubits)
    shots = int(shots)
    target_state = str(target_state)

    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    qc.compose(build_oracle(num_qubits, target_state), inplace=True)
    qc.compose(build_diffusion(num_qubits), inplace=True)
    qc.measure(range(num_qubits), range(num_qubits))

    sv_backend = Aer.get_backend("statevector_simulator")
    state = sv_backend.run(qc.remove_final_measurements(inplace=False)).result().get_statevector()

    state_json = [{"real": complex(ampl).real, "imag": complex(ampl).imag} for ampl in state]

    qasm_backend = Aer.get_backend("qasm_simulator")
    counts = qasm_backend.run(qc, shots=shots).result().get_counts()
    
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
        "category": "Search",
        "circuit_ascii": circuit_text_ascii,
        "plots": {
            "bloch": f"{base_url}/plots/grover/bloch_{timestamp}.png",
            "histogram": f"{base_url}/plots/grover/hist_{timestamp}.png"
        },
        "artifacts": {
            "statevector": f"{base_url}/results/grover/statevector_{timestamp}.txt",
            "circuit": f"{base_url}/results/grover/circuit_{timestamp}.txt"
        },
        "state": state_json
    }


class GroverAlgorithm(BaseAlgorithm):
    @property
    def name(self) -> str:
        return "grover"

    @property
    def category(self) -> str:
        return "Search"

    @property
    def description(self) -> str:
        return "Grover's Search Algorithm provides quadratic speedup for unstructured search problems."

    @property
    def parameters(self) -> list:
        return [
            {
                "name": "target_state",
                "type": "string",
                "default": "101",
                "description": "Binary string representing the target item to search for."
            },
            {
                "name": "num_qubits",
                "type": "integer",
                "default": 3,
                "description": "Number of qubits in the search space."
            },
            {
                "name": "shots",
                "type": "integer",
                "default": 1024,
                "description": "Number of execution shots on the QASM simulator."
            }
        ]

    def run(self, **kwargs) -> dict:
        """Executes the Grover circuit pipeline with dynamic parameters."""
        return run_grover(
            target_state=kwargs.get("target_state", "101"),
            num_qubits=kwargs.get("num_qubits", 3),
            shots=kwargs.get("shots", 1024)
        )