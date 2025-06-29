import micropython_neuronum as neuronum

cell = neuronum.Cell(
    host="host",
    password="password",
    network="neuronum.net",
    synapse="synapse"
)

# Stream data
label = "label"
data = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3",
}
cell.stream(label, data)

# Activate transitter
TX = "ICfyWjdExPBh::tx"
data = {"say": "hello"}
tx_response = cell.activate_tx(TX, data)
print(tx_response)

# Store data
label = "mylabel"
data = {"key": "value"}
cell.store(label, data)

# Load and access stored data
label = "mylabel"
data = cell.load(label)
value = data["key"]
print(value)
