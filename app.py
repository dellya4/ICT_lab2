import os
import json
import uuid

from datetime import datetime
from flask import Flask, request, jsonify


app = Flask(__name__)


QUEUE_DIR = "queue"
RESULTS_DIR = "results"


os.makedirs(QUEUE_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({
            "error": "field 'message' is required"
        }), 400

    if not isinstance(data["message"], str):
        return jsonify({
            "error": "field 'message' must be a string"
        }), 400

    return jsonify({
        "reply": data["message"]
    }), 200


@app.route("/time", methods=["GET"])
def get_time():
    current_time = datetime.now().isoformat(timespec="seconds")

    return jsonify({
        "time": current_time
    }), 200


@app.route("/jobs", methods=["POST"])
def submit_job():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({
            "error": "field 'message' is required"
        }), 400

    if not isinstance(data["message"], str):
        return jsonify({
            "error": "field 'message' must be a string"
        }), 400

    job_id = str(uuid.uuid4())

    job = {
        "job_id": job_id,
        "message": data["message"]
    }

    temp_path = os.path.join(
        QUEUE_DIR,
        f"{job_id}.tmp"
    )

    final_path = os.path.join(
        QUEUE_DIR,
        f"{job_id}.json"
    )

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(job, file, ensure_ascii=False)

    os.replace(temp_path, final_path)

    return jsonify({
        "job_id": job_id,
        "status": "queued"
    }), 202


@app.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    try:
        uuid.UUID(job_id)
    except ValueError:
        return jsonify({
            "error": "job not found"
        }), 404

    queue_path = os.path.join(
        QUEUE_DIR,
        f"{job_id}.json"
    )

    result_path = os.path.join(
        RESULTS_DIR,
        f"{job_id}.json"
    )

    if os.path.exists(result_path):
        with open(result_path, "r", encoding="utf-8") as file:
            result_data = json.load(file)

        return jsonify({
            "job_id": job_id,
            "status": "done",
            "result": result_data["result"]
        }), 200

    if os.path.exists(queue_path):
        return jsonify({
            "job_id": job_id,
            "status": "queued"
        }), 200

    return jsonify({
        "error": "job not found"
    }), 404


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "resource not found"
    }), 404


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )