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
import threading
import datetime

version = "1.0"
active_handlers = {}
configpath = "/etc/quacker/cfg/config.json" if platform.system() != "Windows" else os.path.join(os.getenv('APPDATA'), "quacker", "config.json")
logpath = f"/etc/quacker/logs/{datetime.date.today()}-{random.randint(1, 10000)}-quacker-log.log" if platform.system() != "Windows" else os.path.join(os.getenv('APPDATA'), "quacker", "config.json")
log = logging.getLogger("Quacker-Server")
logdash = logging.getLogger("Quacker-Dashboard")
log.setLevel(logging.INFO)  # Set the logging level to INFO or the desired level

# Create a log handler and set the formatter
handler = logging.FileHandler("")  # You can also use a FileHandler for writing logs to a file
formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)
logdash.addHandler(handler)

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

outgoingqueue = queue.Queue(1)

class User():
    id: int
    username: str
    color: str

class DashboardHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logdash.info(f"Connected to dashboard at {self.client_address}")
        
        try:
            while True:
                data = core.msgcrypt.decrypt_req(self.request.recv(1024))
                if not data:
                    break

                # Process data received from the dashboard
                # You can implement your logic here

                

                # Respond to the dashboard if needed
                # You can send back data or commands

        except Exception as e:
            logdash.error(f"Error handling connection: {e}")
        finally:
            self.request.close()
            logdash.info(f"Disconnected from dashboard")

class Handler(socketserver.BaseRequestHandler):
    user: User
    def handle(self):
        message = core.msgcrypt.decrypt_req(self.request.recv(1024).strip())

        if message.split(":")[0] == "CONNECT":
            if cfg["password"] is not None:
                self.request.sendall(core.msgcrypt.encrypt_req("PASS_REQ").encode())
                password_attempt = core.msgcrypt.decrypt_req(self.request.recv(1024).strip()).decode()

                if password_attempt.split(":")[0] == "PASSWORD" & password_attempt.split(":")[1].split("/")[1] != cfg["password"]:
                    self.request.sendall(core.msgcrypt.encrypt_req("PASS_INVALID").encode())
                    self.request.close()
                    return

            self.request.sendall(core.msgcrypt.encrypt_req("PASS_OK").encode())
            self.user = User()
            self.user.id = random.randint(10000000000000000, 99999999999999999)
            self.user.username = message.split(":")[1].split("/")[0]
            self.user.color = message.split(":")[1].split("/")[1]
            active_handlers[self.user.id] = self

        elif message == "DISCONNECT":
            self.request.close()
        elif message.split(":")[0] == "MESSAGE":
            outgoingqueue.put(message.split(":")[1].split("/")[0] + ":" + message.split(":")[1].split("/")[1])

def process_outgoing_messages():
    while True:
        try:
            message = outgoingqueue.get()  # Get the next message from the queue
            if message is not None:
                send_to_all_clients(message)  # Send the message to all connected clients
            outgoingqueue.task_done()  # Mark the task as done
        except Exception as e:
            print("Error processing outgoing message:", e)  # Handle exceptions gracefully

def send_to_all_clients(message):
    for handler in active_handlers.values():
        try:
            # Send the message to each connected client
            handler.request.sendall(core.msgcrypt.encrypt_req(f"MESSAGERECV:{message}").encode())
        except Exception as e:
            print("Error sending message to client:", e)  # Handle exceptions gracefully

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
    log.info(f"Quacker Server {version} - This code is licensed under the MIT Lisence")
    outgoing_thread = threading.Thread(target=process_outgoing_messages)
    outgoing_thread.daemon = True
    outgoing_thread.start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:   
        log.info("Stopping!")
        server.shutdown()
        sys.exit()
    
main()