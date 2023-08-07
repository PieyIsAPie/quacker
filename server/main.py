import logging
import socketserver
import ssl
import requesthandler
import json
import platform
import os
import queue
import sys

FORMAT = '%(asctime)s:'
logging.basicConfig(format=FORMAT)

configpath = "/etc/quacker/cfg/config.json" if platform.system() == "Windows" else f"{os.getenv('appdata')}\\quacker\\config.json"
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

def main():
    global cfg
    if os.path.exists(configpath) != True:
        fin = open(configpath, "w+")
        fin.write(defaultcfg)
        fin.close()
    cfg = json.loads(open(configpath).read())
    server = socketserver.ThreadingTCPServer(("", 94464), requesthandler.Handler)
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