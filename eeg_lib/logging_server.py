from flask import Flask, request, jsonify
import json
import sys
import time
import numpy as np
import pandas as pd

app = Flask(__name__)

DEFAULT_FILENAME = "/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/logs/test.json"
stim_freqs = [7,10,12] # stim freqs used
fs = 256 # sampling freq
Ns = 256 # number of sample points to consider
Nh = 1 # number of harmonics for CCA-based algos

cal = { 7:[],
        10:[],
        12:[]
        }
index_pos = dict(zip(["Nc", "Ns", "Nt"], range(3)))

def write_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def log_data(payload, filename=None):

    filename = filename or DEFAULT_FILENAME
    session_id = payload.get("session_id", f"default_session_{int(time.time())}")
    try:
        existing_data = read_json(filename)
    except FileNotFoundError:
        existing_data = {}

    if session_id in existing_data:
        existing_data[session_id].append(payload)
        del payload["session_id"]
    else:
        existing_data[session_id] = [payload]
    write_json(filename, existing_data)
    test(payload)
    print(f"Log file {filename} updated successfully.")

def test(payload):
    print(payload)

@app.route("/", methods=["POST"])
def save_data():
    data = request.get_json(force=True)
    if isinstance(data, str):
        data = json.loads(data)
    if data is not None:
        log_data(data)
        return jsonify(msg="data stored successfully"), 200
    return jsonify(msg="invalid data payload"), 400

@app.route('/7hz', methods=["POST"])
def cal7():
    data = request.get_json(force=True)
    cal[7] = data
    print(cal)
    return jsonify(msg="successfully received"), 200

@app.route('/10hz', methods=["POST"])
def cal10():
    data = request.get_json(force=True)
    cal[10] = data
    print(cal)
    return jsonify(msg="successfully received"), 200

@app.route('/12hz', methods=["POST"])
def cal12():
    data = request.get_json(force=True)
    cal[12] = data
    print(cal)
    return jsonify(msg="successfully received"), 200

@app.route('/calibration', methods=["POST"])
def handle_calibration():
    data = request.get_json(force=True)
    if isinstance(data, str):
        data = json.loads(data)
    test(data)
    return jsonify(msg="successfully received"), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
