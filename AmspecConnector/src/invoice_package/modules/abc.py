import csv
from modules.fetcher import fetch_invoices
from modules.post_2_amspec import post_invoices
from logger import logger
import re
from modules.utils import get_state_codes
# from exceptions import InvoiceExceptions
from modules.base64 import json2base64
from modules.final_payload import cleartax
from modules.POST_cleartax import post_2_cleartax
from dotenv import load_dotenv
import os
from datetime import date,datetime

from modules.invoice_status import einvoice_status
load_dotenv()
count = 0
def invoice_header(data):
  if data.get("homeExchangeRate") is None:
    homeExchangeRate = 1
  else:
    homeExchangeRate = float(data.get('homeExchangeRate'))
  if data.get("Buyer_Registration_Number") is None or data.get("Buyer_Registration_Number") == data.get("VAT_Registration_No_SST_Number") :
        brn_reg_num = "NA"
  else:
        brn_reg_num = data.get("Buyer_Registration_Number")
        # logger.info(brn_reg_num)
  if data.get("Buyer_Registration_Type") is None or data.get("Buyer_Registration_Type") == "SST":
        brn_reg_type = "BRN"
  else:
        if data.get("Buyer_Registration_Type") == "VAT":
            brn_reg_type = "SST"
        else:
          brn_reg_type = data.get("Buyer_Registration_Type")
        # logger.info(brn_reg_type)
  if data.get('documentType').upper() =='INVOICE':
      doc_typ_code = '01'
  elif data.get('documentType').upper() == 'CREDIT NOTE':
      doc_typ_code = '02'
  else:
      doc_typ_code = '01'  #change it in future if debit note or other scenarios exist
  raw_number = data.get("Telephone_Number_Please_include_country_code_area_code_and_telephone")
  cleaned_number = re.sub(r"[^\d]", "", raw_number)
  sst = data.get("VAT_Registration_No_SST_Number")
  postal_code = data.get(data.get("billTo.address.postalCode"))if data.get("billTo.address.country") == "MYS" else None 
  normalized_sst = "NA" if str(sst).strip().lower() in ["n/a", "na"] else sst
  if normalized_sst == "NA":
      sst_type = "SST"
  else:
      sst_type = "SST"
  normalized_brn = "NA" if str(brn_reg_num).strip().lower() in ["n/a", "na",None] else brn_reg_num
  state = get_state_codes(data.get("billTo.address.state","State_Province")) if data.get("billTo.address.state","State_Province") else get_state_codes("not applicable")
  

  cleartax_payload = {
  "InvoiceTypeCode": {
    "Value": doc_typ_code
  },
  "IssueDate": str(date.today()),
  "IssueTime": "00:00:00",
  "DocumentCurrencyCode": data.get("homeCurrency") if not None else "MYR",
  "Id": data.get("invoiceNumber"),
  "AccountingCustomerParty": {
    "Party": {
      "Contact": {
        "ElectronicMail":  None if data.get("E_invoicing_Notification_Email_Address").strip().lower() in ["n/a", "na"] else data.get("E_invoicing_Notification_Email_Address"),
        "Telephone":cleaned_number
      },
      "PartyIdentification": [
        {
          "Id": {
            "SchemeID": "TIN",
            "Value": data.get("Tax_registration_No_TIN_Number")
          }
        },
        {
          "Id": {
            "SchemeID": "BRN",
            "Value": str(normalized_brn)
          }
        }
        ,
        {
          "Id": {
            "SchemeID": sst_type,
            "Value": normalized_sst
          }
        },

      ],
      "PartyLegalEntity": {
        "RegistrationName": data.get("billTo.companyName")
      },
      "PostalAddress": {
        "AddressLine": [
          {
            "Line": data.get("billTo.address.streetAddress")

          }
        ],
        "CityName": data.get("billTo.address.city") if data.get("billTo.address.city","Town_City2") else "NA",
        "Country": {
          "IdentificationCode": {
            "CountryCode": data.get("billTo.address.country")
          }
        },
        "CountrySubentityCode": state,
        "PostalZone": postal_code
      }
    }
  },
  "AccountingSupplierParty": {
    "Party": {
      "Contact": {
        "ElectronicMail": "malaysia.invoicing@amspecgroup.com",
        "Telephone": "601111199600"
      },
      "IndustryClassificationCode": {
        "Value": "71200",
        "Name": "NOT APPLICABLE"
      },
      "PartyIdentification": [
        {
          "Id": {
            "SchemeID": "TIN",
            "Value": os.getenv("CLEAR_AMSPEC_TIN")
          }
        },
        {
          "Id": {
            "SchemeID": "BRN",
            "Value": "1110122-M"
          }
        },
        {
          "Id": {
            "SchemeID": "SST",
            "Value": "B10-2407-32000032"
          }
        },
        {
          "Id": {
            "SchemeID": "TTX",
            "Value": "NA"
          }
        }
      ],
      "PartyLegalEntity": {
        "RegistrationName": "AmSpec Inspection Malaysia Sdn. Bhd."
      },
      "PostalAddress": {
        "AddressLine": [
          {
            "Line": "No. 3-10 Blok 10, The Landmark,"
          },
          {
            "Line": "Jalan Batu Nilam 16, Bandar Bukit Tinggi 2,"
          },
          {
            "Line": "Klang, Selangor Darul Ehsan,"
          }
        ],
        "CityName": "Selangor",
        "Country": {
          "IdentificationCode": {
            "CountryCode": "MYS"
          }
        },
        "CountrySubentityCode": "10",
        "PostalZone": "41200"
      }
    }
  },
  
  "InvoiceLine": [],
  "AllowanceCharge": [
    {
      "ChargeIndicator": "false",
      "MultiplierFactorNumeric": 0,
      "AllowanceChargeReason": "In store discount",
      "Amount": {
        "CurrencyID": data.get("homeCurrency") if not None else "MYR",
        "Value": 0
      }
    },
    {
      "ChargeIndicator": "true",
      "MultiplierFactorNumeric": 0,
      "AllowanceChargeReason": "Convenience fee",
      "Amount": {
        "CurrencyID": data.get("homeCurrency") if not None else "MYR",
        "Value": 0
      }
    }
  ],
  "TaxTotal": [
    {
      "TaxAmount": {

        "CurrencyID": data.get("homeCurrency") if not None else "MYR",
        "Value": data.get("taxAmount")
      },
      "TaxSubtotal": [
        {
          "TaxAmount": {
            "CurrencyID": data.get("homeCurrency") if not None else "MYR",
            "Value": (data.get("taxAmount"))

          },
          "TaxCategory": {
            "Id": "02",
            "TaxExemptionReason": ""
          }
        }
      ]
    }
  ],
  "LegalMonetaryTotal": {
    "TaxExclusiveAmount": {
        "CurrencyID": data.get("homeCurrency") if not None else "MYR",
      "Value": data.get("preTaxAmount")
    },
    "TaxInclusiveAmount": {
        "CurrencyID": data.get("homeCurrency") if not None else "MYR",
      "Value": (data.get("totalAmount"))
      
    },
    "PayableAmount": {
        "CurrencyID": data.get("homeCurrency") if not None else "MYR",
      "Value": (data.get("totalAmount"))

    },
  },
  "PaymentMeans": {
    "PaymentMeansCode": "04",
    "PayeeFinancialAccount": {
      "Id": "1234567890123"
    }
  },
  "PaymentTerms": {
    "Note": "Payment Method is CARD"
  },
  "TaxExchangeRate": {
    "CalculationRate": homeExchangeRate
  },
}

  return cleartax_payload
