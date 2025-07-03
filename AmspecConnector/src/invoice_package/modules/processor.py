import csv
import openpyxl
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
from modules.header_subtotal import header_subtotal
def to_2_decimal(value):
    try:
        return float(round(float(value), 2))
    except (TypeError, ValueError):
        return 0.0 
load_dotenv()
# payload_count = 0
Send_To_Cleartax = True # set it false to check the payloads without sending to cleartax.

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
  
  items = data.get('items', [])
  total_line_extension_amount = sum(
        # abs(float(item.get("invoiceItems", {}).get('unitPrice', 0))) * abs(float(item.get("invoiceItems", {}).get("serviceQuantity", 0)))
        (abs(float(item.get("invoiceItems").get("preTaxAmount"))))
        for item in items
    )
  cleartax_payload = {
  "InvoiceTypeCode": {
    "Value": doc_typ_code
  },
  "IssueDate": str(date.today()),
  "IssueTime": "00:00:00",
  "DocumentCurrencyCode": data.get("invoiceCurrency"),# if not None else "MYR",
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
        "RegistrationName": data.get("billTo.partyName")
        
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
      "AllowanceChargeReason": "",
      "Amount": {
        "CurrencyID": data.get("invoiceCurrency"),# if not None else "MYR",
        "Value": 0
      }
    },
    {
      "ChargeIndicator": "true",
      "MultiplierFactorNumeric": 0,
      "AllowanceChargeReason": "",
      "Amount": {
        "CurrencyID": data.get("invoiceCurrency"),# if not None else "MYR",
        "Value": 0
      }
    }
  ],
  "TaxTotal": [
    {
      "TaxAmount": {

        "CurrencyID": data.get("invoiceCurrency"),#if not None else "MYR",
        "Value": data.get("taxAmount")
      },
      "TaxSubtotal": []
    }
  ],

  "LegalMonetaryTotal": {
    "TaxExclusiveAmount": {
        "CurrencyID": data.get("invoiceCurrency") if not None else "MYR",
        "Value": to_2_decimal(data.get("preTaxAmount"))
    },
    "LineExtensionAmount": {
                "CurrencyID": data.get("invoiceCurrency"),#if not None else "MYR",
                "Value": to_2_decimal(total_line_extension_amount)
    },
    "TaxInclusiveAmount": {
        "CurrencyID": data.get("invoiceCurrency"),#if not None else "MYR",
        "Value": to_2_decimal(data.get("totalAmount"))
    },
    "PayableAmount": {
        "CurrencyID": data.get("invoiceCurrency"),#if not None else "MYR",
        "Value": to_2_decimal(data.get("totalAmount"))
    },

  },
  # "PaymentMeans": {
  #   "PaymentMeansCode": "04",
  #   "PayeeFinancialAccount": {
  #     "Id": ""
  #   }
  # },
  # "PaymentTerms": {
  #   "Note": ""
  # },
  # "TaxExchangeRate": {
  #   "CalculationRate": homeExchangeRate
  # },
}
  #changes start here

  # Add this function to aggregate tax details
  # def aggregate_tax_subtotals(items):
  #       tax_categories = {}
        
  #       if items:
  #           for item in items:
  #               tax_info = item.get("invoiceItems", {}).get("tax", {})
  #               tax_category = "02" if tax_info.get("name") else "E"
  #               tax_percent = 0 if tax_info.get("percent") is None else tax_info.get("percent")/100
                
  #               key = (tax_category, tax_percent)
  #               if key not in tax_categories:
  #                   tax_categories[key] = {
  #                       "taxAmount": 0,
  #                       "taxableAmount": 0,
  #                       "category": tax_category,
  #                        "percent": tax_percent,
  #                       # "exemptionReason": "" if tax_info.get("name") else "Exempted Service"
  #                   }
                
  #               tax_categories[key]["taxAmount"] += abs(tax_info.get("amount", 0))
  #               tax_categories[key]["taxableAmount"] += abs(float(item.get("invoiceItems", {}).get("preTaxAmount", 0)))
        
  #       return [
  #           {
  #               "TaxAmount": {
  #                   "CurrencyID": data.get("invoiceCurrency") ,#if not None else "MYR",
  #                   "Value": details["taxAmount"]
  #               },
  #               "TaxableAmount": {
  #                   "CurrencyID": data.get("invoiceCurrency") ,#if not None else "MYR",
  #                   "Value": details["taxableAmount"]
  #               },
  #               "TaxCategory": {
  #                   "Id": details["category"],
  #                   ##"TaxExemptionReason": details["exemptionReason"]
  #               },
  #               # "Percent": details["percent"]
  #           }
  #           for details in tax_categories.values()
  #       ]

  #   # Modify the TaxTotal section in cleartax_payload
  items = data.get('items', [])
  tax_subtotals = header_subtotal(items, data)
  
  
  cleartax_payload["TaxTotal"] = [
        {
            "TaxAmount": {
                "CurrencyID": data.get("invoiceCurrency"),#if not None else "MYR",
                "Value": sum(sub["TaxAmount"]["Value"] for sub in tax_subtotals)
            },
            "TaxSubtotal": header_subtotal(items,data)
        }
    ]

 #changes end here 
 #commented out
  logger.info(f"cleartax_payload_XXXXXXXXXXXX: {cleartax_payload}") 
  return cleartax_payload

    
