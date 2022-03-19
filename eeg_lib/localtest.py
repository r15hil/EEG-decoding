from codecs import xmlcharrefreplace_errors
import json
import sys
import time
import numpy as np
import pandas as pd
from cca import GCCA_SSVEP
from cca import MsetCCA_SSVEP
from cal import cal, test7hz, test10hz, test12hz
from cal1 import cal1, test12hz1, test10hz1, test7hz1

def calibrate():
    # print(cal)
    for i in cal1:
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
    return data_tensor

def decoding(decode_data):
    decode_data = np.array(decode_data).reshape(1,Ns)
    # print(decode_data.shape)
    # print(decode_data[0][0])

    # print(mset_cca.classify(decode_data))
    # print(gcca.classify(decode_data))
    return mset_cca.classify(decode_data)



stim_freqs = [7,10,12] # stim freqs used
fs = 256 # sampling freq
Ns = 256 # number of sample points to consider
Nh = 1 # number of harmonics for CCA-based algos

index_pos = dict(zip(["Nc", "Ns", "Nt"], range(3)))


stim_freqs = [7,10,12] # stim freqs used
fs = 256 # sampling freq
Ns = 256 # number of sample points to consider
Nh = 1 # number of harmonics for CCA-based algos

# cal = [{'7':[]},{'10':[]},{'12':[]}]

pre_cal = {}
proc_calibration = {}
gcca = GCCA_SSVEP(stim_freqs, fs, Nh=Nh)
mset_cca = MsetCCA_SSVEP(stim_freqs)
mset_cca_pynb = MsetCCA_SSVEP(stim_freqs)

from utils import read_json
import json

tests = {7: ["7hz"], 
         10: ["10hz"], 
         12: ["12hz"]
        }

# all_data = read_json('/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/logs/combined.json')
all_data = read_json('/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/logs/combined.json')
data = {}

for f, test_set in tests.items():
    data[f] = []
    
    for test in test_set:
        values = all_data[test]
        proc_data = np.array([values[i] for i in range(len(values))])
        data[f].append(proc_data[1:, :Ns].reshape((1, Ns, -1))) # exclude first trial


# del all_data    

for f, proc_data in data.items():
    if len(proc_data) <= 1:
        data[f] = proc_data[0]
    else:
        data[f] = np.concatenate([*proc_data], axis=-1) # merge data from across trials

min_trial_len = np.min([test_set.shape[-1] for test_set in data.values()])
data_tensor = np.array([test_set[:, :, :min_trial_len] for test_set in data.values()])

train_this = calibrate()
chi_train = data_tensor[:, :, :, [1,2,3,4]]

print(train_this,"========",chi_train)

mset_cca_pynb.fit(chi_train)

X_test = test7hz[1]

print(decoding(X_test),mset_cca_pynb.classify(np.array(X_test).reshape(1,Ns)))
# index_pos = dict(zip(["Nc", "Ns", "Nt"], range(3)))

# mset_cca.fit(chi_train)

# for i in X_test:

#     mset_res = decoding(i)
#     mset_cca_pynb_res = mset_cca.classify(np.array(i).reshape(1,256))
#     highest_mset = 0
#     highest_mset_freq = -1
#     highest_mset1 = 0
#     highest_mset_freq1 = -1

#     for freq, acc in mset_res.items():
#         if abs(acc) > highest_mset:
#             highest_mset_freq = freq
#             highest_mset = abs(acc)

#     for freq, acc in mset_cca_pynb_res.items():
#         if abs(acc) > highest_mset1:
#             highest_mset_freq1 = freq
#             highest_mset1 = abs(acc)

#     print(highest_mset_freq, highest_mset_freq1 )
#     if 12 == highest_mset_freq:
#         print("CORRECT:", highest_mset_freq)
#     else:
#         print("WRONG:", highest_mset_freq)