import micropython_neuronum as neuronum

cell = neuronum.Cell(
    host="host",
    password="password",
    network="neuronum.net",
    synapse="synapse"
)

# Store data
label = "mylabel"
data = {"key": "value"}
cell.store(label, data)