import requests
import os
from dotenv import load_dotenv
from logger import logger
from exceptions import InvoiceExceptions

load_dotenv()

LOGIN_URL = os.getenv("LOGIN_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("LOGIN_PASSWORD")
# logger.info(EMAIL)
# logger.info(PASSWORD)

def get_token():
    try:
        logger.info("Authenticating LOGIN URL")
        payload = dict({"email":EMAIL,"password":PASSWORD})
        # logger.info(payload)
        header = {"Content-Type":"multipart/form-data; boundary=<calculated when request is sent>"}
        response = requests.post(LOGIN_URL,data=payload)
        if(response.status_code == 200):
            data = response.json().get("data")
            token = data.get("token")
            if not token:
                raise InvoiceExceptions("Login API response did not contain a token.")
            # logger.info("Authentication Successful")
            return token

        else:
            raise InvoiceExceptions(f"Login failed: {response.status_code} - {response.text}")
    except requests.exceptions.Timeout:
        logger.error("Login request timed out.")
        raise InvoiceExceptions("Login request timed out.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Login request failed: {e}")
        raise InvoiceExceptions(f"Login request failed: {e}")