def process():
    invoices = fetch_invoices()
    datas = invoices.get("data")
    now = datetime.now()
    # logger.info(type(now.month))
    payload_count = 0
    logger.info(f"Total invoices: {len(datas)}")
    # wb = openpyxl.Workbook()
    # ws = wb.active
    # ws.title = "Invoices"
    # ws.append(["Invoice Number", "Registration Name", "Date"])
    for data in datas:
        #Debugging logic starts
        # logger.info(f"Processing invoice: {data.get('invoiceNumber')}")
        # invoice_date = datetime.strptime(data.get('invoiceDate'), "%Y-%m-%d %H:%M:%S")
        # if not (invoice_date.year == now.year and (invoice_date.month == now.month or invoice_date.month == now.month-1)):
        #     logger.info("Skipped due to date filter")
        #     continue
        # if not data.get("invoiceNumber"):
        #     logger.info("Skipped due to missing invoice number")
        #     continue
        # if data.get("LHDN_Status") == 'VALID' and data.get("LHDN_QrCode") is not None:
        #     logger.info("Skipped due to LHDN status/QR code")
        #     continue
        # #Debugging logic ends
        invoice_date = datetime.strptime(data.get('invoiceDate'), "%Y-%m-%d %H:%M:%S")
       # for particular date and invoice number starts
        # registration_name = data.get("billTo.partyName")
        # if invoice_date.day == 25 and invoice_date.month == 6 and data.get("invoiceNumber"):
        #     # logger.info(f"Processing invoice: {data.get('invoiceNumber')}, Registration Name: {registration_name}, Date: {invoice_date}")
        #     ws.append([data.get('invoiceNumber'), registration_name, invoice_date.strftime("%Y-%m-%d")])
        if (invoice_date.year == now.year and (invoice_date.month == now.month or invoice_date.month == now.month-1)) and data.get("invoiceNumber"):#=="518-014079": #Checking for this month and previous month
         ## ends
          logger.info(data)
          # break
          if data.get("LHDN_Status") != 'VALID' or data.get("LHDN_QrCode") is None:
            invoice_headers = invoice_header(data)
            invoice_id = data.get("invoiceId")
            items = data.get('items')
            if items is not None:
                for item in items:
                    invoice_headers["InvoiceLine"].append(process_line_item(item,data))
            # commented out
            logger.info(invoice_headers)
            # break
            base64 = json2base64(invoice_headers)
            #commented out
            logger.info(base64)
            cleartax_final_payload = cleartax(base64)
            #commented out
            logger.info(cleartax_final_payload)
            payload_count += 1
            # logger.info(f"Payloads sent so far: {payload_count, data.get('invoiceNumber')}")
            if Send_To_Cleartax and payload_count:
                try:
                    document_id_response = post_2_cleartax(cleartax_final_payload)
                    logger.info(document_id_response)
                except Exception as e:
                    logger.error(f"Error sending payload to ClearTax: {e}")
                    continue
            else:
                # logger.info("Skipping sending to ClearTax as Send_To_Cleartax is False or payload_count is 0")
                document_id_response = None
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
            # logger.info(post_invoice)
            # break
          else:
              continue
    # wb.save("invoices_25_june.xlsx")
