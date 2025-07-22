import micropython_neuronum as neuronum

cell = neuronum.Cell(
    host="host",
    password="password",
    network="neuronum.net",
    synapse="synapse"
)

TX = "id::tx"                                                           # select the Transmitter TX
client = "id::cell"                                                     # select the Client Cell 
data = {                                                                # enter response key value data 
    "json": "value",
    "html": "value"
}
cell.tx_response(TX, client, data)                                      # respond TX - > get success message back