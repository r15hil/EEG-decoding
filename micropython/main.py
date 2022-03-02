# import gc
# from micropython import alloc_emergency_exception_buf

# # allocate exception buffer for ISRs
# alloc_emergency_exception_buf(100)

# # enable and configure garbage collection
# gc.enable()
# gc.collect()
# gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

# from machine import Pin
# import time

# p26 = Pin(26, Pin.OUT)  #green
# p13 = Pin(13, Pin.OUT)  #red
# buttonA = Pin(32, Pin.IN)
# buttonB = Pin(34, Pin.IN)
# p26.on()
# p13.on()

# counter = 0
# while counter !=10:
#     if (counter % 2 == 0):
#         p26.on()
#         p13.off()
#     else:
#         p13.on()
#         p26.off()
#     time.sleep(1)
#     counter+=1

# p26.off()
# p13.off()

# time.sleep(5)

# from lib.utils import connect_wifi, load_env_vars

# # env_vars = load_env_vars("lib/.envh")
# # # connect WiFI
# # ssid = env_vars.get("WIFI_SSID")
# # password = env_vars.get("WIFI_PASSWORD")
# # ssid ="Rishil"
# # password = "rishilhotspot"
# # connect_wifi(ssid, password)

# # # import webrepl
# # # webrepl.start()

# p26.on()
# p13.on()

# time.sleep(5)

# from ulab import numpy as np
# import utime as time
# from lib.runner import Runner

# def collectData(decode_period_s):
    
#     global runner
    
#     time.sleep(decode_period_s)
#     data = runner.output_buffer
#     gc.collect()
#     return np.array(data)

# def getData(Nt, decode_period_s):

#     global runner
#     global p26

#     runner.run()
    
#     trials = []
#     time.sleep(5)
#     count=0
    
#     toggle = True

#     if Nt <=1:
#         return collectData(decode_period_s)
#     for i in range(Nt):
#         if toggle:
#             p26.on()
#             toggle = False
#         else:
#             p26.off()
#             toggle = True

#         trials.append(collectData(decode_period_s).flatten())
        
#     runner.stop()

#     gc.collect()
#     p26.off()
#     return np.array(trials)

# print(1)

# decode_period_s = 4 # decode every x seconds
# Nc = 1
# Ns = 128
# Nt = 3
# stim_freqs = [7, 10, 12]

# runner = Runner('CCA', buffer_size=Ns)
# runner.setup() 

# p26.off()
# p13.off()

# calibration_data = {}
# print(2)
# time.sleep(5)

# p26.on()
# p13.on()

# calibration_data[7] = getData(Nt, decode_period_s)
# print(gc.mem_free())
# gc.collect()
# print(gc.mem_free())
# p26.off()
# p13.on()
# time.sleep(5)
# calibration_data[10] = getData(Nt, decode_period_s)
# print(gc.mem_free())
# gc.collect()
# print(gc.mem_free())
# p26.off()
# p13.on()
# time.sleep(5)
# calibration_data[12] = getData(Nt, decode_period_s)
# print(gc.mem_free())
# gc.collect()
# print(gc.mem_free())
# p26.off()
# p13.on()
# time.sleep(5)

# p26.on()
# p13.on()

# time.sleep(5)

# p26.on()
# p13.off()

# time.sleep(5)

# print(3)

# del runner

# from lib.runner import OnlineRunner
# from lib.logging import logger_types

# api_host = "http://172.20.10.2:5001/" # make sure the port corresponds to your logging server configuration

# log_params = dict(server=api_host, 
#                   log_period=4, 
#                   logger_type=logger_types.HTTP, 
#                   send_raw=True, 
#                   session_id='hotspot_test_device')

# runner = OnlineRunner('MsetCCA', buffer_size=Ns)
# runner.setup(**log_params)

# runner.calibrate(calibration_data)
# runner.run()

import gc
from micropython import alloc_emergency_exception_buf

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

counter = 0
while counter !=10:
    if (counter % 2 == 0):
        p26.on()
        p13.off()
    else:
        p13.on()
        p26.off()
    time.sleep(1)
    counter+=1

p26.off()
p13.off()

time.sleep(5)

from lib.utils import connect_wifi, load_env_vars

p26.on()
p13.on()

time.sleep(5)

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
    from lib.signal import sos_filter
    downsample_freq = 64
    ds_factor = 256//downsample_freq
    return sos_filter(signal)[::ds_factor]

def collectData(decode_period_s):
    
    global runner
    
    time.sleep(decode_period_s)
    data = preprocess_data(runner.output_buffer)
    gc.collect()
    return np.array(data)

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

        trials.append(collectData(decode_period_s).flatten())
        
    runner.stop()

    gc.collect()
    p26.off()
    return np.array(trials)

print(1)

decode_period_s = 4 # decode every x seconds
Nc = 1
Ns = 256
Nt = 3
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

calibration_data[7] = getData(Nt, decode_period_s)
print(gc.mem_free())
gc.collect()
print(gc.mem_free())
p26.off()
p13.on()
time.sleep(5)
calibration_data[10] = getData(Nt, decode_period_s)
print(gc.mem_free())
gc.collect()
print(gc.mem_free())
p26.off()
p13.on()
time.sleep(5)
calibration_data[12] = getData(Nt, decode_period_s)
print(gc.mem_free())
gc.collect()
print(gc.mem_free())
p26.off()
p13.on()
time.sleep(5)

p26.on()
p13.on()

time.sleep(5)

p26.on()
p13.off()

time.sleep(5)

print(3)

del runner

from lib.runner import OnlineRunner
from lib.logging import logger_types

api_host = "http://172.20.10.2:5001/" # make sure the port corresponds to your logging server configuration

log_params = dict(server=api_host, 
                  log_period=4, 
                  logger_type=logger_types.HTTP, 
                  send_raw=True, 
                  session_id='downsample_test')

runner = OnlineRunner('MsetCCA', buffer_size=Ns)
runner.setup(**log_params)

runner.calibrate(calibration_data)
runner.run()
