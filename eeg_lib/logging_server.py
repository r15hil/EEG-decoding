from flask import Flask, request, jsonify
import json
import sys
import time
import numpy as np
import pandas as pd
from cca import GCCA_SSVEP
from cca import MsetCCA_SSVEP

app = Flask(__name__)

DEFAULT_FILENAME = "/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/logs/newData.json"

stim_freqs = [7,10,12] # stim freqs used
fs = 256 # sampling freq
Ns = 256 # number of sample points to consider
Nh = 1 # number of harmonics for CCA-based algos

cal = [{'7':[]},{'10':[]},{'12':[]}]
# cal = [{'7': [[0.08608168, 63.97714, -10.95186, 19.06907, 97.78001, -58.55355, -17.09743, 5.744898, -19.44468, -154.5176, -70.6512, 7.254728, 70.29575, -65.22755, 19.3994, 83.19728, -0.1587, 79.14191, 124.9848, -80.8523, -66.59636, -106.6282, 158.1011, 18.6889, -91.77558, -31.38925, 49.25134, 134.6853, -33.49792, -55.22517, 25.63784, -5.474773, 0.1292482, 98.37338, -100.2213, -29.13411, 92.16316, -14.71991, -73.43613, -88.22791, 99.44291, 5.445168, -96.91243, 30.14591, 114.0855, -64.05473, -4.791245, 45.39081, -0.1180776, 60.97627, 71.72646, -14.90696, -73.29198, 7.407163, -2.112297, -59.6017, -131.4947, 56.13616, 29.38062, -48.09933, 23.04197, 94.06303, 117.6484, -51.9588], [-0.03113472, -89.58508, 4.664486, 88.18389, 66.92102, -63.85786, -56.60577, 55.66212, 55.01099, -151.6385, 35.95838, -73.1279, -102.9078, 104.3905, 62.76445, -138.825, -0.1006649, 124.0058, 21.5789, 14.83963, -23.36331, 68.37307, -56.17267, 10.3171, 20.86862, -165.4349, -55.29525, 9.367093, 31.36337, -61.53616, -0.6864805, 103.2919, -0.1285314, 73.04314, 104.1034, -92.9646, -18.13019, 2.455214, 49.29693, -89.42948, -100.269, 121.7752, -44.78757, -151.5056, 103.3387, 15.41797, -92.53924, -1.257305, -0.07528348, -86.35637, 2.307805, 94.8072, 91.32171, -59.61378, -28.93213, 98.05148, -93.44037, -45.2926, 15.08645, 50.34007, -69.38409, -96.79453, 49.45483, 60.97854], [-0.07528348, -86.35637, 2.307805, 94.8072, 91.32171, -59.61378, -28.93213, 98.05148, -93.44037, -45.2926, 15.08645, 50.34007, -69.38409, -96.79453, 49.45483, 60.97854, -0.06435973, -20.10022, 41.09283, 1.234785, -113.5008, -97.58199, 79.35908, -4.267892, -137.0867, 16.41276, 36.88237, -20.64272, -7.069607, 88.11347, 115.3652, -60.32734, 0.1704095, 10.96589, -70.27126, -45.01587, 21.11184, 27.84858, -115.3701, -39.16667, 89.37253, -30.83098, 11.37188, 11.02855, 87.59206, 7.906512, -49.00477, 85.61246, -0.03020137, -109.9827, 69.32402, -14.25044, -17.74427, -110.6884, 104.5726, 92.44341, -107.9399, 64.01708, 88.28169, 59.75462, -46.53099, 8.563478, 90.21355, -82.08953], [-0.03020137, -109.9827, 69.32402, -14.25044, -17.74427, -110.6884, 104.5726, 92.44341, -107.9399, 64.01708, 88.28169, 59.75462, -46.53099, 8.563478, 90.21355, -82.08953, -0.03803459, 144.0075, 8.284266, -129.5013, -43.70687, 62.65037, 21.89877, -108.9544, 10.35776, 92.09826, -37.28483, 45.01656, 145.2784, -126.1515, -25.72871, -21.87284, 0.09583076, 69.87121, -105.4652, 52.13925, 90.39283, -1.062859, 34.06622, 10.25257, 40.85835, -100.3273, -59.88543, 73.44593, -99.16586, -66.02314, 1.981026, 66.77709, -0.1496557, 104.8055, 99.65731, -109.8174, 5.179205, 49.8391, -3.706533, -74.83076, -104.1175, -8.650368, 66.15178, -30.29998, -80.50389, 82.09163, 83.72914, -33.49072]]}, {'10': [[-0.1043486, -13.33695, 100.4732, -88.47826, -36.22219, 137.5589, 74.88473, -64.03402, 10.62998, 90.59745, -12.68498, -118.4803, -94.66031, -14.86983, 61.59597, -9.532911, -0.1306718, 80.96171, 72.87428, -16.04513, -129.0432, -92.98131, 53.23998, 98.26925, 87.46434, -55.59928, -18.25013, 136.7518, -96.01127, -76.50774, 0.9475412, 17.13705, -0.1177734, -35.04586, 95.06115, -25.14559, -93.77893, 64.68454, 117.3286, -33.51221, 5.736861, 56.52369, 91.43999, -31.65752, 31.04222, 28.7196, -108.9172, -87.53994, 0.2069497, -62.7331, -127.3073, 69.2698, 46.56086, -107.2749, 40.27647, 96.79324, -82.11807, 22.40168, 41.10485, -30.54868, -85.98487, -77.2451, 142.2844, -101.1263], [0.1752418, -48.34167, -45.99485, -0.3444633, 16.18074, -76.77022, -31.6993, 92.71541, 1.817501, -49.54332, 37.30521, 161.5148, 158.8612, -103.4736, -17.13124, 54.93356, -0.04444013, 46.92864, 20.20745, -76.62983, -10.99974, 85.5852, -75.4773, -65.34931, 156.6938, -71.63124, -73.66522, 106.181, 30.76204, -139.2391, 102.1765, 83.39052, -0.04757319, 59.31236, 96.31934, -18.43739, 7.472086, 83.60398, -67.43854, -102.6139, 73.42743, 24.92946, -102.246, 17.11113, 70.40063, -72.54376, -39.52789, 120.3372, -0.01507718, -30.62789, -34.65472, 49.34919, 41.75918, -49.7547, 59.09557, 20.63937, -51.11325, 74.02886, -8.737236, -80.67675, 21.77176, 36.81058, -122.7737, -35.39436], [-0.01507718, -30.62789, -34.65472, 49.34919, 41.75918, -49.7547, 59.09557, 20.63937, -51.11325, 74.02886, -8.737236, -80.67675, 21.77176, 36.81058, -122.7737, -35.39436, 0.03242887, -148.9842, 3.941494, 1.163358, 51.48264, 130.9608, -77.76794, -31.89644, 75.27122, -21.84326, -138.0087, -46.95594, 100.4285, -43.6329, -134.5282, 43.25222, 0.09406101, 84.7924, -47.95569, -70.22775, -60.8075, 95.27133, -52.13165, -138.2369, 118.2345, 140.8745, -4.594959, 8.986491, -14.88912, 142.0841, -86.86051, -61.74882, 0.1977495, -66.89752, -92.25333, -136.5463, 61.91156, 111.9172, -98.22142, 38.22547, 109.342, 102.7025, -113.8822, -19.55362, 126.5634, -69.62427, -145.7222, -19.69587], [0.1977495, -66.89752, -92.25333, -136.5463, 61.91156, 111.9172, -98.22142, 38.22547, 109.342, 102.7025, -113.8822, -19.55362, 126.5634, -69.62427, -145.7222, -19.69587, 0.1085225, -163.1385, -89.95663, 68.13913, 109.0995, -137.658, 13.63322, 91.71023, -42.4983, 62.51218, 108.4085, -56.44769, -25.22568, 64.71243, 161.3872, -103.3502, -0.1204935, -121.8866, 44.11933, 131.8055, 39.54119, -78.39206, -21.51241, 168.4483, -82.42186, -51.85623, -3.118003, 110.7248, -58.15444, -167.716, 68.16181, 113.4215, -0.06472819, 53.23997, 44.79729, 135.7889, -105.6051, -49.64223, 55.71906, -0.1380947, -120.1351, -130.1379, 41.99719, 52.40293, -72.97746, -13.01465, 71.25951, 132.6152]]}, {'12': [[0.201909, 109.6816, -84.89796, -27.11821, 173.5033, -102.4539, -47.6832, 89.84548, 32.27638, -59.07192, -79.2338, 108.2876, -57.60692, -60.58772, 89.37287, -69.67218, -0.06205927, 1.887882, 76.41217, 32.33065, -99.78899, -30.16665, 95.60084, -85.06287, -11.05799, 56.23605, -105.6227, 20.23252, 71.61115, -44.20852, -35.34204, 128.2798, 0.1819267, 18.98095, -61.93252, -35.87576, 36.72758, -61.31686, -79.15775, 98.50841, -8.830605, -118.8998, 52.17219, 83.82289, -136.9271, -30.73372, 79.73387, -31.78047, -0.1469519, 99.92157, 48.86704, -16.67245, -39.35848, 114.682, -143.3823, -11.99729, 82.73784, -27.93763, -110.7468, 37.23843, 84.26595, -16.88642, -12.39011, 75.27257], [-0.05060499, 79.61908, 45.24036, 134.7997, -90.4135, -126.7692, -16.60143, 51.20008, -48.92217, -85.88056, 19.1665, -48.49952, 151.8261, -101.8489, -43.89304, 94.66708, -0.1185047, 77.35083, -36.93397, -66.24909, -96.0262, -0.5174332, 89.51703, -164.383, -10.29572, 52.26135, 80.76729, -41.22609, 16.57922, 121.3336, -85.37257, 15.35652, 0.1257225, -163.7942, -146.8397, 74.1098, 49.78936, -83.83316, -57.62743, 90.16026, -16.73098, -118.2901, 63.35203, 54.14778, -15.44832, 36.44562, 102.818, -37.46918, -0.07241192, 31.19582, 32.65739, -39.41261, -147.3487, 84.89903, 53.16864, -129.259, 59.81129, 108.4906, -87.89133, 58.07372, 129.543, 25.00314, -36.86413, 9.037676], [-0.07241192, 31.19582, 32.65739, -39.41261, -147.3487, 84.89903, 53.16864, -129.259, 59.81129, 108.4906, -87.89133, 58.07372, 129.543, 25.00314, -36.86413, 9.037676, -0.05931111, -9.254891, 44.30799, 108.5027, -144.876, -84.2347, 150.2219, 15.67633, -95.72747, -69.5859, 51.29879, 122.4581, -77.52284, -4.438187, 49.28709, 33.79745, -0.149435, 98.29823, 42.76174, -87.41211, -27.4184, -24.01069, 46.80655, -95.2066, -81.70237, 116.9625, 17.31933, -66.48677, 39.83315, 130.7812, 38.54799, -9.94528, 0.04141067, -26.24183, -52.04245, -75.24664, 149.0899, -48.74563, -151.1009, 56.31434, 105.3568, -20.07854, -70.02519, 38.91983, 173.4764, 78.75238, -87.67256, -90.32985], [0.04141067, -26.24183, -52.04245, -75.24664, 149.0899, -48.74563, -151.1009, 56.31434, 105.3568, -20.07854, -70.02519, 38.91983, 173.4764, 78.75238, -87.67256, -90.32985, 0.1431265, 45.20949, -47.03851, -109.921, 57.91627, 117.4757, -137.7378, 55.48093, 117.1168, -66.61363, 3.270416, 19.59726, 71.116, -85.50328, -85.30243, 109.5011, 0.1796545, -99.36991, -149.4189, 42.9202, 133.2463, -13.75969, 1.094508, -6.165476, 102.5665, -96.9052, -110.5412, 53.14275, 88.62674, -98.48755, -63.51204, 112.5766, -0.06991679, -37.52928, 12.85823, -96.89918, -205.2481, 147.0599, 55.13304, -78.61377, -78.98631, 39.39, 178.0739, -123.8706, -70.53348, -28.04102, 81.44475, 45.52984]]}]
pre_cal = {}
proc_calibration = {}

