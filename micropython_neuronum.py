import usocket
import ujson
import ssl
import urequests as requests
import uwebsockets.client
import utime


class Cell:
    def __init__(self, host: str, password: str, network: str, synapse: str):
        self.host = host
        self.password = password
        self.network = network
        self.synapse = synapse


    def to_dict(self):
        return {
            "host": self.host,
            "password": self.password,
            "synapse": self.synapse
        }


    def __repr__(self):
        return f"Cell(host={self.host}, password={self.password}, network={self.network}, synapse={self.synapse})"


    def stream(self, label, data, stx=None, retry_delay=3):
        while True:
            sock = None
            try:
                addr = usocket.getaddrinfo(self.network, 55555)[0][-1]
                sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
                sock.connect(addr)

                sock = ssl.wrap_socket(sock)

                credentials = f"{self.host}\n{self.password}\n{self.synapse}\n{stx}\n"
                sock.send(credentials.encode("utf-8"))

                response = sock.recv(1024).decode("utf-8")

                if "Authentication successful" not in response:
                    print("Authentication failed, retrying...")
                    sock.close()
                    return

                stream_payload = ujson.dumps({"label": label, "data": data})
                sock.send(stream_payload.encode("utf-8"))
                response_text = sock.recv(1024).decode("utf-8")

                if response_text == "Sent":
                    print(f"Success: {response_text} - {stream_payload}")
                    break
                else:
                    print(f"Error sending: {stream_payload}")
                    utime.sleep(retry_delay)

            except Exception as e:
                print(f"Error: {e}, retrying...")
                utime.sleep(retry_delay)

            finally:
                if sock:
                    sock.close()



    def sync(self, stx: str = None):
        full_url = f"wss://{self.network}/sync/{stx}"

        auth_payload = {
            "host": self.host,
            "password": self.password,
            "synapse": self.synapse,
        }

        while True:
            try:
                ws = uwebsockets.client.connect(full_url)
                print(f"Connecting to {full_url}")

                ws.send(ujson.dumps(auth_payload))

                try:
                    while True:
                        raw_operation = ws.recv()
                        if raw_operation is None:
                            print("No data received. Connection might be closed or timed out.")
                            break
                        
                        operation = ujson.loads(raw_operation)
                        yield operation

                except Exception as e:
                    print(f"Error during data reception: {e}")
                finally:
                    ws.close()
                    print("Connection closed.")

            except Exception as e:
                print(f"An error occurred: {e}")
            
            utime.sleep(3)


    def activate_tx(self, txID: str, data: dict):
        url = f"https://{self.network}/api/activate_tx/{txID}"
        TX = {
            "data": data,
            "cell": self.to_dict()
        }

        try:
            response = requests.post(url, json=TX)
            if response.status_code != 200:
                print(f"HTTP {response.status_code}: {response.text}")
                return

            try:
                data = response.json()
            except Exception as e:
                print("Failed to parse JSON:", e)
                return

            if data.get("success") is True:
                resp = data.get("response", {})
                if "json" in resp:
                    return resp.get("json")
                elif "html" in resp:
                    return "Info: HTML response available. Please activate TX in browser."
                else:
                    return "Info: Response received but contains no usable content."
            else:
                print("Server returned error:", data.get("message"))

        except Exception as e:
            print(f"Request failed: {e}")


    def store(self, label: str, data: dict, ctx: str = None):
        if ctx:
            full_url = f"https://{self.network}/api/store_in_ctx/{ctx}"
        else:
            full_url = f"https://{self.network}/api/store"

        store_payload = {
            "label": label,
            "data": data,
            "cell": self.to_dict()
        }

        try:
            response = requests.post(full_url, json=store_payload)
            if response.status_code != 200:
                print(f"HTTP {response.status_code}: {response.text}")
                return

            try:
                response_data = response.json()
            except Exception as e:
                print("Failed to parse JSON:", e)
                return

            print(f"Response from Neuronum: {response_data}")
            return response_data

        except Exception as e:
            print(f"Request failed: {e}")


    def load(self, label: str, ctx: str = None):
        if ctx:
            full_url = f"https://{self.network}/api/load_from_ctx/{ctx}"
        else:
            full_url = f"https://{self.network}/api/load"

        load_payload = {
            "label": label,
            "cell": self.to_dict()
        }

        try:
            response = requests.post(full_url, json=load_payload)

            if response.status_code != 200:
                print(f"HTTP {response.status_code}: {response.text}")
                return

            try:
                data = response.json()
                return data
            except Exception as e:
                print("Failed to parse JSON:", e)
                return

        except Exception as e:
            print(f"Request failed: {e}")


    def tx_response(self, txID: str, client: str, data: dict):
        url = f"https://{self.network}/api/tx_response/{txID}"

        tx_response = {
            "client": client,
            "data": data,
            "cell": self.to_dict()
        }

        try:
            for _ in range(2):
                response = requests.post(url, json=tx_response)

                if response.status_code != 200:
                    print(f"HTTP {response.status_code}: {response.text}")
                    return

                try:
                    data = response.json()
                    print(data["message"])
                except Exception as e:
                    print("Failed to parse JSON:", e)
                    return

        except Exception as e:
            print(f"Request failed: {e}")


    def notify(self, receiver: str, title: str, message: str):
        full_url = f"https://{self.network}/api/notify"

        notify_payload = {
            "receiver": receiver,
            "notification": {
                "title": title,
                "message": message
            },
            "cell": self.to_dict()
        }

        try:
            response = requests.post(full_url, json=notify_payload)
            if response.status_code != 200:
                print(f"HTTP {response.status_code}: {response.text}")
                return

            try:
                response_data = response.json()
            except Exception as e:
                print("Failed to parse JSON:", e)
                return

            print(f"Response from Neuronum: {response_data}")
            return response_data

        except Exception as e:
            print(f"Request failed: {e}")