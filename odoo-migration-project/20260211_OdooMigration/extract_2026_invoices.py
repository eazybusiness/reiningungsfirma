#!/usr/bin/env python3
"""
Extract 2026 invoices from the new database dump to CSV files
- Customer invoice headers
- Invoice product lines
- Invoice note lines
- Credit notes
- Vendor bills
"""

import psycopg2
import csv
import os

# Database configuration
DB_NAME = 'odoo_backup_2026'
DUMP_PATH = '/home/nop/Downloads/Exartia-odoo-produccion_2026-03-03_20-24-28/dump.sql'

# Output directory
OUTPUT_DIR = '/home/nop/CascadeProjects/freelance_project_cuotes/odoo-migration-project/20260211_OdooMigration/2026_invoices_csv'

print("="*80)
print("EXTRACT 2026 INVOICES FROM DATABASE DUMP")
print("="*80 + "\n")

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"Output directory: {OUTPUT_DIR}\n")

# Step 1: Check if database exists, drop if it does
print("Step 1: Preparing database...")
try:
    conn = psycopg2.connect(dbname='postgres')
    conn.autocommit = True
    cur = conn.cursor()
    
    # Check if database exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone()
    
    if exists:
        print(f"   Database '{DB_NAME}' exists, dropping it...")
        cur.execute(f"DROP DATABASE {DB_NAME}")
        print(f"   ✅ Dropped existing database")
    
    # Create new database
    print(f"   Creating database '{DB_NAME}'...")
    cur.execute(f"CREATE DATABASE {DB_NAME}")
    print(f"   ✅ Database created")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"   ⚠️  Error: {e}")
    print("   Continuing anyway...")

# Step 2: Restore the dump
print("\nStep 2: Restoring database dump...")
print("   This may take several minutes...")

import subprocess

# Check if dump.sql exists
if os.path.exists(DUMP_PATH):
    print(f"   Found dump file: {DUMP_PATH}")
    
    # Restore using psql
    result = subprocess.run(
        ['psql', '-d', DB_NAME, '-f', DUMP_PATH],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("   ✅ Database restored successfully")
    else:
        print(f"   ⚠️  Warning: Restore may have had issues")
        if result.stderr:
            print(f"   Error output: {result.stderr[:200]}")
else:
    print(f"   ❌ Dump file not found: {DUMP_PATH}")
    print("   Please check the path and try again")
    exit(1)

# Step 3: Connect to database and extract data
print("\nStep 3: Connecting to database...")

try:
    conn = psycopg2.connect(dbname=DB_NAME)
    cur = conn.cursor()
    print("   ✅ Connected to database\n")
except Exception as e:
    print(f"   ❌ Error connecting: {e}")
    exit(1)

# Step 4: Extract customer invoices (headers)
print("="*80)
print("EXTRACTING CUSTOMER INVOICE HEADERS (2026)")
print("="*80 + "\n")

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
    AND EXTRACT(YEAR FROM am.invoice_date) = 2026
ORDER BY am.invoice_date, am.name;
"""

cur.execute(query_invoices)
invoices = cur.fetchall()

output_file = os.path.join(OUTPUT_DIR, 'customer_invoices_2026.csv')
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Invoice Number', 'Invoice Date', 'Due Date', 'Customer Name', 
        'Customer VAT', 'Customer Email', 'State', 'Payment State',
        'Amount Untaxed', 'Amount Tax', 'Amount Total', 'Amount Residual',
        'Payment Term', 'Reference', 'Origin', 'Currency', 'Notes'
    ])
    writer.writerows(invoices)

print(f"✅ Extracted {len(invoices)} customer invoices")
print(f"   Output: {output_file}\n")

# Step 5: Extract invoice lines (product lines)
print("="*80)
print("EXTRACTING INVOICE LINES (2026)")
print("="*80 + "\n")

query_lines = """
SELECT 
    am.name as invoice_number,
    CASE 
        WHEN aml.display_type IS NULL OR aml.display_type = 'product' THEN 'product'
        ELSE aml.display_type
    END as type,
    pp.default_code as product_code,
    pt.name as product_name,
    aml.name as description,
    aml.quantity,
    aml.price_unit,
    aml.price_subtotal,
    aml.price_total,
    string_agg(at.name->>'en_US', ', ') as taxes
FROM account_move_line aml
JOIN account_move am ON aml.move_id = am.id
LEFT JOIN product_product pp ON aml.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN account_move_line_account_tax_rel amlat ON aml.id = amlat.account_move_line_id
LEFT JOIN account_tax at ON amlat.account_tax_id = at.id
WHERE am.move_type = 'out_invoice'
    AND EXTRACT(YEAR FROM am.invoice_date) = 2026
    AND (aml.display_type IS NULL OR aml.display_type = 'product')
GROUP BY am.name, aml.id, pp.default_code, pt.name, aml.name, 
         aml.quantity, aml.price_unit, aml.price_subtotal, 
         aml.price_total, aml.display_type, aml.sequence
ORDER BY am.name, aml.sequence;
"""

cur.execute(query_lines)
lines = cur.fetchall()

output_file = os.path.join(OUTPUT_DIR, 'invoice_lines_2026.csv')
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Invoice Number', 'Type', 'Product Code', 'Product Name', 
        'Description', 'Quantity', 'Unit Price', 'Subtotal', 'Total', 'Taxes'
    ])
    writer.writerows(lines)

print(f"✅ Extracted {len(lines)} invoice lines")
print(f"   Output: {output_file}\n")

# Step 6: Extract note lines
print("="*80)
print("EXTRACTING INVOICE NOTE LINES (2026)")
print("="*80 + "\n")

query_notes = """
SELECT 
    am.name as invoice_number,
    aml.sequence,
    aml.name as note_text,
    aml.display_type
FROM account_move_line aml
JOIN account_move am ON aml.move_id = am.id
WHERE am.move_type = 'out_invoice'
    AND EXTRACT(YEAR FROM am.invoice_date) = 2026
    AND aml.display_type = 'line_note'
ORDER BY am.name, aml.sequence;
"""

cur.execute(query_notes)
notes = cur.fetchall()

output_file = os.path.join(OUTPUT_DIR, 'invoice_note_lines_2026.csv')
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Invoice Number', 'Sequence', 'Note Text', 'Display Type'])
    writer.writerows(notes)

print(f"✅ Extracted {len(notes)} note lines")
print(f"   Output: {output_file}\n")

# Step 7: Extract credit notes
print("="*80)
print("EXTRACTING CREDIT NOTES (2026)")
print("="*80 + "\n")

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
    AND EXTRACT(YEAR FROM am.invoice_date) = 2026
ORDER BY am.invoice_date, am.name;
"""

cur.execute(query_credit_notes)
credit_notes = cur.fetchall()

output_file = os.path.join(OUTPUT_DIR, 'credit_notes_2026.csv')
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Credit Note Number', 'Date', 'Due Date', 'Customer Name', 
        'Customer VAT', 'Customer Email', 'State', 'Payment State',
        'Amount Untaxed', 'Amount Tax', 'Amount Total', 'Amount Residual',
        'Payment Term', 'Reference', 'Origin', 'Currency', 'Notes'
    ])
    writer.writerows(credit_notes)