index_pos = dict(zip(["Nc", "Ns", "Nt"], range(3)))

gcca = GCCA_SSVEP(stim_freqs, fs, Nh=Nh)
mset_cca = MsetCCA_SSVEP(stim_freqs)

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

# @app.route('/7hz', methods=["POST"])
# def cal7():
#     data = request.get_json(force=True)
#     cal.append(data)
#     print(cal)
#     return jsonify(msg="successfully received"), 200

@app.route('/7hz', methods=["POST"])
def cal7():
    data = request.get_json(force=True)
    cal[0]['7'].append(data['7'])
    # print(cal[0]['7'])
    print(data)
    return jsonify(msg="successfully received"), 200

@app.route('/10hz', methods=["POST"])
def cal10():
    data = request.get_json(force=True)
    cal[1]['10'].append(data['10'])
    print(data)
    return jsonify(msg="successfully received"), 200

@app.route('/12hz', methods=["POST"])
def cal12():
    data = request.get_json(force=True)
    cal[2]['12'].append(data['12'])
    # print(cal[2]['12'])
    print(data)
    return jsonify(msg="successfully received"), 200

@app.route('/raw', methods=["POST"])
def raw():
    data = request.get_json(force=True)
    # print(cal[2]['12'])
    print(data)
    return jsonify(msg="successfully received"), 200

