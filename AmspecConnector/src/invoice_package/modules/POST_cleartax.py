import requests
import json
from logger import logger
import os
from dotenv import load_dotenv
from exceptions import InvoiceExceptions
from tenacity import retry, stop_after_attempt, wait_exponential
import time
from ratelimit import limits, sleep_and_retry

load_dotenv()
CALLS_PER_MINUTE = 10  # Adjust this number based on API limits
PERIOD_IN_SECONDS = 60
@sleep_and_retry
@limits(calls=CALLS_PER_MINUTE, period=PERIOD_IN_SECONDS)
@retry(
    stop=stop_after_attempt(3),  # Retry 3 times
    wait=wait_exponential(multiplier=1, min=4, max=10),  # Wait between 4-10 seconds
    reraise=True
)
def post_2_cleartax(final_payload):
    try:
        HOST = os.getenv("HOST")
        E_URL = "/einvoice/v1/documents/generate"
        URL = HOST + E_URL
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "x-clear-tin": os.getenv("CLEAR_AMSPEC_TIN"),
            "x-cleartax-auth-token": os.getenv("CLEAR_AMSPEC_TOKEN")
        }

        logger.info(f"Making request to: {URL}")
        logger.info(f"Request Payload: {json.dumps(final_payload)}")
        
        response = requests.post(URL, json=final_payload, headers=headers)
        
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response Headers: {dict(response.headers)}")
        logger.info(f"Response Text: {response.text}")

        if response.status_code == 429:
            logger.warning("Rate limit exceeded, will retry with backoff...")
            raise requests.exceptions.RequestException("Rate limit exceeded")

        response.raise_for_status()

        if response.text.strip():
            try:
                return response.json()
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {str(e)}")
                logger.error(f"Response content: {response.text}")
                return None
        else:
            logger.error("Empty response received")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise  # Allow retry decorator to catch this
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None

