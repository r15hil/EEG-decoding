import gc
from micropython import alloc_emergency_exception_buf
from lib.requests import MicroWebCli as requests
from lib.utils import load_env_vars
import ujson as json
from lib.utils import connect_wifi, load_env_vars

# allocate exception buffer for ISRs
alloc_emergency_exception_buf(100)

# enable and configure garbage collection
gc.enable()
gc.collect()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

from machine import Pin
import time

p26 = Pin(26, Pin.OUT)  #green
p13 = Pin(13, Pin.OUT)  #red
buttonA = Pin(32, Pin.IN)
buttonB = Pin(34, Pin.IN)
p26.on()
p13.on()

# time.sleep(5)

# p26.off()
# p13.off()

# time.sleep(5)

from ulab import numpy as np
import utime as time
from lib.runner import Runner  


def preprocess_data(signal):
    
    """Preprocess incoming signal before decoding algorithms.
    This involves applying a bandpass filter to isolate the target SSVEP range
    and then downsampling the signal to the Nyquist boundary.
    
    Returns:
        [np.ndarray]: filtered and downsampled signal
    """
    downsample_freq = 64
    ds_factor = 256//downsample_freq
    return signal[::ds_factor]

def collectData(decode_period_s):
    
    global runner
    
    time.sleep(decode_period_s)
    data = preprocess_data(runner.output_buffer)
    gc.collect()
    return data

def getData(Nt, decode_period_s):

    global runner
    global p26

    runner.run()
    
    trials = []
    time.sleep(5)
    count=0
    
    toggle = True

    if Nt <=1:
        return collectData(decode_period_s)
    for i in range(Nt):
        if toggle:
            p26.on()
            toggle = False
        else:
            p26.off()
            toggle = True

        trials.append(collectData(decode_period_s))
        
    runner.stop()

    gc.collect()
    p26.off()
    return trials

print(1)

decode_period_s = 4 # decode every x seconds
Ns = 256
Nt = 4
stim_freqs = [7, 10, 12]

runner = Runner('CCA', buffer_size=Ns)
runner.setup()

p26.off()
p13.off()

calibration_data = {}
print(2)
time.sleep(5)

p26.on()
p13.on()

env_vars = load_env_vars("lib/.env")
ssid = env_vars.get("WIFI_SSID")
password = env_vars.get("WIFI_PASSWORD")
connect_wifi(ssid, password)

calibration_data[7] = getData(Nt, decode_period_s)
toSend = {"7": calibration_data[7]}
requests.JSONRequest("http://192.168.0.13:5001/7hz", toSend)
del calibration_data[7]
print(gc.mem_free())
gc.collect()
print(gc.mem_free())
p26.off()
p13.on()
time.sleep(5)
calibration_data[10] = getData(Nt, decode_period_s)
print("=====================================================")
toSend = {"10": calibration_data[10]}
requests.JSONRequest("http://192.168.0.13:5001/10hz", toSend)
del calibration_data[10]
print(gc.mem_free())
gc.collect()
print(gc.mem_free())
p26.off()
p13.on()
time.sleep(5)
calibration_data[12] = getData(Nt, decode_period_s)
toSend = {"12": calibration_data[12]}
requests.JSONRequest("http://192.168.0.13:5001/12hz", toSend)
del calibration_data
print(gc.mem_free())
gc.collect()
print(gc.mem_free())
p26.off()
p13.on()
time.sleep(5)

requests.GETRequest("http://192.168.0.13:5001/isCalibrated")
print(3)
runner.run()

while True:
    time.sleep(4)
    data = preprocess_data(runner.output_buffer)
    toSend = {"raw_data_downsampled":data}
    requests.JSONRequest("http://192.168.0.13:5001/decode", toSend)