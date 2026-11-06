"use client";

import React, { useState, useEffect } from "react";

export default function QuantumDashboard() {
  const [catalog, setCatalog] = useState({});
  const [selectedAlgo, setSelectedAlgo] = useState("");
  const [params, setParams] = useState({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const API_BASE = "http://localhost:8000";

  // 1. Fetch dynamic catalog on mount
  useEffect(() => {
    fetch(`${API_BASE}/catalog`)
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          setCatalog(data.catalog);
          // Auto-select the first available algorithm if present
          const categories = Object.keys(data.catalog);
          if (categories.length > 0 && data.catalog[categories[0]].length > 0) {
            const firstAlgo = data.catalog[categories[0]][0];
            setSelectedAlgo(firstAlgo.id);
            initParams(firstAlgo.parameters);
          }
        }
      })
      .catch((err) => setError("Failed to connect to Quantum Gateway API: " + err.message));
  }, []);

  // Initialize form parameters with default values from schema
  const initParams = (parameters) => {
    const defaults = {};
    parameters.forEach((p) => {
      defaults[p.name] = p.default;
    });
    setParams(defaults);
  };

  // Handle algorithm selection change
  const handleAlgoChange = (algoId) => {
    setSelectedAlgo(algoId);
    for (const cat of Object.keys(catalog)) {
      const found = catalog[cat].find((a) => a.id === algoId);
      if (found) {
        initParams(found.parameters);
        break;
      }
    }
    setResult(null);
  };

  // Handle parameter input changes
  const handleParamChange = (name, value) => {
    setParams((prev) => ({ ...prev, [name]: value }));
  };

  // Execute algorithm run
  const handleRun = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          algorithm: selectedAlgo,
          params: params,
        }),
      });

      const data = await response.json();
      if (data.status === "success") {
        setResult(data.results);
      } else {
        setError(data.message || "Execution failed.");
      }
    } catch (err) {
      setError("Network error during execution: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Helper to find current algorithm metadata
  const getCurrentAlgoMeta = () => {
    for (const cat of Object.keys(catalog)) {
      const found = catalog[cat].find((a) => a.id === selectedAlgo);
      if (found) return found;
    }
    return null;
  };

  const currentMeta = getCurrentAlgoMeta();

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-6">
      <header className="max-w-6xl mx-auto mb-8 border-b border-gray-800 pb-4">
        <h1 className="text-3xl font-bold tracking-tight text-cyan-400">Quantum Algorithm Dashboard</h1>
        <p className="text-sm text-gray-400 mt-1">
          Dynamic Gateway Architecture • Python Qiskit Backend & Next.js Frontend
        </p>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Left Column: Control Panel */}
        <section className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl md:col-span-1">
          <h2 className="text-xl font-semibold mb-4 text-cyan-300">Algorithm Control</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-950/50 border border-red-800 rounded-lg text-red-300 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleRun} className="space-y-4">
            <div>
              <label className="block text-xs font-medium uppercase tracking-wider text-gray-400 mb-2">
                Select Algorithm
              </label>
              <select
                value={selectedAlgo}
                onChange={(e) => handleAlgoChange(e.target.value)}
                className="w-full bg-gray-950 border border-gray-700 rounded-lg p-2.5 text-sm text-gray-200 focus:ring-2 focus:ring-cyan-500 outline-none"
              >
                {Object.keys(catalog).map((cat) => (
                  <optgroup key={cat} label={cat}>
                    {catalog[cat].map((algo) => (
                      <option key={algo.id} value={algo.id}>
                        {algo.name}
                      </option>
                    ))}
                  </optgroup>
                ))}
              </select>
            </div>

            {currentMeta && (
              <p className="text-xs text-gray-400 bg-gray-950 p-3 rounded-lg border border-gray-800">
                {currentMeta.description}
              </p>
            )}

            {/* Dynamic Parameter Inputs */}
            {currentMeta && currentMeta.parameters && currentMeta.parameters.length > 0 && (
              <div className="space-y-3 pt-2">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-gray-400">Parameters</h3>
                {currentMeta.parameters.map((param) => (
                  <div key={param.name}>
                    <label className="block text-xs text-gray-300 mb-1">
                      {param.name} <span className="text-gray-500">({param.type})</span>
                    </label>
                    <input
                      type={param.type === "integer" ? "number" : "text"}
                      value={params[param.name] ?? param.default}
                      onChange={(e) =>
                        handleParamChange(
                          param.name,
                          param.type === "integer" ? parseInt(e.target.value) || 0 : e.target.value
                        )
                      }
                      className="w-full bg-gray-950 border border-gray-700 rounded-lg p-2 text-sm text-gray-200 focus:ring-2 focus:ring-cyan-500 outline-none"
                    />
                    <p className="text-[10px] text-gray-500 mt-0.5">{param.description}</p>
                  </div>
                ))}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-4 bg-cyan-600 hover:bg-cyan-500 text-white font-medium py-2.5 px-4 rounded-lg transition-colors disabled:opacity-50 text-sm shadow-lg shadow-cyan-900/20"
            >
              {loading ? "Executing Simulation..." : "Run Simulation"}
            </button>
          </form>
        </section>

        {/* Right Column: Results & Visualization */}
        <section className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl md:col-span-2 space-y-6">
          <h2 className="text-xl font-semibold text-cyan-300">Execution Telemetry</h2>

          {!result ? (
            <div className="flex flex-col items-center justify-center h-64 border border-dashed border-gray-800 rounded-lg text-gray-500">
              <p>Select an algorithm and click 'Run Simulation' to view results.</p>
            </div>
          ) : (
            <div className="space-y-6">
              {/* ASCII Circuit View */}
              <div>
                <h3 className="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">
                  Quantum Circuit Diagram (ASCII)
                </h3>
                <pre className="bg-gray-950 border border-gray-800 p-4 rounded-lg text-xs font-mono overflow-x-auto text-emerald-400">
                  {result.circuit_ascii}
                </pre>
              </div>

              {/* Generated Plots */}
              {result.plots && (
                <div>
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">
                    Visualization Plots
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {result.plots.bloch && (
                      <div className="bg-gray-950 border border-gray-800 p-3 rounded-lg text-center">
                        <p className="text-xs text-gray-400 mb-2">Bloch Sphere</p>
                        <img
                          src={result.plots.bloch}
                          alt="Bloch Sphere Plot"
                          className="mx-auto rounded max-h-48 object-contain"
                        />
                      </div>
                    )}
                    {result.plots.histogram && (
                      <div className="bg-gray-950 border border-gray-800 p-3 rounded-lg text-center">
                        <p className="text-xs text-gray-400 mb-2">Measurement Histogram</p>
                        <img
                          src={result.plots.histogram}
                          alt="Histogram Plot"
                          className="mx-auto rounded max-h-48 object-contain"
                        />
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Artifact Links */}
              {result.artifacts && (
                <div className="pt-2 border-t border-gray-800 flex gap-4 text-xs">
                  <a
                    href={result.artifacts.statevector}
                    target="_blank"
                    rel="noreferrer"
                    className="text-cyan-400 hover:uint-link text-cyan-400 hover:underline"
                  >
                    📄 View Statevector Text
                  </a>
                  <a
                    href={result.artifacts.circuit}
                    target="_blank"
                    rel="noreferrer"
                    className="text-cyan-400 hover:underline"
                  >
                    📄 View Raw Circuit File
                  </a>
                </div>
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}