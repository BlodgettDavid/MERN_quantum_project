from flask import Flask, jsonify
from flask_cors import CORS
from src.algorithms.teleportation.teleportation import run_teleportation

app = Flask(__name__)
CORS(app)

@app.route("/teleportation", methods=["GET"])
def teleportation_route():
    try:
        return jsonify(run_teleportation())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    from waitress import serve
    print("Teleportation microservice running on http://localhost:8002 ...")
    serve(app, host="0.0.0.0", port=8002)