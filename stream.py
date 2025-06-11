import micropython_neuronum as neuronum

cell = neuronum.Cell(
    host="host",
    password="password",
    network="neuronum.net",
    synapse="synapse"
)

label = "label"
data = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3",
}
cell.stream(label, data)

