def header_subtotal(items, data):
    groups = {
        "02": {
            "TaxAmount": 0.0,
            "TaxableAmount": 0.0,
            "Percent": 0.0,
            ##"TaxExemptionReason": ""
        },
        "E": {
            "TaxAmount": 0.0,
            "TaxableAmount": 0.0,
            "Percent": 0.0,
            ##"TaxExemptionReason": "Exempted Service"
        }
    }
    for item in items:
        tax = item.get("invoiceItems").get("tax")
        pre_tax_amount = abs(float(item.get("invoiceItems").get("preTaxAmount")))
        tax_amount = abs(float(tax.get("amount") or 0))
        percent = tax.get("percent")
        if tax.get("name") is not None:
            group_id = "02"
            groups[group_id]["Percent"] = percent / 100 if percent is not None else 0.0
        else:
            group_id = "E"
            groups[group_id]["Percent"] = 0.0
        groups[group_id]["TaxAmount"] += tax_amount
        groups[group_id]["TaxableAmount"] += pre_tax_amount

    subtotals = []
    for group_id, values in groups.items():
        # Only include groups with non-zero taxable amount
        if values["TaxableAmount"] > 0:
            subtotals.append({
                "TaxAmount": {
                    "CurrencyID": data.get("homeCurrency") or "MYR",
                    "Value": round(values["TaxAmount"], 2)
                },
                "TaxableAmount": {
                    "CurrencyID": data.get("homeCurrency") or "MYR",
                    "Value": round(values["TaxableAmount"], 2)
                },
                "TaxCategory": {
                    "Id": group_id,
                    ##"TaxExemptionReason": values["TaxExemptionReason"]
                },
                "Percent": values["Percent"]
            })
    return subtotals