def process():
    invoices = fetch_invoices()
    datas = invoices.get("data")
    now = datetime.now()
    logger.info(type(now.month))
    for data in datas:
        invoice_date = datetime.strptime(data.get('invoiceDate'), "%Y-%m-%d %H:%M:%S")
        if (invoice_date.year == now.year and (invoice_date.month == now.month or invoice_date.month == now.month-1)): #Checking for this month and previous month
          # logger.info(data)
          if data.get("LHDN_Status") != 'VALID' or data.get("LHDN_QrCode") is None:
            invoice_headers = invoice_header(data)
            invoice_id = data.get("invoiceId")
            items = data.get('items')
            if items is not None:
                for item in items:
                    invoice_headers["InvoiceLine"].append(process_line_item(item,data))
              # logger.info(invoice_headers)
            base64 = json2base64(invoice_headers)
            logger.info(base64)
            cleartax_final_payload = cleartax(base64)
            logger.info(cleartax_final_payload)
            document_id_response = post_2_cleartax(cleartax_final_payload)
            logger.info(document_id_response)
            if document_id_response != None and  document_id_response.get("DocumentResponses") != None and len(document_id_response.get("DocumentResponses"))>0:
              if document_id_response.get("ErrorDetails") !=None:
                error_dtls = str(document_id_response.get("ErrorDetails"))
              else:
                  error_dtls = "None"
              document_id = document_id_response.get("DocumentResponses")[0].get("DocumentId")
              einvoice_stat = einvoice_status(document_id)
              qr_code = einvoice_stat.get("QrCode") if einvoice_stat.get("QrCode") != None else "None"
              govt_qr_code_url = einvoice_stat.get("GovtQrCodeUrl") if einvoice_stat.get("GovtQrCodeUrl") != None else "None"
              lhdn_status = str(einvoice_stat.get("Status"))
              post_invoice = post_invoices(invoice_id,document_id,lhdn_status,error_dtls,qr_code,govt_qr_code_url)
              # break
          else:
              continue
