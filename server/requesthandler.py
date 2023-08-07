import socketserver
import core.msgcrypt
import logging
import random
import main

log = logging.getLogger("Quacker-Server")

class User():
    id: int
    username: str
    color: str

class Handler(socketserver.BaseRequestHandler):
    user: User
    def handle(self):
        message = core.msgcrypt.decrypt_req(self.request.recv(1024).strip())

        if message.split(":")[0] == "CONNECT":
            if main.cfg["password"] is not None:
                self.request.sendall(core.msgcrypt.encrypt_req("PASS_REQ").encode())
                password_attempt = core.msgcrypt.decrypt_req(self.request.recv(1024).strip()).decode()

                if password_attempt != main.cfg["password"]:
                    self.request.sendall(core.msgcrypt.encrypt_req("PASS_INVALID").encode())
                    self.request.close()
                    return

            self.request.sendall(core.msgcrypt.encrypt_req("PASS_OK").encode())
            self.user = User()
            self.user.id = random.randint(10000000000000000, 99999999999999999)
            self.user.username = message.split(":")[1].split("/")[0]
            self.user.color = message.split(":")[1].split("/")[1]

        elif message == "DISCONNECT":
            self.request.close()
        elif message.split(":")[0] == "MESSAGE":
            main.outgoingqueue.put(message.split(":")[1].split("/")[0])


        
        