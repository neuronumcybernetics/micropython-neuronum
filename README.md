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

### **Installation**
Ensure your MicroPython device is **connected to Wi-Fi** before installation.

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
