import micropython_neuronum as neuronum

cell = neuronum.Cell(
    host="host",
    password="password",
    network="neuronum.net",
    synapse="synapse"
)

# Sync data of your private Stream (STX)
for operation in cell.sync():
    label = operation.get("label")
    data = operation.get("data")
    ts = operation.get("time")
    stxID = operation.get("stxID")
    operator = operation.get("operator")
    print(label, data, ts, stxID, operator)

# Sync data of a public Stream (STX)
STX = "id::stx"
for operation in cell.sync(STX):
    label = operation.get("label")
    data = operation.get("data")
    ts = operation.get("time")
    stxID = operation.get("stxID")
    operator = operation.get("operator")
    print(label, data, ts, stxID, operator)