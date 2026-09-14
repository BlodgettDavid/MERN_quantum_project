'use client';

import React, { useState } from 'react';
import axios from 'axios';
import './QuantumDashboard.css';

const API_BASE_URL = 'http://localhost:8000';

function QuantumDashboard() {
  const [selectedProgram, setSelectedProgram] = useState('grover');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const formatUrl = (url) => {
    if (!url) return '';
    const cleanPath = url.replace(/\\/g, '/');
    if (cleanPath.startsWith('http')) return cleanPath;
    return `${API_BASE_URL}/${cleanPath.replace(/^\//, '')}`;
  };

  const handleRunProgram = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await axios.get(`${API_BASE_URL}/run?program=${selectedProgram}`);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Execution failed');
    } finally {
      setLoading(false);
    }
  };

  // Direct nested mappings to your Flask Gateway JSON schema
  const histogramUrl = result?.plots?.histogram;
  const blochUrl = result?.plots?.bloch;
  const circuitFileUrl = result?.results?.circuit;
  const statevectorFileUrl = result?.results?.statevector;

  // Format array of complex numbers into a clean string representation
  const formatStatevector = (stateArray) => {
    if (!Array.isArray(stateArray)) return null;
    return stateArray
      .map((item, idx) => {
        const real = item.real !== undefined ? item.real.toFixed(4) : '0.0000';
        const imag = item.imag !== undefined ? item.imag.toFixed(4) : '0.0000';
        const sign = item.imag >= 0 ? '+' : '-';
        return `|${idx}⟩ (${idx.toString(2).padStart(3, '0')}): ${real} ${sign} ${Math.abs(imag)}j`;
      })
      .join('\n');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Quantum Algorithm Dashboard</h1>
        <p>Microservice-Powered Quantum Simulations</p>
      </header>

      <div className="controls-panel">
        <label htmlFor="program-select">Select Algorithm:</label>
        <select
          id="program-select"
          value={selectedProgram}
          onChange={(e) => setSelectedProgram(e.target.value)}
          disabled={loading}
        >
          <option value="grover">Grover Search</option>
          <option value="teleportation">Quantum Teleportation</option>
        </select>

        <button 
          onClick={handleRunProgram} 
          disabled={loading}
          className="run-btn"
        >
          {loading ? 'Executing...' : 'Run Simulation'}
        </button>
      </div>

      {error && (
        <div className="error-banner">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="results-grid">
          {result.circuit_ascii && (
            <div className="result-card">
              <h3>Circuit Diagram</h3>
              <pre className="ascii-output">{result.circuit_ascii}</pre>
              {circuitFileUrl && (
                <a 
                  href={formatUrl(circuitFileUrl)} 
                  download 
                  className="download-link"
                >
                  Download ASCII Circuit (.txt)
                </a>
              )}
            </div>
          )}

          {result.state && (
            <div className="result-card">
              <h3>Final Statevector</h3>
              <pre className="ascii-output">{formatStatevector(result.state)}</pre>
              {statevectorFileUrl && (
                <a 
                  href={formatUrl(statevectorFileUrl)} 
                  download 
                  className="download-link"
                >
                  Download Statevector (.txt)
                </a>
              )}
            </div>
          )}

          {histogramUrl && (
            <div className="result-card">
              <h3>Measurement Histogram</h3>
              <img 
                src={formatUrl(histogramUrl)} 
                alt="Histogram Plot" 
                className="plot-image"
              />
              <br />
              <a 
                href={formatUrl(histogramUrl)} 
                download 
                className="download-link"
              >
                Download Histogram (.png)
              </a>
            </div>
          )}

          {blochUrl && (
            <div className="result-card">
              <h3>Bloch Sphere Vector</h3>
              <img 
                src={formatUrl(blochUrl)} 
                alt="Bloch Sphere Plot" 
                className="plot-image"
              />
              <br />
              <a 
                href={formatUrl(blochUrl)} 
                download 
                className="download-link"
              >
                Download Bloch Plot (.png)
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default QuantumDashboard;