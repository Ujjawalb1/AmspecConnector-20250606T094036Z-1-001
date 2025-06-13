import requests
import os
from dotenv import load_dotenv
from logger import logger
from modules.auth import get_token
from exceptions import InvoiceExceptions
import json
load_dotenv()
API_URL = os.getenv("API_URL")
def fetch_invoices():
    try:
        """Fetch Invoices from API URL"""
        token=get_token()

        header = {
            "Authorization": f"Bearer {token}",
            "Connection": "keep-alive",
        }
        payload = {
            "items":"true",
            "customer":"true",
        }
        logger.info("Accessing API....")
        response = requests.post(API_URL,headers=header,data=payload,stream=True,timeout=300)
        response_data = b""
        chunk_number = 0
        for chunk in response.iter_content(1024*1024):
            if not chunk:
                print(f"Received empty chunk after {chunk_number} chunks.")
                break
            chunk_number += 1
            response_data += chunk
        # logger.info(f"Chunk {chunk_number}: {len(chunk)} bytes (Total: {len(response_data)} bytes)")
        # logger.info("Final Size (bytes):", len(response_data))
        # logger.info(response.headers)
        if(response.status_code==200):
            # Decode and process
            try:
                response_text = response_data.decode('utf-8')
                # logger.info("Decoded Length (characters):", len(response_text))
                # Optionally parse as JSON if the response is JSON
                invoice = json.loads(response_text)
                # logger.info(json.dumps(invoice, indent=2))
            except UnicodeDecodeError:
                logger.info("Failed to decode as UTF-8. Raw size:", len(response_data))

            response.close()
            if not invoice:
                raise InvoiceExceptions("No invoices found in API response.")
                logger.info(f"Successfully fetched {len(invoices)} invoices.")
                
            return invoice
        else:
            raise InvoiceExceptions(f"Invoice API returned {response.status_code}: {response.text}")
    except requests.exceptions.Timeout:
        logger.error("Invoice API request timed out.")
        raise InvoiceExceptions("Invoice API request timed out.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Invoice API request failed: {e}")
        raise InvoiceExceptions(f"Invoice API request failed: {e}")
        