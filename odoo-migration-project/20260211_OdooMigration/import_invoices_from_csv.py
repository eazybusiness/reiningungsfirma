#!/usr/bin/env python3
"""
Import invoices from CSV files to Odoo Online
- Prevents duplicates by checking existing invoice numbers
- Imports invoices first, then invoice lines
- Tracks progress and reports skipped/failed records
- Can resume if interrupted
"""

import xmlrpc.client
import csv
import sys
from datetime import datetime

# Odoo connection
ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

# File paths
INVOICE_FILE = '/home/nop/Downloads/zips/invoices/customer_invoices (ONLY 2025).csv'
INVOICE_LINES_FILE = '/home/nop/Downloads/zips/invoices/invoice_lines (ONLY 2025).csv'
CREDIT_NOTES_FILE = '/home/nop/Downloads/zips/invoices/credit_notes.csv'

# Test mode - set to False for full import
TEST_MODE = False
TEST_LIMIT = 5

print("="*80)
print("INVOICE IMPORT TO ODOO ONLINE")
print("="*80 + "\n")

if TEST_MODE:
    print(f"🧪 TEST MODE - Will import only {TEST_LIMIT} invoices")
    print("   Set TEST_MODE = False in script for full import\n")

# Connect to Odoo
print("Connecting to Odoo...")
common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
print(f"✅ Connected as user ID: {uid}\n")

# Statistics
stats = {
    'invoices_total': 0,
    'invoices_imported': 0,
    'invoices_skipped': 0,
    'invoices_failed': 0,
    'lines_total': 0,
    'lines_imported': 0,
    'lines_skipped': 0,
    'lines_failed': 0,
    'errors': []
}

# Track imported invoice numbers to IDs
invoice_map = {}  # {invoice_number: odoo_id}

def check_invoice_exists(invoice_number):
    """Check if invoice already exists in Odoo"""
    try:
        invoice_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'search',
            [[['name', '=', invoice_number], ['move_type', '=', 'out_invoice']]]
        )
        return invoice_ids[0] if invoice_ids else None
    except Exception as e:
        print(f"   ⚠️  Error checking invoice {invoice_number}: {e}")
        return None

def get_customer_by_vat(vat):
    """Find customer by VAT number"""
    if not vat or vat == 'None':
        return None
    
    try:
        partner_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.partner', 'search',
            [[['vat', '=', vat]]]
        )
        return partner_ids[0] if partner_ids else None
    except Exception as e:
        print(f"   ⚠️  Error finding customer with VAT {vat}: {e}")
        return None

def get_product_by_code(product_code):
    """Find product by internal reference (default_code)"""
    if not product_code or product_code == 'None':
        return None
    
    try:
        product_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.product', 'search',
            [[['default_code', '=', product_code]]]
        )
        return product_ids[0] if product_ids else None
    except Exception as e:
        print(f"   ⚠️  Error finding product {product_code}: {e}")
        return None

def get_tax_by_rate(tax_rate=21.0):
    """Find tax by rate (default 21% IVA)"""
    try:
        tax_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.tax', 'search',
            [[['amount', '=', tax_rate], ['type_tax_use', '=', 'sale']]]
        )
        return tax_ids[0] if tax_ids else None
    except Exception as e:
        print(f"   ⚠️  Error finding tax: {e}")
        return None

def import_invoice(row):
    """Import a single invoice"""
    invoice_number = row['Invoice Number']
    
    # Check if already exists
    existing_id = check_invoice_exists(invoice_number)
    if existing_id:
        print(f"   ⏭️  SKIPPED: {invoice_number} (already exists, ID: {existing_id})")
        stats['invoices_skipped'] += 1
        invoice_map[invoice_number] = existing_id
        return existing_id
    
    # Find customer
    customer_vat = row['Customer VAT']
    partner_id = get_customer_by_vat(customer_vat)
    
    if not partner_id:
        error_msg = f"Customer not found for VAT: {customer_vat}"
        print(f"   ❌ FAILED: {invoice_number} - {error_msg}")
        stats['invoices_failed'] += 1
        stats['errors'].append({'invoice': invoice_number, 'error': error_msg})
        return None
    
    # Prepare invoice data
    invoice_data = {
        'move_type': 'out_invoice',
        'partner_id': partner_id,
        'invoice_date': row['Invoice Date'] if row['Invoice Date'] else False,
        'invoice_date_due': row['Due Date'] if row['Due Date'] else False,
        'state': 'draft',  # Import as draft first, then post
        'name': invoice_number,  # Set invoice number
    }
    
    # Add reference if exists
    if row.get('Reference') and row['Reference'] != 'None':
        invoice_data['ref'] = row['Reference']
    
    # Add origin if exists
    if row.get('Origin') and row['Origin'] != 'None':
        invoice_data['invoice_origin'] = row['Origin']
    
    try:
        # Create invoice
        invoice_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'create',
            [invoice_data]
        )
        
        print(f"   ✅ IMPORTED: {invoice_number} (ID: {invoice_id}) - Customer: {row['Customer Name'][:40]}")
        stats['invoices_imported'] += 1
        invoice_map[invoice_number] = invoice_id
        return invoice_id
        
    except Exception as e:
        error_msg = str(e)
        print(f"   ❌ FAILED: {invoice_number} - {error_msg[:80]}")
        stats['invoices_failed'] += 1
        stats['errors'].append({'invoice': invoice_number, 'error': error_msg})
        return None

