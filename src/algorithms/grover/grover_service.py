from flask import Flask, jsonify
from flask_cors import CORS
from src.algorithms.grover.grover import run_grover

app = Flask(__name__)
CORS(app)

@app.route("/grover", methods=["GET"])
def grover_route():
    try:
        return jsonify(run_grover())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    from waitress import serve
    print("Grover microservice running on http://localhost:8001 ...")
    serve(app, host="0.0.0.0", port=8001)