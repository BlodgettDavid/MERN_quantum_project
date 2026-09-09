## Non-Python Requirements

This project uses both Python and Node.js stacks.  
Python handles the quantum libraries and analytics, while Node.js powers the frontend (Next.js) and backend (Express + MongoDB).

### Required Software
- Python 3.11+ with virtual environment (`.quantum-dev-env`)
- Node.js v20+ and npm (comes bundled with Node.js)
- MongoDB (local install or Atlas cloud instance)
- Git (already initialized in this repo)

### Version Checks
Verify installations:
- `node -v` → should be v20+
- `npm -v` → should be v12+
- `mongod --version` → confirm MongoDB is installed

### Setup Instructions

#### Backend (Express + Quantum)
cd src/server  
npm install  
node index.js  

Runs the Express API server, connects to MongoDB (local or Atlas), and can call into quantum code in `src/`.

#### Frontend (Next.js)
cd client  
npm install  
npm run dev  

Starts the Next.js development server, accessible at http://localhost:3000, with hot‑reload on file changes.

### Environment Variables
- Place secrets (e.g., MongoDB connection string) in a `.env` file.
- Example: `MONGO_URI=mongodb://localhost:27017/quantumdb`
- Ensure `.env` is excluded via `.gitignore`.

### Repo Structure
quantum-project/  
  client/        <-- Next.js frontend  
  src/           <-- Backend + quantum code  
    server/      <-- Express API  
  utils/         <-- Helper scripts  
  results/       <-- Output data  
  plots/         <-- Visualizations  
  .quantum-dev-env/ <-- Python virtual environment  

### Notes
- Python venv is isolated from Node.js stack — they run separately.
- Anyone cloning this repo must install both Python and Node.js stacks.
- MongoDB can be local or cloud; update `.env` accordingly.
