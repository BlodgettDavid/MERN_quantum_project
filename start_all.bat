@echo off
TITLE Quantum Services Starter
echo Starting all Quantum Dashboard Microservices...

:: Dynamically get the directory where this batch file lives (Project Root)
set "PROJECT_ROOT=%~dp0"
set "CLIENT_DIR=%~dp0client"

:: 1. Start Grover Microservice (Port 8001)
start "Grover Service (Port 8001)" cmd /k "cd /d "%PROJECT_ROOT%" && .venv\Scripts\activate.bat && python -m src.algorithms.grover.grover_service"

:: 2. Start Teleportation Microservice (Port 8002)
start "Teleportation Service (Port 8002)" cmd /k "cd /d "%PROJECT_ROOT%" && .venv\Scripts\activate.bat && python -m src.algorithms.teleportation.teleportation_service"

:: 3. Start Main Quantum Gateway (Port 8000)
start "Quantum Gateway (Port 8000)" cmd /k "cd /d "%PROJECT_ROOT%" && .venv\Scripts\activate.bat && python -m src.quantum_service"

:: 4. Start Next.js Frontend (Port 3000)
start "Next.js Client (Port 3000)" cmd /k "cd /d "%CLIENT_DIR%" && npm run dev"

echo All 4 services launched!