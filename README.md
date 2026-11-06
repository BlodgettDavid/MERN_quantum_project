# Quantum Algorithm Dashboard

An interactive quantum computing dashboard powered by a Dockerized Python microservices backend and a Next.js web frontend.

## Software Requirements

- Docker & Docker Compose (Recommended)
- Node.js v20+ (if running frontend standalone)
- Python 3.11+ (if running backend standalone)
- Git

## Setup & Quick Start (Docker Architecture)

The application uses Docker Compose to manage and orchestrate both the Next.js frontend and the Python quantum gateway backend in isolated containers.

### 1. Clone & Navigate to Project
From your terminal:
cd MERN_quantum_project

### 2. Launch All Services via Docker Compose
Build and start the containerized architecture:
docker-compose up --build

This automatically builds and launches:
- **Backend Service (`mern_quantum_backend`)**: Python dynamic quantum gateway running on port 8000.
- **Frontend Service (`mern_quantum_frontend`)**: Next.js web application running on port 3000.

Once running, access the dashboard at http://localhost:3000.

### 3. Stopping Services
To stop and remove the containers, run:
docker-compose down

## Repository Structure

mern_quantum_project/
├── client/                     <-- Next.js frontend application (Standalone output)
│   ├── app/                    <-- Next.js App Router pages
│   └── components/             <-- React UI components
├── src/
│   ├── modules/                <-- Auto-discovered quantum algorithm modules (Grover, Teleportation, etc.)
│   ├── base.py                 <-- Base algorithm class interface
│   └── quantum_service.py      <-- Main Dynamic Quantum Gateway Flask service (Port 8000)
├── plots/                      <-- Generated visualization outputs (.png)
├── results/                    <-- Generated statevector/circuit text outputs (.txt)
├── Dockerfile                  <-- Backend container specification
├── docker-compose.yml          <-- Multi-service orchestration configuration
└── requirements.txt            <-- Python package dependencies

## Notes
- Python and Node.js dependencies are fully containerized, eliminating the need for a local `.venv` or manual dependency installation.
- The Next.js client connects directly to the Quantum Gateway via environment configuration.
- Generated circuit ASCII files, statevectors, Bloch spheres, and histograms are saved to `results/` and `plots/` via volume mounts and served dynamically for browser download.