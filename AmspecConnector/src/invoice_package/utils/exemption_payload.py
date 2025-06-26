import os
from dotenv import load_dotenv
load_dotenv()
def dummy_exemption_payload():
    return {
  "InvoiceTypeCode": {
    "Value": "01"
  },
  "IssueDate": "2025-03-02",

  "IssueTime": "11:19:36",
  "DocumentCurrencyCode": "MYR",
#   "DocumentCurrencyCode": data.get("invoiceCurrency"),

  "Id": "TEST-CT-00001",
#   "Id": data.get("invoiceNumber"),

  "AccountingCustomerParty": {
    "Party": {
      "Contact": {
        "ElectronicMail": "e-invoice@pacificofats.com",
        "Telephone": "6032230090"
        # "Telephone":data.get("Telephone_Number_Please_include_country_code_area_code_and_telephone")
      },
      "PartyIdentification": [
        {
          "Id": {
            "SchemeID": "TIN",
            "Value": os.getenv("CLEAR_AMSPEC_TIN")
            # "Value": data.get("Tax_registration_No_TIN_Number")

          }
        },
        {
          "Id": {
            "SchemeID": "BRN",
            "Value": "198801004020"
          }
        },
        {
          "Id": {
            "SchemeID": "SST",
            "Value": "W10-1809-32000158"
            # "Value": data.get("VAT_Registration_No_SST_Number")

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
        "RegistrationName": "PACIFIC OILS & FATS INDUSTRIES SDN. BHD."
        # "RegistrationName": data.get("Full_Registered_Company_Name")


      },
      "PostalAddress": {
        "AddressLine": [
          {
            "Line": "No 8, Jalan Besi Utama, Batu 24, Kelapa Sawit"
            # "Line": data.get("Registered_Street_Address")

          },
          {
            "Line": "line2"
          },
          {
            "Line": "line3"
          }
        ],
        "CityName": "KULAI",
        # "CityName": data.get("Town_City2"),

        "Country": {
          "IdentificationCode": {
            "CountryCode": "MYS"
          }
        },
        "CountrySubentityCode": "01",
        "PostalZone": "81030"
        # "PostalZone": data.get("Postal_Code2")

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
  
  "InvoiceLine": [
     {
      "Id": 1,
      "InvoicedQuantity": {
        "Quantity": 100000,
        "UnitCode": "H87"
      },
      "Item": {
        "CommodityClassification": [
          {
            "ItemClassificationCode": {
              "ListID": "CLASS",
              "Value": "022"
            }
          }
        ],
        "Description": "test description",
      },
      "AllowanceCharge": [
        {
          "ChargeIndicator": "true",
          "MultiplierFactorNumeric": 0,
          "AllowanceChargeReason": "NA",
          "Amount": {
            "CurrencyID": "MYR",
            "Value": 1000
          }
        }
      ],
      "ItemPriceExtension": {
        "Amount": {
          "CurrencyID": "MYR",
          "Value": 50000000.00
        }
      },
      "Price": {
        "PriceAmount": {
          "CurrencyID": "MYR",
          "Value": 500.00
        }
      },
      "LineExtensionAmount": {
        "CurrencyID": "MYR",
        "Value": 49999000.00
      },
      "TaxTotal": 
    {
      "TaxAmount": {
        "CurrencyID": "MYR",
        "Value": 0
      },
      "TaxSubtotal": [
        {
          "TaxAmount": {
            "CurrencyID": "MYR",
            "Value": 0
          },
          "TaxableAmount": {
            "CurrencyID": "MYR",
            "Value": 49999000.00
          },
          "TaxCategory": {
            "Id": "E",
            "TaxExemptionReason": "bicycles"
          }
        }
      ]
     }
     }
  ],
  "AllowanceCharge": [
    {
      "ChargeIndicator": "false",
      "MultiplierFactorNumeric": 0,
      "AllowanceChargeReason": "",
      "Amount": {
        "CurrencyID": "MYR",
        # "CurrencyID": data.get("InvoiceCurrency"),

        "Value": 0
      }
    },
    {
      "ChargeIndicator": "true",
      "MultiplierFactorNumeric": 0,
      "AllowanceChargeReason": "",
      "Amount": {
        "CurrencyID": "MYR",
        # "CurrencyID": data.get("InvoiceCurrency"),

        "Value": 0
      }
    }
  ],
#   "PrepaidPayment": {
#     "Id": "Clear-02",
#     "PaidAmount": {
#       "CurrencyID": "MYR",
#         # "CurrencyID": data.get("InvoiceCurrency"),
#       "Value": "1500000"
#     #   "Value": "0"

#     },
#     "PaidDate": "2024-07-28",
#     "PaidTime": "13:00:00"
#   },
  "TaxTotal": [
    {
      "TaxAmount": {
        "CurrencyID": "MYR",
        # "CurrencyID": data.get("InvoiceCurrency"),

        # "Value": 3999920.00
        "Value":0
        # "Value": data.get("taxAmount")

      },
      "TaxableAmount": {
        "CurrencyID": "MYR",
        "Value": 49999000.00
      },
      "TaxSubtotal": [
        {
          "TaxAmount": {
            "CurrencyID": "MYR",
            # "CurrencyID": data.get("InvoiceCurrency"),

            # "Value": 3999920.00
            # "Value": data.get("taxAmount")
            "Value":0

          },
          "TaxableAmount": {
            "CurrencyID": "MYR",
            "Value": 49999000.00
          },
          "TaxCategory": {
            "Id": "E",
            "TaxExemptionReason": "bicycles"
          }
        }
      ]
    }
  ],
  "LegalMonetaryTotal": {
    "LineExtensionAmount": {
      "CurrencyID": "MYR",
      "Value": 49999000.00
    },
    # "AllowanceTotalAmount": {
    #   "CurrencyID": "MYR",
    #   "Value": 4000.00
    # },
    # "ChargeTotalAmount": {
    #   "CurrencyID": "MYR",
    #   "Value": 4000.00
    # },
    "TaxExclusiveAmount": {
      # "CurrencyID": "MYR",
        # "CurrencyID": data.get("InvoiceCurrency"),

      "Value": 49999000.00
    #   "Value": float(data.get("preTaxAmount"))
    },
    "TaxInclusiveAmount": {
      # "CurrencyID": "MYR",
        # "CurrencyID": data.get("InvoiceCurrency"),
        "Value": 49999000.00

      # "Value": 53998920.00
    #   "Value": float(data.get("totalAmount"))
      
    },
    # "PrepaidAmount": {
    #   "CurrencyID": "MYR",
    #   "Value": 1500000
    # },
    "PayableAmount": {
      # "CurrencyID": "MYR",
        # "CurrencyID": data.get("InvoiceCurrency"),
        "Value": 49999000.00

      # "Value": 52498920.00
    #   "Value": float(data.get("totalAmount"))

    },
    # "PayableRoundingAmount": {
    #   "CurrencyID": "MYR",
    #   "Value": 0.00
    # }
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
    "CalculationRate": "1"
  },
  # "AdditionalDocumentReference": [
  #   {
  #     "Id": "E12345678912",
  #     "DocumentType": "CustomsImportForm"
  #   },
  #   {
  #     "Id": "FTA",
  #     "DocumentDescription": "",
  #     "DocumentType": "FreeTradeAgreement"
  #   },
  #   {
  #     "Id": "E12345678912",
  #     "DocumentType": "K2"
  #   },
  #   {
  #     "Id": "CIF"
  #   }
  # ]
}