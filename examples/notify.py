import micropython_neuronum as neuronum

cell = neuronum.Cell(
    host="host",
    password="password",
    network="neuronum.net",
    synapse="synapse"
)

# Send Notification
receiver = "receiver::cell"
title = "notification_title"
message = "notification_message"
cell.notify(receiver, title, message)