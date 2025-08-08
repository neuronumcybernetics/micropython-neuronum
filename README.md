<h1 align="center">
  <img src="https://neuronum.net/static/neuronum.svg" alt="Neuronum" width="80">
</h1>
<h4 align="center">The MicroPython implementation of the Neuronum client library</h4>

<p align="center">
  <a href="https://neuronum.net">
    <img src="https://img.shields.io/badge/Website-Neuronum-blue" alt="Website">
  </a>
  <a href="https://github.com/neuronumcybernetics/micropython-neuronum">
    <img src="https://img.shields.io/badge/Docs-Read%20now-green" alt="Documentation">
  </a>
  <a href="https://github.com/neuronumcybernetics/neuronum/blob/main/LICENSE.md">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
</p>

---

### **About micropython-neuronum**
The **MicroPython implementation** of the [Neuronum client library](https://pypi.org/project/neuronum/) — actively developed and tested on ESP32.

Firmware Version: MicroPython v1.25.0 on 2025-04-15; Generic ESP32 module with ESP32<br>
Download and flash your ESP: https://micropython.org/download/ESP32_GENERIC/

### **Installation**
#### **Set configs + connect To Wifi**
config.json
```json
{
  "ssid": "your_ssid",
  "password": "your_password",
  "node_id": "your_node_id",
  "discoverable": true
}
```

boot.py
```python
import network
import time
import ujson
import bluetooth

ble = bluetooth.BLE()
ble.active(True)

def activate_ble(node_id, discoverable):
    if discoverable == True:
        device_name = node_id
        name_bytes = device_name.encode()

        advertising_payload = bytearray(b'\x02\x01\x06')
        advertising_payload += bytearray((len(name_bytes) + 1, 0x09)) + name_bytes

        ble.gap_advertise(100_000, advertising_payload)
        print(f"Node {device_name} discoverable")
    else:
        print(f"Node {device_name} not discoverable")

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print(f"Connecting to Wi-Fi: {ssid}")
    timeout = 30
    start_time = time.time()

    while not wlan.isconnected() and (time.time() - start_time < timeout):
        print("Attempting Wi-Fi connection...")
        time.sleep(1)

    if wlan.isconnected():
        print("Connected! IP Address:", wlan.ifconfig()[0])
    else:
        print("Wi-Fi connection failed. Starting AP mode...")

try:
    with open("config.json", "r") as f:
        config = ujson.load(f)
        ssid = config.get("ssid", "not_assigned")
        password = config.get("password", "not_assigned")
        node_id = config.get("node_id", "not_assigned")
        discoverable = config.get("discoverable", "not_assigned")
        print(f"SSID: {ssid}, Password: {password}, Node ID: {node_id}, Discoverable: {discoverable}")
except Exception as e:
    print("Error loading config:", e)
    ssid, password = "not_assigned", "not_assigned"


connect_to_wifi(ssid, password)
activate_ble(node_id, discoverable)
```

#### **Install the MicroPython-Neuronum Library using mip**
```python
import mip
mip.install("github:neuronumcybernetics/micropython-neuronum")
```

This will either create a /lib folder containing or add the following files to an existing /lib folder:
- micropython_neuronum.py
- /uwebsockets/client.py
- /uwebsockets/protocol.py


### **Sync Stream Data in Real Time with your ESP** **[(More Examples Here)](https://github.com/neuronumcybernetics/micropython-neuronum/tree/main/examples)**
Create, upload, and run this sync.py file on your ESP
```python
import micropython_neuronum as neuronum

cell = neuronum.Cell(
    host="host",                # replace with your cell host
    password="password",        # replace with your cell password
    network="neuronum.net",     # choose the network -> neuronum.net
    synapse="synapse"           # replace with your cell synapse (auth token)
)

# Sync data of a public Stream (STX) gy3w11qAEibN::stx
STX = "gy3w11qAEibN::stx"
for operation in cell.sync(STX):
    label = operation.get("label")
    data = operation.get("data")
    ts = operation.get("time")
    stxID = operation.get("stxID")
    operator = operation.get("operator")
    print(label, data, ts, stxID, operator)
```
