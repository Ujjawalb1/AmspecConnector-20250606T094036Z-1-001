from logger import logger
from exceptions import InvoiceExceptions
from modules.fetcher import fetch_invoices
from modules.processor import process
from modules.auth import get_token
from test.tax_exemption import exemption_test
from datetime import date

def main():
    #data = fetch_invoices()
    # logger.info(data)
    process()
if __name__ == "__main__":
    main()
    