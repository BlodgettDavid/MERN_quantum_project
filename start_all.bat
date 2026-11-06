@echo off
TITLE Quantum Services Starter
echo Starting Quantum Dashboard Setup...

:: Dynamically get the directory where this batch file lives (Project Root)
set "PROJECT_ROOT=%~dp0"
set "CLIENT_DIR=%~dp0client"

:: ============================================================================
:: 1. Docker Approach (Containerized Environment - ACTIVE)
:: ============================================================================
echo Launching Docker Compose containers...
start "Docker Ecosystem" cmd /k "cd /d "%PROJECT_ROOT%" && docker-compose up --build"


:: ============================================================================
:: 2. Non-Docker Approach (Local Python Virtual Environment + Node - INACTIVE)
:: ============================================================================
:: To run locally outside Docker:
::   1. Comment out line 13 above (Docker Ecosystem).
::   2. Uncomment the local Gateway and Next.js lines below.
::
:: --- Dynamic Gateway Server (Port 8000) ---
:: start "Quantum Gateway (Port 8000)" cmd /k "cd /d "%PROJECT_ROOT%" && .venv\Scripts\activate.bat && python -m src.quantum_service"
::
:: --- Next.js Frontend Client (Port 3000) ---
:: start "Next.js Client (Port 3000)" cmd /k "cd /d "%CLIENT_DIR%" && npm run dev"
::
:: --- Optional Legacy Microservices (Ports 8001 & 8002 - Fallback) ---
:: start "Grover Service (Port 8001)" cmd /k "cd /d "%PROJECT_ROOT%" && .venv\Scripts\activate.bat && python -m src.algorithms.grover.grover_service"
:: start "Teleportation Service (Port 8002)" cmd /k "cd /d "%PROJECT_ROOT%" && .venv\Scripts\activate.bat && python -m src.algorithms.teleportation.teleportation_service"