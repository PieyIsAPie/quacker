import logging
import socketserver
import ssl
import json
import platform
import os
import queue
import sys
import core.msgcrypt
import random

FORMAT = '%(asctime)s:'
logging.basicConfig(format=FORMAT)

configpath = "/etc/quacker/cfg/config.json" if platform.system() != "Windows" else os.path.join(os.getenv('APPDATA'), "quacker", "config.json")
defaultcfg = """
{
    "ssl": {
        "enabled": false,
        "certificate": "MyCert.crt",
        "key": "MyKey.key"
    },
    "password": "",
    "brand": "My Chat Room",
    "allowDuplicateUsernames": false
}
"""
global cfg

log = logging.getLogger("Quacker-Server")
outgoingqueue = queue.Queue(1)

class User():
    id: int
    username: str
    color: str

class Handler(socketserver.BaseRequestHandler):
    user: User
    def handle(self):
        message = core.msgcrypt.decrypt_req(self.request.recv(1024).strip())

        if message.split(":")[0] == "CONNECT":
            if cfg["password"] is not None:
                self.request.sendall(core.msgcrypt.encrypt_req("PASS_REQ").encode())
                password_attempt = core.msgcrypt.decrypt_req(self.request.recv(1024).strip()).decode()

                if password_attempt != cfg["password"]:
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
            outgoingqueue.put(message.split(":")[1].split("/")[0])

def main():
    global cfg
    if os.path.exists(configpath) != True:
        fin = open(configpath, "w+")
        fin.write(defaultcfg)
        fin.close()
    cfg = json.loads(open(configpath).read())
    server = socketserver.ThreadingTCPServer(("", 55555), Handler)
    if cfg["ssl"] == "true":
        server.socket = ssl.wrap_socket(
            server.socket,
            keyfile=cfg["ssl"]["key"],
            certfile=cfg["ssl"]["certificate"],
            server_side=True
        )
    log.info("Starting server!")
    try:
        server.serve_forever()
    except KeyboardInterrupt:   
        log.info("Stopping!")
        sys.exit()
    
main()