print(f"✅ Extracted {len(credit_notes)} credit notes")
print(f"   Output: {output_file}\n")

# Step 8: Extract vendor bills
print("="*80)
print("EXTRACTING VENDOR BILLS (2026)")
print("="*80 + "\n")

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
    AND EXTRACT(YEAR FROM am.invoice_date) = 2026
ORDER BY am.invoice_date, am.name;
"""

cur.execute(query_vendor_bills)
vendor_bills = cur.fetchall()

output_file = os.path.join(OUTPUT_DIR, 'vendor_bills_2026.csv')
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Bill Number', 'Bill Date', 'Due Date', 'Vendor Name', 
        'Vendor VAT', 'Vendor Email', 'State', 'Payment State',
        'Amount Untaxed', 'Amount Tax', 'Amount Total', 'Amount Residual',
        'Payment Term', 'Reference', 'Origin', 'Currency', 'Notes'
    ])
    writer.writerows(vendor_bills)

print(f"✅ Extracted {len(vendor_bills)} vendor bills")
print(f"   Output: {output_file}\n")

# Close database connection
cur.close()
conn.close()

# Summary
print("="*80)
print("EXTRACTION COMPLETE")
print("="*80 + "\n")

print("Summary:")
print(f"  Customer invoices: {len(invoices)}")
print(f"  Invoice lines: {len(lines)}")
print(f"  Note lines: {len(notes)}")
print(f"  Credit notes: {len(credit_notes)}")
print(f"  Vendor bills: {len(vendor_bills)}")

print(f"\nAll CSV files saved to: {OUTPUT_DIR}")
print("\nFiles created:")
print("  1. customer_invoices_2026.csv")
print("  2. invoice_lines_2026.csv")
print("  3. invoice_note_lines_2026.csv")
print("  4. credit_notes_2026.csv")
print("  5. vendor_bills_2026.csv")

print("\n" + "="*80)
print("✅ Ready for import to Odoo Online")
print("="*80)
