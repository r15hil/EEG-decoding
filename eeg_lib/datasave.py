from flask import Flask, request, jsonify
import json
import sys
import time

app = Flask(__name__)

DEFAULT_FILENAME = "/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/logs/texts/"

data_array = []

@app.route("/collect", methods=["POST"])
def collect_data():
    global data_array
    data = request.get_json(force=True)
    if isinstance(data, str):
        data = json.loads(data)
    if data is not None:
        data_array = data_array + data['raw_data']
    
    return jsonify(msg="data collected"), 200

@app.route("/save", methods=["GET"])
def save_data():
    sourceFile = open(DEFAULT_FILENAME+'saved_array.txt', 'w')
    print(data_array , file = sourceFile)
    sourceFile.close()
    return jsonify(msg="data stored successfully"), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)