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

p26.on()
p13.on()

time.sleep(5)

from lib.runner import OnlineRunner
from lib.logging import logger_types

#api_host = "http://172.20.10.2:5001/" # make sure the port corresponds to your logging server configuration

decode_period_s = 4 # decode every x seconds
Ns = 256
Nt = 3

api_host = "http://192.168.0.13:5001/"

log_params = dict(server=api_host, 
                  log_period=4, 
                  logger_type=logger_types.HTTP, 
                  send_raw=True, 
                  session_id='open_eyes')

runner = OnlineRunner('CCA', buffer_size=Ns)
runner.setup(**log_params)

runner.run()