def import_invoice_line(row, invoice_id):
    """Import a single invoice line"""
    
    # Find product
    product_code = row.get('Product Code', '')
    product_id = None
    
    if product_code and product_code != 'None':
        product_id = get_product_by_code(product_code)
    
    # Prepare line data
    line_data = {
        'move_id': invoice_id,
        'name': row['Description'] if row['Description'] else 'Service',
        'quantity': float(row['Quantity']) if row['Quantity'] else 1.0,
        'price_unit': float(row['Unit Price']) if row['Unit Price'] else 0.0,
    }
    
    # Add product if found
    if product_id:
        line_data['product_id'] = product_id
    
    # Add tax (default 21% IVA)
    tax_id = get_tax_by_rate(21.0)
    if tax_id:
        line_data['tax_ids'] = [(6, 0, [tax_id])]
    
    try:
        line_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move.line', 'create',
            [line_data]
        )
        
        stats['lines_imported'] += 1
        return line_id
        
    except Exception as e:
        error_msg = str(e)
        stats['lines_failed'] += 1
        stats['errors'].append({'invoice': row['Invoice Number'], 'line': row['Description'][:40], 'error': error_msg[:80]})
        return None

def post_invoice(invoice_id, invoice_number):
    """Post (validate) an invoice"""
    try:
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'action_post',
            [[invoice_id]]
        )
        return True
    except Exception as e:
        error_msg = str(e)
        print(f"   ⚠️  Could not post {invoice_number}: {error_msg[:80]}")
        stats['errors'].append({'invoice': invoice_number, 'error': f'Post failed: {error_msg}'})
        return False

# STEP 1: Import invoices
print("="*80)
print("STEP 1: IMPORTING INVOICES")
print("="*80 + "\n")

with open(INVOICE_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    invoices = list(reader)
    stats['invoices_total'] = len(invoices)
    
    if TEST_MODE:
        invoices = invoices[:TEST_LIMIT]
    
    print(f"Processing {len(invoices)} invoices...\n")
    
    for i, row in enumerate(invoices, 1):
        print(f"[{i}/{len(invoices)}] {row['Invoice Number']}")
        import_invoice(row)

# STEP 2: Import invoice lines
print("\n" + "="*80)
print("STEP 2: IMPORTING INVOICE LINES")
print("="*80 + "\n")

with open(INVOICE_LINES_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    all_lines = list(reader)
    
    # Filter lines for imported invoices only
    lines = [line for line in all_lines if line['Invoice Number'] in invoice_map]
    stats['lines_total'] = len(lines)
    
    print(f"Processing {len(lines)} invoice lines for {len(invoice_map)} invoices...\n")
    
    current_invoice = None
    line_count = 0
    
    for i, row in enumerate(lines, 1):
        invoice_number = row['Invoice Number']
        invoice_id = invoice_map.get(invoice_number)
        
        if not invoice_id:
            stats['lines_skipped'] += 1
            continue
        
        # Print invoice header when switching to new invoice
        if invoice_number != current_invoice:
            if current_invoice:
                print(f"      → {line_count} lines imported")
            current_invoice = invoice_number
            line_count = 0
            print(f"\n   {invoice_number} (ID: {invoice_id})")
        
        import_invoice_line(row, invoice_id)
        line_count += 1
    
    if current_invoice:
        print(f"      → {line_count} lines imported")

# STEP 3: Post invoices (validate them)
print("\n" + "="*80)
print("STEP 3: POSTING INVOICES (VALIDATING)")
print("="*80 + "\n")

posted_count = 0
for invoice_number, invoice_id in invoice_map.items():
    if post_invoice(invoice_id, invoice_number):
        posted_count += 1
        print(f"   ✅ Posted: {invoice_number}")

print(f"\n✅ Posted {posted_count}/{len(invoice_map)} invoices")

# SUMMARY
print("\n" + "="*80)
print("IMPORT SUMMARY")
print("="*80)

print(f"\n📊 INVOICES:")
print(f"   Total in CSV: {stats['invoices_total']}")
print(f"   Imported: {stats['invoices_imported']}")
print(f"   Skipped (duplicates): {stats['invoices_skipped']}")
print(f"   Failed: {stats['invoices_failed']}")

print(f"\n📊 INVOICE LINES:")
print(f"   Total for imported invoices: {stats['lines_total']}")
print(f"   Imported: {stats['lines_imported']}")
print(f"   Skipped: {stats['lines_skipped']}")
print(f"   Failed: {stats['lines_failed']}")

if stats['errors']:
    print(f"\n❌ ERRORS ({len(stats['errors'])}):")
    for i, error in enumerate(stats['errors'][:10], 1):
        print(f"   {i}. {error}")
    if len(stats['errors']) > 10:
        print(f"   ... and {len(stats['errors']) - 10} more errors")

print("\n" + "="*80)

if TEST_MODE:
    print("\n🧪 TEST MODE COMPLETE")
    print("   Review the results above")
    print("   If everything looks good, set TEST_MODE = False and run again")
else:
    print("\n✅ IMPORT COMPLETE")
    print(f"   {stats['invoices_imported']} invoices imported")
    print(f"   {stats['lines_imported']} lines imported")
    print(f"   {posted_count} invoices posted")

print("\n" + "="*80)
