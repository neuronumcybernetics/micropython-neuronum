import network
import time
import ujson
import bluetooth

ble = bluetooth.BLE()
ble.active(True)

def activate_ble(node_id, node_name, discoverable):
    if discoverable:
        adv_payload = bytearray(b'\x02\x01\x06')
        adv_payload += bytearray((len(node_id) + 1, 0x09)) + node_id

        full_name = f"{node_name}_{node_id}"
        
        scan_resp_payload = bytearray((len(node_name) + 1, 0x09)) + node_name

        ble.gap_advertise(100_000, adv_payload, resp_data=scan_resp_payload)
        
        print(f"Node {full_name} is discoverable")
    else:
        ble.gap_advertise(None)
        print("Node is not discoverable")

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print(f"Connecting to Wi-Fi: {ssid}")
    timeout = 30
    start_time = time.time()

    while not wlan.isconnected() and (time.time() - start_time < timeout):
        print("Attempting Wi-Fi connection...")
        time.sleep(1)

    if wlan.isconnected():
        print("Connected! IP Address:", wlan.ifconfig()[0])
    else:
        print("Wi-Fi connection failed. Starting AP mode...")

try:
    with open("config.json", "r") as f:
        config = ujson.load(f)
        ssid = config.get("ssid", "not_assigned")
        password = config.get("password", "not_assigned")
        node_id = config.get("node_id", "not_assigned")
        node_name = config.get("node_name", "not_assigned")
        discoverable = config.get("discoverable", "not_assigned")
        print(f"SSID: {ssid}, Password: {password}, Node ID: {node_id}, Node Name: {node_name}, Discoverable: {discoverable}")
except Exception as e:
    print("Error loading config:", e)
    ssid, password = "not_assigned", "not_assigned"


connect_to_wifi(ssid, password)
activate_ble(node_id, node_name, discoverable)


