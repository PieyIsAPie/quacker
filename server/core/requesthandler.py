import queue
import socketserver
import msgcrypt
import logging

log = logging.getLogger("Quacker-Server")
outgoingqueue = queue.Queue(1)
incomingqueue = queue.Queue(1)

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        message = msgcrypt.decrypt_req(self.request.recv(1024).strip())
        if message == 1: self.request.close()
        
        