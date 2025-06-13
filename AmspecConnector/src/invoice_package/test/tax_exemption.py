# from logger import logger
from modules.base64 import json2base64
from modules.final_payload import cleartax
from utils.exemption_payload import dummy_exemption_payload
from modules.POST_cleartax import post_2_cleartax
def exemption_test():
    payload = dummy_exemption_payload()
    base64_encoded = json2base64(payload)
    final = cleartax(base64_encoded)
    response = post_2_cleartax(final)
    print(response)