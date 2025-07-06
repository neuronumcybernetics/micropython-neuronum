import micropython_neuronum as neuronum

cell = neuronum.Cell(
    host="host",
    password="password",
    network="neuronum.net",
    synapse="synapse"
)

# Activate transitter
TX = "id::tx"
data = {"say": "hello"}
tx_response = cell.activate_tx(TX, data)
print(tx_response)