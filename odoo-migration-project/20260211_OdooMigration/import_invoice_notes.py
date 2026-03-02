#!/usr/bin/env python3
"""
Import invoice note lines to Odoo Online
- Adds note lines (display_type = 'line_note') to existing invoices
- Preserves sequence order
"""

import xmlrpc.client
import csv

# Odoo connection
ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

# File path
NOTES_FILE = '/home/nop/Downloads/zips/invoices/invoice_note_lines.csv'

print("="*80)
print("IMPORT INVOICE NOTE LINES TO ODOO ONLINE")
print("="*80 + "\n")

# Connect to Odoo
print("Connecting to Odoo...")
common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
print(f"✅ Connected as user ID: {uid}\n")

# Statistics
stats = {
    'total': 0,
    'imported': 0,
    'skipped': 0,
    'failed': 0,
    'errors': []
}

def get_invoice_id(invoice_number):
    """Get invoice ID by invoice number"""
    try:
        invoice_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'search',
            [[['name', '=', invoice_number], ['move_type', '=', 'out_invoice']]]
        )
        return invoice_ids[0] if invoice_ids else None
    except Exception as e:
        print(f"   ⚠️  Error finding invoice {invoice_number}: {e}")
        return None

def unpost_invoice(invoice_id):
    """Unpost invoice to allow adding lines"""
    try:
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'button_draft',
            [[invoice_id]]
        )
        return True
    except Exception as e:
        # Invoice might already be in draft
        return True

def post_invoice(invoice_id):
    """Post invoice after adding lines"""
    try:
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'action_post',
            [[invoice_id]]
        )
        return True
    except Exception as e:
        print(f"   ⚠️  Could not post invoice: {e}")
        return False

def add_note_line(invoice_id, note_text, sequence):
    """Add a note line to an invoice"""
    try:
        line_data = {
            'move_id': invoice_id,
            'name': note_text,
            'display_type': 'line_note',
            'sequence': sequence,
        }
        
        line_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move.line', 'create',
            [line_data]
        )
        
        return line_id
    except Exception as e:
        raise Exception(f"Failed to create note line: {e}")

# Read notes from CSV
print("Reading note lines from CSV...")
with open(NOTES_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    notes = list(reader)
    stats['total'] = len(notes)

print(f"Found {len(notes)} note lines to import\n")

# Group notes by invoice
notes_by_invoice = {}
for note in notes:
    inv_num = note['Invoice Number']
    if inv_num not in notes_by_invoice:
        notes_by_invoice[inv_num] = []
    notes_by_invoice[inv_num].append(note)

print(f"Notes for {len(notes_by_invoice)} invoices\n")

print("="*80)
print("IMPORTING NOTE LINES")
print("="*80 + "\n")

# Process each invoice
for i, (invoice_number, invoice_notes) in enumerate(notes_by_invoice.items(), 1):
    print(f"[{i}/{len(notes_by_invoice)}] {invoice_number} ({len(invoice_notes)} notes)")
    
    # Get invoice ID
    invoice_id = get_invoice_id(invoice_number)
    if not invoice_id:
        print(f"   ⚠️  SKIPPED: Invoice not found in Odoo")
        stats['skipped'] += len(invoice_notes)
        continue
    
    try:
        # Unpost invoice
        unpost_invoice(invoice_id)
        
        # Add each note line
        for note in invoice_notes:
            sequence = int(note['Sequence']) if note['Sequence'] else 10
            note_text = note['Note Text']
            
            add_note_line(invoice_id, note_text, sequence)
            stats['imported'] += 1
        
        # Repost invoice
        post_invoice(invoice_id)
        
        print(f"   ✅ Added {len(invoice_notes)} note lines")
        
    except Exception as e:
        error_msg = str(e)[:100]
        print(f"   ❌ FAILED: {error_msg}")
        stats['failed'] += len(invoice_notes)
        stats['errors'].append({'invoice': invoice_number, 'error': error_msg})

# SUMMARY
print("\n" + "="*80)
print("IMPORT SUMMARY")
print("="*80)

print(f"\n📊 NOTE LINES:")
print(f"   Total in CSV: {stats['total']}")
print(f"   Imported: {stats['imported']}")
print(f"   Skipped: {stats['skipped']}")
print(f"   Failed: {stats['failed']}")

if stats['errors']:
    print(f"\n❌ ERRORS ({len(stats['errors'])}):")
    for i, error in enumerate(stats['errors'][:10], 1):
        print(f"   {i}. {error}")

print("\n" + "="*80)
print(f"\n✅ IMPORT COMPLETE")
print(f"   {stats['imported']} note lines imported")
print(f"   {len(notes_by_invoice)} invoices updated")
print("\n" + "="*80)
