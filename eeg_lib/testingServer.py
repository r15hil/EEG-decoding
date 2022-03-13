import requests
import time
from cal1 import cal1

data = cal1[0]['7'][0]
toSend = {"7":data}
print(toSend)
x = requests.post("http://192.168.0.13:5001/7hz", json=toSend)

print(x.text)