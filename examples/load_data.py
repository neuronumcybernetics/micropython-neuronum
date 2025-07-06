import micropython_neuronum as neuronum

cell = neuronum.Cell(
    host="host",
    password="password",
    network="neuronum.net",
    synapse="synapse"
)

# Load and access stored data
label = "mylabel"
data = cell.load(label)
value = data["key"]
print(value)