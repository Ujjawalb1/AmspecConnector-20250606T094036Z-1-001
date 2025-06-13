from logger import logger
import json
import base64

def json2base64(payload):
    json_str = json.dumps(payload)
    json_bytes = json_str.encode("utf-8")
    base64_encoded = base64.b64encode(json_bytes).decode("utf-8")
    return base64_encoded
