import logging
import socketserver
import ssl
import core.requesthandler
import json
import platform
import os

configpath = "/etc/quacker/cfg/config.json" if platform.system() == "Windows" else f"{os.getenv('appdata')}\\quacker\\config.json"
defaultcfg = """

"""
cfg: dict

log = logging.getLogger("Quacker-Server")

def main():
    if os.path.exists(configpath) != True:
        fin = open(configpath, "w+")

    json.loads(open(configpath).read())
    server = socketserver.ThreadingTCPServer(("", 94464), core.requesthandler.Handler)

    
