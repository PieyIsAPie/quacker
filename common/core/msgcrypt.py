"""god fucking dammit"""
import json, base64, hashlib, datetime
import logging

log = logging.getLogger("Quacker-Crypt")

class Request:
    requesttype = str()
    data = str()
    id = int()


def encrypt_req(req: str):
    log.info("Encrypting request")
    dictout = dict()
    dictout["message"] = base64.b64encode(req.encode()).decode()
    dictout["decode_md5"] = hashlib.md5(req.encode()).hexdigest()
    dictout["decode_sha1"] = hashlib.sha1(req.encode()).hexdigest()
    dictout["decode_sha256"] = hashlib.sha256(req.encode()).hexdigest()
    dictout["decode_sha384"] = hashlib.sha384(req.encode()).hexdigest()
    dictout["decode_sha512"] = hashlib.sha512(req.encode()).hexdigest()
    dictout["encode_md5"] = hashlib.md5(base64.b64encode(req.encode())).hexdigest()
    dictout["encode_sha1"] = hashlib.sha1(base64.b64encode(req.encode())).hexdigest()
    dictout["encode_sha256"] = hashlib.sha256(base64.b64encode(req.encode())).hexdigest()
    dictout["encode_sha384"] = hashlib.sha384(base64.b64encode(req.encode())).hexdigest()
    dictout["encode_sha512"] = hashlib.sha512(base64.b64encode(req.encode())).hexdigest()
    data = json.dumps(dictout)

    return data
    

def decrypt_req(req: str):
    dictin = json.loads(req)
    msg = base64.b64decode(dictin["message"].encode()).decode()
    if hashlib.md5(msg.encode()).hexdigest() != dictin["decode_md5"]:
        return 1
    elif hashlib.sha1(msg.encode()).hexdigest() != dictin["decode_sha1"]:
        return 1
    elif hashlib.sha256(msg.encode()).hexdigest() != dictin["decode_sha256"]:
        return 1
    elif hashlib.sha384(msg.encode()).hexdigest() != dictin["decode_sha384"]:
        return 1
    elif hashlib.sha512(msg.encode()).hexdigest() != dictin["decode_sha512"]:
        return 1

    elif hashlib.md5(dictin["message"].encode()).hexdigest() != dictin["encode_md5"]:
        return 1
    elif hashlib.sha1(dictin["message"].encode()).hexdigest() != dictin["encode_sha1"]:
        return 1
    elif hashlib.sha256(dictin["message"].encode()).hexdigest() != dictin["encode_sha256"]:
        return 1
    elif hashlib.sha384(dictin["message"].encode()).hexdigest() != dictin["encode_sha384"]:
        return 1
    elif hashlib.sha512(dictin["message"].encode()).hexdigest() != dictin["encode_sha512"]:
        return 1
    else:
        return msg

def parse(req):
    req = req.split(":")
    reqtype = req[0]
    


