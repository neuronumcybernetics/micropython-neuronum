import micropython_neuronum as neuronum

cell = neuronum.Cell(
    host="host",
    password="password",
    network="neuronum.net",
    synapse="synapse"
)

# Stream data to your private Stream (STX)
label = "label"
data = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3",
}
cell.stream(label, data)

# Stream data to a public Stream (STX)
STX = "id::stx"
label = "label"
data = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3",
}
cell.stream(label, data, STX)