@app.route('/isCalibrated', methods=["GET"])
def calibrate():
    # print(cal)
    for i in cal:
        for key, value in i.items():
            pre_cal[key] = value
    # print(pre_cal)
    # print(len(pre_cal['7'][0]))
    tests = {
            7: ['7'], 
            10: ['10'], 
            12: ['12']
        }

    for f, test_set in tests.items():
        proc_calibration[f] = []
        
        for test in test_set:
            values = pre_cal[test]
            proc_data = np.array([values[i] for i in range(len(values))])
            proc_calibration[f].append(proc_data[:, :Ns].reshape((1, Ns, -1)))

    # print(proc_calibration)
    # del all_data    

    for f, proc_data in proc_calibration.items():
        if len(proc_data) <= 1:
            proc_calibration[f] = proc_data[0]
        else:
            proc_calibration[f] = np.concatenate([*proc_data], axis=-1) # merge data from across trials
    # print(proc_calibration)
    
    data_tensor = np.array([test_set[:, :, :] for test_set in proc_calibration.values()])

    print("Data tensor shape: ", data_tensor.shape)

    gcca.fit(data_tensor)
    mset_cca.fit(data_tensor)

    # print(data_tensor[0,:,:,0].shape)
    # print(mset_cca.classify(data_tensor[0,:,:,0]))
    return "calibrated", 200

@app.route('/decode', methods=["POST"])
def decoding():
    decode_data = request.get_json(force=True)
    decode_data = np.array(decode_data['raw_data']).reshape(1,Ns)
    # print(decode_data.shape)
    # print(decode_data)

    mset_res = mset_cca.classify(decode_data)
    gcca_res = gcca.classify(decode_data)
    highest_mset = 0
    highest_mset_freq = -1

    for freq, acc in mset_res.items():
            if abs(acc) > highest_mset:
                highest_mset_freq = freq
                highest_mset = abs(acc)

    print(highest_mset_freq, highest_mset)

    highest_gcca = 0
    highest_gcca_freq = -1

    for freq, acc in gcca_res.items():
            if abs(acc) > highest_gcca:
                highest_gcca_freq = freq
                highest_gcca = abs(acc)

    print(highest_gcca_freq, highest_gcca)

    return jsonify(msg="successfully received"), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
