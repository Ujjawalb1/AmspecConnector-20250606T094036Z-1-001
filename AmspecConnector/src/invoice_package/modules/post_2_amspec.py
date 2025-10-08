import requests
import os
from dotenv import load_dotenv
from logger import logger
from modules.auth import get_token
from exceptions import InvoiceExceptions
import json
load_dotenv()
API_URL = os.getenv("POST_API_URL")
def post_invoices(invoice_id,lhdn_doc_id,lhdn_status,lhdn_error_dtls,lhdn_qr_code,lhdn_govt_qr_code_url):
    try:
        """Send Response to POST API URL"""
        token=get_token()

        header = {
            "Authorization": f"Bearer {token}",
            "Connection": "keep-alive",
        }
        payload = {
            "invoiceId":invoice_id,
            "LHDN_DocumentId":lhdn_doc_id,
            "LHDN_Status":lhdn_status,
            "LHDN_ErrorDetails":lhdn_error_dtls,
            "LHDN_QrCode":lhdn_qr_code,
            "LHDN_GovtQrCodeUrl":lhdn_govt_qr_code_url
        }
        logger.info("Sending Data to API....")
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
                invoice_response = json.loads(response_text)
                logger.info(f"POST API Response:\n{json.dumps(invoice_response, indent=2)}")
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                logger.error(f"Failed to decode/parse POST response: {e}")
                raise InvoiceExceptions(f"Invalid response from POST API: {e}")


            response.close()
            if not invoice_response:
                raise InvoiceExceptions("No invoices found in API response.")                
            return invoice_response
        else:
            raise InvoiceExceptions(f"Invoice API returned {response.status_code}: {response.text}")
    except requests.exceptions.Timeout:
        logger.error("Invoice API request timed out.")
        raise InvoiceExceptions("Invoice API request timed out.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Invoice API request failed: {e}")
        raise InvoiceExceptions(f"Invoice API request failed: {e}")
        