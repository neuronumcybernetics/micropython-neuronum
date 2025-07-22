import micropython_neuronum as neuronum

cell = neuronum.Cell(
    host="host",
    password="password",
    network="neuronum.net",
    synapse="synapse"
)
     
STX = "id::stx"
for operation in cell.sync(STX):  
    txID = operation.get("txID")
    client = operation.get("operator")                      
    if txID == "id::tx":             
        data = {
            "json": f"Hello {client}",
            "html": f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Greeting Node</title>
  </head>
  <body>
    <div class="card">
      <h1>Hello, {client}</h1>
    </div>
  </body>
</html>
"""
        }
        cell.tx_response(txID, client, data)

