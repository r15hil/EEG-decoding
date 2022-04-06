import gc
from micropython import alloc_emergency_exception_buf
from lib.requests import MicroWebCli as requests
from lib.utils import load_env_vars
import ujson as json
from lib.utils import connect_wifi, load_env_vars
from ulab import numpy as np
import utime as time
from lib.runner import Runner 

ssid = 'Rishil'
password = 'rishilhotspot'
connect_wifi(ssid, password)
time.sleep(4)
runner = Runner('CCA', buffer_size=256)
runner.setup()

runner.run()
time.sleep(4)

while True:
    time.sleep(4)
    data = runner.periph_manager.read_adc_buffer()
    toSend = {"raw_data":data}
    print(toSend)
#     requests.JSONRequest("http://192.168.0.13:5001/collect", toSend)
    requests.JSONRequest("http://172.20.10.2:5001/collect", toSend)
    del data
    del toSend
    requests.GETRequest("http://172.20.10.2:5001/save")
    

# requests.GETRequest("http://192.168.0.13:5001/save")
requests.GETRequest("http://172.20.10.2:5001/save")


runner.stop()