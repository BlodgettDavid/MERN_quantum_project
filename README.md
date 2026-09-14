# Quantum Algorithm Dashboard

An interactive quantum computing dashboard powered by a Python microservices architecture and a Next.js web frontend.

## Software Requirements

- Python 3.11+
- Node.js v20+ with npm
- Git

## Setup & Quick Start

### 1. Python Environment Setup
From the project root:

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

### 2. Frontend Dependencies
cd client
npm install
cd ..

### 3. Launching All Services (Windows)
Run the automated batch script from the root directory to launch all 4 microservices in separate windows simultaneously:

start_all.bat

This will automatically launch:
- Grover Microservice (Port 8001)
- Teleportation Microservice (Port 8002)
- Quantum Gateway API (Port 8000)
- Next.js Web Client (Port 3000)

Once running, access the dashboard at http://localhost:3000.

## Repository Structure

quantum-project/
├── client/                     <-- Next.js frontend application
│   ├── app/                    <-- Next.js App Router pages
│   └── components/             <-- React UI components
├── src/
│   ├── algorithms/
│   │   ├── grover/             <-- Grover search implementation & service (Port 8001)
│   │   └── teleportation/      <-- Teleportation implementation & service (Port 8002)
│   └── quantum_service.py      <-- Main Quantum Gateway service (Port 8000)
├── utils/                      <-- ASCII and plotting helper modules
├── plots/                      <-- Generated visualization outputs (.png)
├── results/                    <-- Generated statevector/circuit text outputs (.txt)
├── .venv/                      <-- Local Python virtual environment (ignored by Git)
├── start_all.bat               <-- One-click batch launcher for local development
└── requirements.txt            <-- Python package dependencies

## Notes
- Python virtual environment dependencies are isolated within .venv/
- The Next.js client connects directly to the Quantum Gateway (http://localhost:8000)
- Generated circuit ASCII files, statevectors, Bloch spheres, and histograms are saved to results/ and plots/ and served dynamically for browser download.