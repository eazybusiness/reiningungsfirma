#!/usr/bin/env python3
"""
Extract invoices, credit notes, and vendor bills from backup to CSV files
"""

import psycopg2
import csv
from datetime import datetime

DB_NAME = 'odoo_backup_analysis'

print("="*80)
print("EXTRACTING INVOICES FROM BACKUP TO CSV")
print("="*80 + "\n")

conn = psycopg2.connect(dbname=DB_NAME)
cur = conn.cursor()

# Extract customer invoices (out_invoice)
print("Extracting customer invoices (out_invoice)...")

query_invoices = """
SELECT 
    am.name as invoice_number,
    am.invoice_date,
    am.invoice_date_due,
    rp.name as customer_name,
    rp.vat as customer_vat,
    rp.email as customer_email,
    am.state,
    am.payment_state,
    am.amount_untaxed,
    am.amount_tax,
    am.amount_total,
    am.amount_residual,
    apt.name as payment_term,
    am.ref as reference,
    am.invoice_origin as origin,
    rc.name as currency,
    am.narration as notes
FROM account_move am
LEFT JOIN res_partner rp ON am.partner_id = rp.id
LEFT JOIN account_payment_term apt ON am.invoice_payment_term_id = apt.id
LEFT JOIN res_currency rc ON am.currency_id = rc.id
WHERE am.move_type = 'out_invoice'
ORDER BY am.invoice_date, am.name;
"""

cur.execute(query_invoices)
invoices = cur.fetchall()

with open('customer_invoices.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Invoice Number', 'Invoice Date', 'Due Date', 'Customer Name', 'Customer VAT',
        'Customer Email', 'State', 'Payment State', 'Amount Untaxed', 'Amount Tax',
        'Amount Total', 'Amount Residual', 'Payment Term', 'Reference', 'Origin',
        'Currency', 'Notes'
    ])
    writer.writerows(invoices)

print(f"✅ Exported {len(invoices)} customer invoices to customer_invoices.csv")

# Extract credit notes (out_refund)
print("\nExtracting credit notes (out_refund)...")

query_credit_notes = """
SELECT 
    am.name as credit_note_number,
    am.invoice_date,
    am.invoice_date_due,
    rp.name as customer_name,
    rp.vat as customer_vat,
    rp.email as customer_email,
    am.state,
    am.payment_state,
    am.amount_untaxed,
    am.amount_tax,
    am.amount_total,
    am.amount_residual,
    apt.name as payment_term,
    am.ref as reference,
    am.invoice_origin as origin,
    rc.name as currency,
    am.narration as notes
FROM account_move am
LEFT JOIN res_partner rp ON am.partner_id = rp.id
LEFT JOIN account_payment_term apt ON am.invoice_payment_term_id = apt.id
LEFT JOIN res_currency rc ON am.currency_id = rc.id
WHERE am.move_type = 'out_refund'
ORDER BY am.invoice_date, am.name;
"""

cur.execute(query_credit_notes)
credit_notes = cur.fetchall()

with open('credit_notes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Credit Note Number', 'Date', 'Due Date', 'Customer Name', 'Customer VAT',
        'Customer Email', 'State', 'Payment State', 'Amount Untaxed', 'Amount Tax',
        'Amount Total', 'Amount Residual', 'Payment Term', 'Reference', 'Origin',
        'Currency', 'Notes'
    ])
    writer.writerows(credit_notes)

print(f"✅ Exported {len(credit_notes)} credit notes to credit_notes.csv")

# Extract vendor bills (in_invoice)
print("\nExtracting vendor bills (in_invoice)...")

query_vendor_bills = """
SELECT 
    am.name as bill_number,
    am.invoice_date,
    am.invoice_date_due,
    rp.name as vendor_name,
    rp.vat as vendor_vat,
    rp.email as vendor_email,
    am.state,
    am.payment_state,
    am.amount_untaxed,
    am.amount_tax,
    am.amount_total,
    am.amount_residual,
    apt.name as payment_term,
    am.ref as reference,
    am.invoice_origin as origin,
    rc.name as currency,
    am.narration as notes
FROM account_move am
LEFT JOIN res_partner rp ON am.partner_id = rp.id
LEFT JOIN account_payment_term apt ON am.invoice_payment_term_id = apt.id
LEFT JOIN res_currency rc ON am.currency_id = rc.id
WHERE am.move_type = 'in_invoice'
ORDER BY am.invoice_date, am.name;
"""

cur.execute(query_vendor_bills)
vendor_bills = cur.fetchall()

with open('vendor_bills.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Bill Number', 'Bill Date', 'Due Date', 'Vendor Name', 'Vendor VAT',
        'Vendor Email', 'State', 'Payment State', 'Amount Untaxed', 'Amount Tax',
        'Amount Total', 'Amount Residual', 'Payment Term', 'Reference', 'Origin',
        'Currency', 'Notes'
    ])
    writer.writerows(vendor_bills)

print(f"✅ Exported {len(vendor_bills)} vendor bills to vendor_bills.csv")

# Extract invoice lines for all types
print("\nExtracting invoice lines...")

query_lines = """
SELECT 
    am.name as invoice_number,
    am.move_type,
    pp.default_code as product_code,
    pt.name as product_name,
    aml.name as description,
    aml.quantity,
    aml.price_unit,
    aml.price_subtotal,
    aml.price_total,
    string_agg(at.name::text, ', ') as taxes
FROM account_move_line aml
JOIN account_move am ON aml.move_id = am.id
LEFT JOIN product_product pp ON aml.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN account_move_line_account_tax_rel amlat ON aml.id = amlat.account_move_line_id
LEFT JOIN account_tax at ON amlat.account_tax_id = at.id
WHERE am.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')
  AND aml.account_id IS NOT NULL
GROUP BY am.name, am.move_type, pp.default_code, pt.name, aml.name, 
         aml.quantity, aml.price_unit, aml.price_subtotal, aml.price_total, aml.id
ORDER BY am.name, aml.id;
"""

cur.execute(query_lines)
lines = cur.fetchall()

with open('invoice_lines.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Invoice Number', 'Type', 'Product Code', 'Product Name', 'Description',
        'Quantity', 'Unit Price', 'Subtotal', 'Total', 'Taxes'
    ])
    writer.writerows(lines)

print(f"✅ Exported {len(lines)} invoice lines to invoice_lines.csv")

# Summary
print("\n" + "="*80)
print("EXTRACTION SUMMARY")
print("="*80)
print(f"Customer invoices: {len(invoices)}")
print(f"Credit notes: {len(credit_notes)}")
print(f"Vendor bills: {len(vendor_bills)}")
print(f"Invoice lines: {len(lines)}")
print("\nFiles created:")
print("  - customer_invoices.csv")
print("  - credit_notes.csv")
print("  - vendor_bills.csv")
print("  - invoice_lines.csv")

cur.close()
conn.close()

print("\n✅ All CSV files created successfully!")
