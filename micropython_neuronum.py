import usocket
import ujson
import ssl
import urequests as requests


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

    def stream(self, label, data, stx=None):
        try:
            addr = usocket.getaddrinfo(self.network, 55555)[0][-1]
            sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
            sock.connect(addr)

            sock = ssl.wrap_socket(sock)

            credentials = f"{self.host}\n{self.password}\n{self.synapse}\n{stx}\n"
            sock.send(credentials.encode("utf-8"))

            response = sock.recv(1024).decode("utf-8")

            if "Authentication successful" not in response:
                print("Authentication failed")
                sock.close()
                return

            stream_payload = ujson.dumps({"label": label, "data": data})
            sock.send(stream_payload.encode("utf-8"))
            response_text = sock.recv(1024).decode("utf-8")
            if response_text == "Sent":
                    print(f"Success: {response_text} - {stream_payload}")
            else:
                print(f"Error sending: {stream_payload}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            sock.close()


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
