from cca import GCCA_SSVEP
from cca import MsetCCA_SSVEP
from utils import read_json
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# set global plotting params here for consistency
plt.style.use('styles.mplstyle')
palette = ['#0b528c', '#7170b6', '#b86eb2', '#ec7098', '#ff8572', '#ffaa4f']

from cycler import cycler
plt.rc('axes', prop_cycle=cycler('color', palette[::2]+palette[-1:]))

stim_freqs = [7,10,12] # stim freqs used
fs = 256 # sampling freq
Ns = 256 # number of sample points to consider
Nh = 1 # number of harmonics for CCA-based algos

index_pos = dict(zip(["Nc", "Ns", "Nt"], range(3)))

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


                  
stim_freqs = [7,10,12]
fs= 256
Nh = 1

min_trial_len = np.min([test_set.shape[-1] for test_set in data.values()])

# Nf x Nc x Ns x Nt
data_tensor = np.array([test_set[:, :, :min_trial_len] for test_set in data.values()])

print("Data tensor shape: ", data_tensor.shape)

gcca = GCCA_SSVEP(stim_freqs, fs, Nh=Nh)
mset_cca = MsetCCA_SSVEP(stim_freqs)

chi_train = data_tensor[:, :, :, [6,7,8,9]]
print(chi_train.shape)
                        
gcca.fit(chi_train)
mset_cca.fit(chi_train)

X_test = data_tensor[0, :, :, 6]

results_gcca = {'correct':0,
                'incorrect':0}
results_mset = {'correct':0,
                'incorrect':0}

for i in range(data_tensor.shape[0]):
    for j in range(6):
        print(i,j)
        X_test = data_tensor[i, :, :, j]
#         print("=============================================")
#         print(X_test)
#         print("=============================================")
        gcca_res = gcca.classify(X_test)
        mset_res = mset_cca.classify(X_test)

        highest_gcca = 0
        highest_gcca_freq = -1
        for freq, acc in gcca_res.items():
            if abs(acc) > highest_gcca:
                highest_gcca_freq = freq
                highest_gcca = abs(acc)

        if stim_freqs[i] == highest_gcca_freq:
            results_gcca['correct']+=1
        else:
            results_gcca['incorrect']+=1

        highest_mset = 0
        highest_mset_freq = -1
        for freq, acc in mset_res.items():
            if abs(acc) > highest_mset:
                highest_mset_freq = freq
                highest_mset = abs(acc)
        if stim_freqs[i] == highest_mset_freq:
            results_mset['correct']+=1
            print("CORRECT:", highest_mset_freq)
        else:
            print("WRONG:", highest_mset_freq)
            results_mset['incorrect']+=1

print("GCCA", results_gcca)
print("Mset", results_mset)