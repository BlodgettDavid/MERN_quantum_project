import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from src.base import BaseAlgorithm
from utils.ascii_utils import to_ascii_diagram


class BellStateAlgorithm(BaseAlgorithm):
    @property
    def name(self) -> str:
        return "bell_state"

    @property
    def category(self) -> str:
        return "Core Primitives"

    @property
    def description(self) -> str:
        return "Generates a maximally entangled Bell state (EPR pair) to demonstrate quantum entanglement and superposition."

    @property
    def parameters(self) -> list:
        return [
            {
                "name": "bell_type",
                "type": "string",
                "default": "Phi_plus",
                "description": "Bell state variant: 'Phi_plus', 'Phi_minus', 'Psi_plus', or 'Psi_minus'."
            },
            {
                "name": "shots",
                "type": "integer",
                "default": 1024,
                "description": "Number of execution shots on the simulator."
            }
        ]

    def run(self, bell_type="Phi_plus", shots=1024):
        # Build 2-qubit circuit for Bell state generation
        qc = QuantumCircuit(2, 2)
        
        # Apply standard circuit depending on the requested Bell variant
        if bell_type == "Phi_plus":
            qc.h(0)
            qc.cx(0, 1)
        elif bell_type == "Phi_minus":
            qc.h(0)
            qc.cx(0, 1)
            qc.z(0)
        elif bell_type == "Psi_plus":
            qc.h(0)
            qc.cx(0, 1)
            qc.x(1)
        elif bell_type == "Psi_minus":
            qc.h(0)
            qc.cx(0, 1)
            qc.z(0)
            qc.x(1)
            
        qc.measure([0, 1], [0, 1])

        # Compute statevector (unmeasured circuit copy)
        clean_qc = qc.copy()
        clean_qc.remove_final_measurements()
        state = Statevector.from_instruction(clean_qc)

        # Output paths
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../results/bell_state"))
        plots_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../plots/bell_state"))

        os.makedirs(results_dir, exist_ok=True)
        os.makedirs(plots_dir, exist_ok=True)

        # Save Statevector text
        sv_path = os.path.join(results_dir, f"statevector_{timestamp}.txt")
        with open(sv_path, "w", encoding="utf-8") as f:
            f.write(str(state))

        # Save ASCII circuit
        circuit_txt_path = os.path.join(results_dir, f"circuit_{timestamp}.txt")
        # Force ASCII-only characters to avoid Windows terminal/encoding rendering corruption
        #circuit_ascii = str(qc.draw(output="text", plot_barriers=False, justify="left"))

        # Draw text and pass through the project's ASCII utility to guarantee clean rendering
        circuit_text = str(qc.draw(output="text", fold=-1))
        circuit_ascii = to_ascii_diagram(circuit_text)

        with open(circuit_txt_path, "w", encoding="utf-8") as f:
            f.write(circuit_ascii)

        # Generate Histogram Plot
        sim = AerSimulator()
        job = sim.run(qc, shots=shots)
        counts = job.result().get_counts()

        hist_path = os.path.join(plots_dir, f"hist_{timestamp}.png")
        plt.figure(figsize=(6, 4))
        fig = plot_histogram(counts)
        fig.savefig(hist_path)
        plt.close()

        return {
            "algorithm": "bell_state",
            "category": self.category,
            "circuit_ascii": circuit_ascii,
            "state": {str(i): {"real": float(val.real), "imag": float(val.imag)} for i, val in enumerate(state.data)},
            "plots": {
                "bloch": None,
                "histogram": f"http://localhost:8000/plots/bell_state/hist_{timestamp}.png"
            },
            "artifacts": {
                "circuit": f"http://localhost:8000/results/bell_state/circuit_{timestamp}.txt",
                "statevector": f"http://localhost:8000/results/bell_state/statevector_{timestamp}.txt"
            }
        }