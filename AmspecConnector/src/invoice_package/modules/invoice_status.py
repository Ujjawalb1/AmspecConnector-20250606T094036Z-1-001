# from logger import logger
# from exceptions import InvoiceExceptions
import os
from dotenv import load_dotenv 
import requests

def einvoice_status(document_id):
    headers = {
        "x-cleartax-auth-token" : os.getenv("CLEAR_AMSPEC_TOKEN"),
        "x-clear-tin" : os.getenv("CLEAR_AMSPEC_TIN"),
        "Content-Type": "application/json"   
    }
    host = os.getenv("HOST")
    url = "/einvoice/v1/documents/" + document_id + "/status"
    full_url = host+url
    response = requests.get(full_url,headers=headers)
    return response.json()