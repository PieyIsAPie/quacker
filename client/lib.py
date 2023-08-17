import socket
import core.msgcrypt

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self, username, color, password=None):
        self.client.connect((self.host, self.port))

        connect_message = f"CONNECT:{username}/{color}"
        self.client.sendall(core.msgcrypt.encrypt_req(connect_message).encode())

        response = core.msgcrypt.decrypt_req(self.client.recv(1024).strip()).decode()
        if response == "PASS_REQ":
            self.client.sendall(core.msgcrypt.encrypt_req(password).encode())
            auth_response = core.msgcrypt.decrypt_req(self.client.recv(1024).strip()).decode()
            if auth_response != "PASS_OK":
                print("Authentication failed.")
                self.client.close()
                return False

        self.connected = True
        return True

    def send_message(self, message):
        if not self.connected:
            print("Not connected.")
            return

        self.client.sendall(core.msgcrypt.encrypt_req(f"MESSAGE:{message}").encode())

    def disconnect(self):
        if self.connected:
            self.client.sendall(core.msgcrypt.encrypt_req("DISCONNECT").encode())
            self.client.close()
            self.connected = False
            print("Disconnected.")
