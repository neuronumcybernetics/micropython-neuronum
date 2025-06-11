import usocket
import ujson
import ssl

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
            print(f"Sent: {stream_payload}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            sock.close()


__all__ = ['Cell']




