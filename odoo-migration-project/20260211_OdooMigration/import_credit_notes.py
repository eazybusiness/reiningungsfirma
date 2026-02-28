#!/usr/bin/env python3
"""
Import credit notes from CSV to Odoo Online
- Prevents duplicates by checking existing credit note numbers
- Imports credit notes with lines
- Tracks progress and reports skipped/failed records
"""

import xmlrpc.client
import csv

# Odoo connection
ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

# File paths
CREDIT_NOTES_FILE = '/home/nop/Downloads/zips/invoices/credit_notes.csv'

print("="*80)
print("CREDIT NOTES IMPORT TO ODOO ONLINE")
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
    'posted': 0,
    'errors': []
}

def check_credit_note_exists(credit_note_number):
    """Check if credit note already exists in Odoo"""
    try:
        cn_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'search',
            [[['name', '=', credit_note_number], ['move_type', '=', 'out_refund']]]
        )
        return cn_ids[0] if cn_ids else None
    except Exception as e:
        print(f"   ⚠️  Error checking credit note {credit_note_number}: {e}")
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

def import_credit_note(row):
    """Import a single credit note"""
    cn_number = row['Credit Note Number']
    
    # Check if already exists
    existing_id = check_credit_note_exists(cn_number)
    if existing_id:
        print(f"   ⏭️  SKIPPED: {cn_number} (already exists, ID: {existing_id})")
        stats['skipped'] += 1
        return existing_id
    
    # Find customer
    customer_vat = row['Customer VAT']
    partner_id = get_customer_by_vat(customer_vat)
    
    if not partner_id:
        error_msg = f"Customer not found for VAT: {customer_vat}"
        print(f"   ❌ FAILED: {cn_number} - {error_msg}")
        stats['failed'] += 1
        stats['errors'].append({'credit_note': cn_number, 'error': error_msg})
        return None
    
    # Prepare credit note data
    cn_data = {
        'move_type': 'out_refund',
        'partner_id': partner_id,
        'invoice_date': row['Date'] if row['Date'] else False,
        'invoice_date_due': row['Due Date'] if row['Due Date'] else False,
        'state': 'draft',
        'name': cn_number,
    }
    
    # Add reference if exists
    if row.get('Reference') and row['Reference'] != 'None':
        cn_data['ref'] = row['Reference']
    
    # Add origin if exists
    if row.get('Origin') and row['Origin'] != 'None':
        cn_data['invoice_origin'] = row['Origin']
    
    # Add notes if exists
    if row.get('Notes') and row['Notes'] != 'None':
        cn_data['narration'] = row['Notes']
    
    try:
        # Create credit note
        cn_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'create',
            [cn_data]
        )
        
        # Add a line with the amount
        amount_untaxed = float(row['Amount Untaxed']) if row['Amount Untaxed'] else 0.0
        
        if amount_untaxed > 0:
            tax_id = get_tax_by_rate(21.0)
            line_data = {
                'move_id': cn_id,
                'name': row.get('Notes', 'Credit Note') if row.get('Notes') else 'Credit Note',
                'quantity': 1.0,
                'price_unit': amount_untaxed,
            }
            
            if tax_id:
                line_data['tax_ids'] = [(6, 0, [tax_id])]
            
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'account.move.line', 'create',
                [line_data]
            )
        
        # Post the credit note
        try:
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'account.move', 'action_post',
                [[cn_id]]
            )
            stats['posted'] += 1
            print(f"   ✅ IMPORTED & POSTED: {cn_number} (ID: {cn_id}) - Customer: {row['Customer Name'][:40]}")
        except Exception as e:
            print(f"   ✅ IMPORTED (draft): {cn_number} (ID: {cn_id}) - Could not post: {str(e)[:60]}")
        
        stats['imported'] += 1
        return cn_id
        
    except Exception as e:
        error_msg = str(e)
        print(f"   ❌ FAILED: {cn_number} - {error_msg[:80]}")
        stats['failed'] += 1
        stats['errors'].append({'credit_note': cn_number, 'error': error_msg})
        return None

# Import credit notes
print("="*80)
print("IMPORTING CREDIT NOTES")
print("="*80 + "\n")

with open(CREDIT_NOTES_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    credit_notes = list(reader)
    stats['total'] = len(credit_notes)
    
    print(f"Processing {len(credit_notes)} credit notes...\n")
    
    for i, row in enumerate(credit_notes, 1):
        print(f"[{i}/{len(credit_notes)}] {row['Credit Note Number']}")
        import_credit_note(row)

# SUMMARY
print("\n" + "="*80)
print("IMPORT SUMMARY")
print("="*80)

print(f"\n📊 CREDIT NOTES:")
print(f"   Total in CSV: {stats['total']}")
print(f"   Imported: {stats['imported']}")
print(f"   Posted: {stats['posted']}")
print(f"   Skipped (duplicates): {stats['skipped']}")
print(f"   Failed: {stats['failed']}")

if stats['errors']:
    print(f"\n❌ ERRORS ({len(stats['errors'])}):")
    for i, error in enumerate(stats['errors'], 1):
        print(f"   {i}. {error}")

print("\n" + "="*80)
print(f"\n✅ IMPORT COMPLETE")
print(f"   {stats['imported']} credit notes imported")
print(f"   {stats['posted']} credit notes posted")
print("\n" + "="*80)
