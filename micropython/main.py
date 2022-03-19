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

from ulab import numpy as np
import utime as time
from lib.runner import Runner  

runner = Runner('CCA', buffer_size=256)
runner.setup()
runner.run()

p26.off()
p13.off()

print(2)
time.sleep(5)

p26.on()
p13.on()

env_vars = load_env_vars("lib/.env")
ssid = env_vars.get("WIFI_SSID")
password = env_vars.get("WIFI_PASSWORD")
connect_wifi(ssid, password)
# ssid = 'vodafone749282'
# password = 'c4Eqssga2YAdAZ97'
# connect_wifi(ssid, password)

while True:
    time.sleep(4)
    # time.sleep(2)
    data = runner.periph_manager.read_adc_buffer()
    toSend = {"raw_data":data}
    print(toSend)
    requests.JSONRequest("http://192.168.0.13:5001/raw", toSend)
#     requests.JSONRequest("http://192.168.1.106:5001/decode", toSend)
    # requests.JSONRequest("http://172.20.10.2:5001/decode", toSend) 
    del data
    print(gc.mem_free())
    gc.collect()
    print(gc.mem_free())