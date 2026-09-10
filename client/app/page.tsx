"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [groverResult, setGroverResult] = useState("");
  const [teleportationResult, setTeleportationResult] = useState("");

  useEffect(() => {
    fetch("http://localhost:5000/api/quantum/grover")
      .then((res) => res.json())
      .then((data) => setGroverResult(data.result));

    fetch("http://localhost:5000/api/quantum/teleportation")
      .then((res) => res.json())
      .then((data) => setTeleportationResult(data.result));
  }, []);

  return (
    <main style={{ padding: "2rem" }}>
      <h1>Quantum Demos</h1>
      <section>
        <h2>Grover Result</h2>
        <pre>{groverResult}</pre>
      </section>
      <section>
        <h2>Teleportation Result</h2>
        <pre>{teleportationResult}</pre>
      </section>
    </main>
  );
}