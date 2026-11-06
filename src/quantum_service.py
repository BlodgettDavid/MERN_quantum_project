import os
import pkgutil
import importlib
import inspect
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from waitress import serve
from src.base import BaseAlgorithm

load_dotenv()

app = Flask(__name__)

allowed_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
CORS(app, resources={r"/*": {"origins": allowed_origin}})

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
RESULTS_DIR = os.path.join(BASE_DIR, "results")


# ============================================================================
# Dynamic Gateway Algorithm Registry
# ============================================================================

REGISTRY = {}

def register_all_domains():
    """Auto-discovers and registers BaseAlgorithm implementations cleanly without duplicates."""
    if REGISTRY:
        return REGISTRY

    #src_dir = os.path.dirname(__file__)    
    modules_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "modules"))

    
    #for _, module_name, is_pkg in pkgutil.walk_packages([src_dir], prefix="src."):
    for _, module_name, is_pkg in pkgutil.walk_packages([modules_dir], prefix="src.modules."):
        
        # Ignore server script itself and base classes
        if is_pkg or "quantum_service" in module_name or module_name.endswith(".base"):
            continue

        try:
            mod = importlib.import_module(module_name)
            
            for _, cls in inspect.getmembers(mod, inspect.isclass):
                if (
                    issubclass(cls, BaseAlgorithm) 
                    and cls is not BaseAlgorithm 
                    and cls.__module__ == mod.__name__
                ):
                    instance = cls()
                    algo_name = getattr(instance, "name", None)
                    
                    if not algo_name:
                        continue

                    algo_key = str(algo_name).lower()
                    
                    if algo_key in REGISTRY:
                        continue

                    REGISTRY[algo_key] = {
                        "instance": instance,
                        "category": getattr(instance, "category", "General")
                    }
                    print(f"[Gateway] Registered algorithm: '{algo_name}' under category [{instance.category}]")

        except Exception as e:
            print(f"[Gateway] Skipped loading {module_name}: {e}")

    return REGISTRY

# Explicitly populate registry once on module initialization
register_all_domains()

# ============================================================================
# Static Asset Routes
# ============================================================================
@app.route("/plots/<path:filename>")
def serve_plot(filename):
    return send_from_directory(PLOTS_DIR, filename, as_attachment=True)

@app.route("/results/<path:filename>")
def serve_result(filename):
    return send_from_directory(RESULTS_DIR, filename, as_attachment=True)

# ============================================================================
# Dynamic API Endpoints
# ============================================================================
@app.route("/catalog", methods=["GET"])
def get_catalog():
    """Returns available programs grouped by domain category for the frontend UI."""
    catalog = {}
    for key, item in REGISTRY.items():
        cat = item["category"]
        algo_instance = item["instance"]
        
        catalog.setdefault(cat, []).append({
            "id": key,
            "name": getattr(algo_instance, "name", key).title(),
            "description": getattr(algo_instance, "description", ""),
            "parameters": getattr(algo_instance, "parameters", [])
        })
        
    return jsonify({
        "status": "success",
        "catalog": catalog
    }), 200

@app.route("/run", methods=["GET", "POST"])
def run_algorithm():
    """Executes a quantum algorithm via GET query string or POST JSON body."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        program = data.get("algorithm", data.get("program", "grover")).lower()
        params = data.get("params", {})
    else:
        program = request.args.get("program", "grover").lower()
        params = {k: v for k, v in request.args.items() if k != "program"}

    if program not in REGISTRY:
        return jsonify({
            "status": "error",
            "message": f"Unknown algorithm '{program}'",
            "available": list(REGISTRY.keys())
        }), 404

    try:
        instance = REGISTRY[program]["instance"]
        
        if params and callable(getattr(instance, "run", None)):
            try:
                payload = instance.run(**params)
            except TypeError:
                payload = instance.run()
        else:
            payload = instance.run()

        return jsonify({
            "status": "success",
            "algorithm": program,
            "results": payload
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    print("Main Dynamic Quantum Gateway running on http://localhost:8000 ...")
    serve(app, host="0.0.0.0", port=8000)