def process_line_item(item,data):
  discount_amount=abs(float(item.get("invoiceItems").get('unitPrice')))*abs(float(item.get("invoiceItems").get("serviceQuantity")))*item.get('invoiceItems').get('discount').get('percent')/100 
  item_price_extension = abs(float(item.get("invoiceItems").get('unitPrice')))*abs(float(item.get("invoiceItems").get("serviceQuantity")))
  line_extension_amount= item_price_extension - discount_amount
  # total_line_amount += line_extension_amount - discount_amount
  return {
      "Id": item.get("sInvItemId"),
      "InvoicedQuantity": {
        "Quantity": abs(float(item.get("invoiceItems").get("serviceQuantity"))),

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
      "ItemPriceExtension": {
        "CurrencyID": data.get("invoiceCurrency"),#if not None else "MYR",
        "Value": to_2_decimal(item_price_extension)
      },
      "AllowanceCharge": [
        {
          "ChargeIndicator": "false" if (item.get('invoiceItems').get('discount').get('percent')/100==0 or item.get('invoiceItems').get('discount').get('percent')/100==None ) else "true",
          "MultiplierFactorNumeric": item.get('invoiceItems').get('discount').get('percent')/100,
          "AllowanceChargeReason": "NA",
          "Amount": {
            "CurrencyID": data.get("invoiceCurrency"),
            "Value": abs(float(item.get("invoiceItems").get('unitPrice')))*abs(float(item.get("invoiceItems").get("serviceQuantity")))*item.get('invoiceItems').get('discount').get('percent')/100  #to be calculated
          }
        },
      ],
      "Price": {
        "PriceAmount": {
          "CurrencyID": data.get("invoiceCurrency"),#if not None else "MYR",
          "Value": abs(item.get("invoiceItems").get("unitPrice"))
        }
      },
      "LineExtensionAmount": {
        "CurrencyID": data.get("invoiceCurrency"),#if not None else "MYR",
        "Value": to_2_decimal(line_extension_amount)
      },
      "TaxTotal": {
        "TaxAmount": {
        "CurrencyID": data.get("invoiceCurrency"),
        "Value": abs(item.get('invoiceItems').get('tax').get('amount')),
        },
        "TaxSubtotal": [
          {
            "TaxAmount": {
              "CurrencyID": data.get("invoiceCurrency") if not None else "MYR",
              "Value": round(abs(item.get('invoiceItems').get('tax').get('amount')),2)
            },
            "TaxableAmount": {
              "CurrencyID": data.get("invoiceCurrency") if not None else "MYR",
              "Value": round(abs(float(item.get("invoiceItems").get("preTaxAmount"))),2)
            },
            "TaxCategory": {
  
              "Id": "02" if item.get("invoiceItems").get("tax").get("name") != None else "E",
              "TaxExemptionReason": "" if item.get("invoiceItems").get('tax').get("name") !=None else "Exempted Service"
            },
            "Percent": 0 if item.get("invoiceItems").get("tax").get("percent") == None else item.get("invoiceItems").get("tax").get("percent")/100

          }
        ]
        
      }
  }
  
