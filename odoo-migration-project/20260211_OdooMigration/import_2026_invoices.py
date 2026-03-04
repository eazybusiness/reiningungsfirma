#!/usr/bin/env python3
"""
Import 2026 invoices to Odoo Online
- Import invoice headers
- Import invoice lines
- Import note lines
- Update invoice sequence to INV/2026/00299
"""

import xmlrpc.client
import csv
from datetime import datetime

# Odoo connection
ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

# CSV files
CSV_DIR = '/home/nop/CascadeProjects/freelance_project_cuotes/odoo-migration-project/20260211_OdooMigration/2026_invoices_csv'
INVOICES_FILE = f'{CSV_DIR}/customer_invoices_2026.csv'
LINES_FILE = f'{CSV_DIR}/invoice_lines_2026.csv'
NOTES_FILE = f'{CSV_DIR}/invoice_note_lines_2026.csv'

print("="*80)
print("IMPORT 2026 INVOICES TO ODOO ONLINE")
print("="*80 + "\n")

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
    'lines_imported': 0,
    'notes_imported': 0,
    'errors': []
}

# Cache for lookups
customer_cache = {}
product_cache = {}
tax_cache = {}

def get_customer_id(vat, name):
    """Get customer ID by VAT or name"""
    if vat in customer_cache:
        return customer_cache[vat]
    
    # Try by VAT first
    if vat:
        partner_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.partner', 'search',
            [[['vat', '=', vat]]]
        )
        if partner_ids:
            customer_cache[vat] = partner_ids[0]
            return partner_ids[0]
    
    # Try by name
    partner_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'res.partner', 'search',
        [[['name', '=', name]]]
    )
    if partner_ids:
        if vat:
            customer_cache[vat] = partner_ids[0]
        return partner_ids[0]
    
    return None

def get_product_id(product_name):
    """Get product ID by name"""
    if product_name in product_cache:
        return product_cache[product_name]
    
    # Search by name
    product_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.product', 'search',
        [[['name', '=', product_name]]]
    )
    
    if product_ids:
        product_cache[product_name] = product_ids[0]
        return product_ids[0]
    
    return None

def get_tax_ids(tax_string):
    """Get tax IDs from tax string like '21% IVA'"""
    if not tax_string or tax_string == 'None':
        return []
    
    if tax_string in tax_cache:
        return tax_cache[tax_string]
    
    # Parse tax names
    tax_names = [t.strip() for t in tax_string.split(',')]
    tax_ids = []
    
    for tax_name in tax_names:
        # Search for tax
        found_tax_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.tax', 'search',
            [[['name', 'ilike', tax_name], ['type_tax_use', '=', 'sale']]]
        )
        if found_tax_ids:
            tax_ids.append(found_tax_ids[0])
    
    tax_cache[tax_string] = tax_ids
    return tax_ids

# Step 1: Load CSV files
print("="*80)
print("LOADING CSV FILES")
print("="*80 + "\n")

