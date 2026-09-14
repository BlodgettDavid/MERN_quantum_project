from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
from waitress import serve

load_dotenv()

app = Flask(__name__)

allowed_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
CORS(app, resources={r"/*": {"origins": allowed_origin}})

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

MICROSERVICES = {
    "grover": "http://localhost:8001/grover",
    "teleportation": "http://localhost:8002/teleportation",
}

@app.route("/plots/<path:filename>")
def serve_plot(filename):
    return send_from_directory(PLOTS_DIR, filename, as_attachment=True)

@app.route("/results/<path:filename>")
def serve_result(filename):
    return send_from_directory(RESULTS_DIR, filename, as_attachment=True)

@app.route("/run", methods=["GET"])
def run_algorithm():
    program = request.args.get("program", "teleportation")
    if program not in MICROSERVICES:
        return jsonify({"error": f"Unknown program '{program}'"}), 400

    try:
        service_url = MICROSERVICES[program]
        response = requests.get(service_url)
        return (response.content, response.status_code, response.headers.items())
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Microservice for {program} is not running on its designated port."}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Main Quantum Gateway running on http://localhost:8000 ...")
    serve(app, host="0.0.0.0", port=8000)