def process_line_item(item,data):
  return {
      "Id": item.get("sInvItemId"),
      "InvoicedQuantity": {
        "Quantity": abs(int(item.get("invoiceItems").get("serviceQuantity"))),

        "UnitCode": "H87"
      },
      "Item": {
        "CommodityClassification": [
          {
            "ItemClassificationCode": {
              "ListID": "CLASS",
                "Value": item.get("classificationCode")

            }
          }
        ],
        "ProductTariffCode": {
          "ItemClassificationCode": {
            "Value": item.get("classificationCode")
          }
        },
        "Description" : item.get("invoiceItems").get("description"),

        "OriginCountry": {
          "IdentificationCode": {
            "CountryCode": "MYS"
          }
        }
      },
      "AllowanceCharge": [
        {
          "ChargeIndicator": "false",
          "MultiplierFactorNumeric": item.get('invoiceItems').get('discount').get('percent'),
          "AllowanceChargeReason": "NA",
          "Amount": {
            "CurrencyID": data.get("homeurrency"),
            "Value": abs(float(item.get("invoiceItems").get('unitPrice')))*abs(float(item.get("invoiceItems").get("serviceQuantity"))) #to be calculated
          }
        },
      ],
      "Price": {
        "PriceAmount": {
          "CurrencyID": data.get("homeCurrency") if not None else "MYR",
          "Value": abs(item.get("invoiceItems").get("unitPrice"))
        }
      },
      "TaxTotal": {
        "TaxAmount": {
        "CurrencyID": data.get("homeurrency"),
        "Value": abs(item.get('invoiceItems').get('tax').get('amount'))
        },
        "TaxSubtotal": [
          {
            "TaxAmount": {
              "CurrencyID": data.get("homeCurrency") if not None else "MYR",
              "Value": abs(abs(float(data.get("totalAmount")))-abs(float(data.get("preTaxAmount"))))
            },
            "TaxableAmount": {
              "CurrencyID": data.get("homeCurrency") if not None else "MYR",
              "Value": abs(float(data.get("preTaxAmount")))           
            },
            "TaxCategory": {
  
              "Id": "02" if item.get("invoiceItems").get("tax").get("name") != None else "E",
              "TaxExemptionReason": "" if item.get("invoiceItems").get('tax').get("name") !=None else "Exempted Service"
            },
            "Percent": item.get("invoiceItems").get("tax").get("percent")
          }
        ]
        
      }
    }