print("Loading invoices...")
with open(INVOICES_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    invoices = list(reader)
stats['invoices_total'] = len(invoices)
print(f"✅ Loaded {len(invoices)} invoices\n")

print("Loading invoice lines...")
with open(LINES_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    lines = list(reader)
print(f"✅ Loaded {len(lines)} invoice lines\n")

print("Loading note lines...")
with open(NOTES_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    notes = list(reader)
print(f"✅ Loaded {len(notes)} note lines\n")

# Group lines by invoice
lines_by_invoice = {}
for line in lines:
    inv_num = line['Invoice Number']
    if inv_num not in lines_by_invoice:
        lines_by_invoice[inv_num] = []
    lines_by_invoice[inv_num].append(line)

# Group notes by invoice
notes_by_invoice = {}
for note in notes:
    inv_num = note['Invoice Number']
    if inv_num not in notes_by_invoice:
        notes_by_invoice[inv_num] = []
    notes_by_invoice[inv_num].append(note)

# Step 2: Import invoices
print("="*80)
print("IMPORTING INVOICES")
print("="*80 + "\n")

for i, invoice in enumerate(invoices, 1):
    inv_num = invoice['Invoice Number']
    print(f"[{i}/{len(invoices)}] {inv_num}")
    
    # Check if invoice already exists
    existing = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'account.move', 'search',
        [[['name', '=', inv_num], ['move_type', '=', 'out_invoice']]]
    )
    
    if existing:
        print(f"   ⚠️  SKIPPED: Invoice already exists")
        stats['invoices_skipped'] += 1
        continue
    
    try:
        # Get customer
        customer_id = get_customer_id(invoice['Customer VAT'], invoice['Customer Name'])
        if not customer_id:
            print(f"   ❌ FAILED: Customer not found: {invoice['Customer Name']}")
            stats['invoices_failed'] += 1
            stats['errors'].append({'invoice': inv_num, 'error': 'Customer not found'})
            continue
        
        # Prepare invoice data (filter out None and empty values)
        invoice_data = {
            'partner_id': customer_id,
            'move_type': 'out_invoice',
        }
        
        if invoice.get('Invoice Date') and invoice['Invoice Date'].strip():
            invoice_data['invoice_date'] = invoice['Invoice Date']
        if invoice.get('Due Date') and invoice['Due Date'].strip():
            invoice_data['invoice_date_due'] = invoice['Due Date']
        if invoice.get('Reference') and invoice['Reference'].strip():
            invoice_data['ref'] = invoice['Reference']
        if invoice.get('Origin') and invoice['Origin'].strip():
            invoice_data['invoice_origin'] = invoice['Origin']
        if invoice.get('Notes') and invoice['Notes'].strip():
            invoice_data['narration'] = invoice['Notes']
        
        # Create invoice
        invoice_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'create',
            [invoice_data]
        )
        
        # Add invoice lines
        invoice_lines = lines_by_invoice.get(inv_num, [])
        for line in invoice_lines:
            product_id = get_product_id(line['Product Name'])
            
            if not product_id:
                # Create line without product (service)
                line_data = {
                    'move_id': invoice_id,
                    'name': line['Description'],
                    'quantity': float(line['Quantity']) if line['Quantity'] else 1.0,
                    'price_unit': float(line['Unit Price']) if line['Unit Price'] else 0.0,
                }
            else:
                line_data = {
                    'move_id': invoice_id,
                    'product_id': product_id,
                    'name': line['Description'],
                    'quantity': float(line['Quantity']) if line['Quantity'] else 1.0,
                    'price_unit': float(line['Unit Price']) if line['Unit Price'] else 0.0,
                }
            
            # Add taxes
            tax_ids = get_tax_ids(line['Taxes'])
            if tax_ids:
                line_data['tax_ids'] = [(6, 0, tax_ids)]
            
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'account.move.line', 'create',
                [line_data]
            )
            stats['lines_imported'] += 1
        
        # Add note lines
        invoice_notes = notes_by_invoice.get(inv_num, [])
        for note in invoice_notes:
            note_text = note.get('Note Text', '').strip()
            if not note_text:
                continue
                
            note_data = {
                'move_id': invoice_id,
                'name': note_text,
                'display_type': 'line_note',
                'sequence': int(note['Sequence']) if note.get('Sequence') and note['Sequence'].strip() else 10,
            }
            
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'account.move.line', 'create',
                [note_data]
            )
            stats['notes_imported'] += 1
        
        # Post the invoice
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'action_post',
            [[invoice_id]]
        )
        
        print(f"   ✅ Imported: {len(invoice_lines)} lines, {len(invoice_notes)} notes")
        stats['invoices_imported'] += 1
        
    except Exception as e:
        error_msg = str(e)[:100]
        print(f"   ❌ FAILED: {error_msg}")
        stats['invoices_failed'] += 1
        stats['errors'].append({'invoice': inv_num, 'error': error_msg})

# Step 3: Update invoice sequence
print("\n" + "="*80)
print("UPDATING INVOICE SEQUENCE")
print("="*80 + "\n")

try:
    # Find the invoice sequence for 2026
    sequence_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'ir.sequence', 'search',
        [[['code', '=', 'account.move'], ['name', 'ilike', '2026']]]
    )
    
    if not sequence_ids:
        # Try to find the main invoice sequence
        sequence_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'ir.sequence', 'search',
            [[['code', '=', 'account.move']]]
        )
    
    if sequence_ids:
        # Update the sequence to 299
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'ir.sequence', 'write',
            [[sequence_ids[0]], {'number_next': 299}]
        )
        print(f"✅ Updated invoice sequence to 299")
        print(f"   Next invoice will be: INV/2026/00299")
    else:
        print("⚠️  Could not find invoice sequence - please update manually")
        print("   Go to: Settings → Technical → Sequences")
        print("   Find: Invoice sequence for 2026")
        print("   Set 'Next Number' to: 299")
        
except Exception as e:
    print(f"⚠️  Error updating sequence: {e}")
    print("   Please update manually in Odoo:")
    print("   Settings → Technical → Sequences → Invoice 2026")
    print("   Set 'Next Number' to: 299")

# Summary
print("\n" + "="*80)
print("IMPORT SUMMARY")
print("="*80)

print(f"\n📊 INVOICES:")
print(f"   Total in CSV: {stats['invoices_total']}")
print(f"   Imported: {stats['invoices_imported']}")
print(f"   Skipped (duplicates): {stats['invoices_skipped']}")
print(f"   Failed: {stats['invoices_failed']}")

print(f"\n📊 LINES:")
print(f"   Invoice lines imported: {stats['lines_imported']}")
print(f"   Note lines imported: {stats['notes_imported']}")

if stats['errors']:
    print(f"\n❌ ERRORS ({len(stats['errors'])}):")
    for i, error in enumerate(stats['errors'][:10], 1):
        print(f"   {i}. {error['invoice']}: {error['error']}")
    if len(stats['errors']) > 10:
        print(f"   ... and {len(stats['errors']) - 10} more")

print("\n" + "="*80)
print(f"✅ IMPORT COMPLETE")
print(f"   {stats['invoices_imported']} invoices imported")
print(f"   {stats['lines_imported']} lines imported")
print(f"   {stats['notes_imported']} notes imported")
print("="*80)
