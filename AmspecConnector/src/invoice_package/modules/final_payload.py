from logger import logger
from exceptions import InvoiceExceptions


def cleartax(base64_encoded):
    return {
    "Documents": [
        {
            "DocumentData": base64_encoded,
            "DocumentFormat": "JSON",
            "UniqueIdentifier": "C58746708080_TEST-SALES-001_01_2024",
            # "CustomFields": {
            #     "Internal Number": "INV00001234561687"
            # },
            "version": "MY_GENERATE_UBL_2_1_V1"
        }
    ],
    "AllowCancelledDocumentsGeneration" : "true"
}
