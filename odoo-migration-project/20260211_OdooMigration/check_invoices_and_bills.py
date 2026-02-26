#!/usr/bin/env python3
"""
Check for invoices (customer invoices) and bills (vendor bills) in Odoo
"""

import xmlrpc.client

ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

print("="*80)
print("CHECKING INVOICES AND BILLS")
print("="*80 + "\n")

common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

print(f"✅ Connected as user ID: {uid}\n")

# Check customer invoices (out_invoice)
print("="*80)
print("CUSTOMER INVOICES (Facturas de cliente)")
print("="*80 + "\n")

invoice_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move', 'search',
    [[['move_type', '=', 'out_invoice']]]
)

print(f"📊 Total customer invoices: {len(invoice_ids)}\n")

if invoice_ids:
    invoices = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'account.move', 'read',
        [invoice_ids[:10], ['id', 'name', 'partner_id', 'invoice_date', 'amount_total', 'state']]
    )
    
    print("Sample invoices:\n")
    for inv in invoices:
        partner_name = inv['partner_id'][1] if inv['partner_id'] else 'Unknown'
        date = inv.get('invoice_date', 'N/A')
        state = inv.get('state', 'N/A')
        total = inv.get('amount_total', 0)
        print(f"   • {inv['name']:20} | {partner_name:40} | {date} | €{total:10.2f} | {state}")
    
    if len(invoice_ids) > 10:
        print(f"\n   ... and {len(invoice_ids) - 10} more")
else:
    print("ℹ️  No customer invoices found")
    print("   This is expected - invoices are generated from subscriptions")

print()

# Check vendor bills (in_invoice)
print("="*80)
print("VENDOR BILLS (Facturas de proveedor)")
print("="*80 + "\n")

bill_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move', 'search',
    [[['move_type', '=', 'in_invoice']]]
)

print(f"📊 Total vendor bills: {len(bill_ids)}\n")

if bill_ids:
    bills = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'account.move', 'read',
        [bill_ids[:10], ['id', 'name', 'partner_id', 'invoice_date', 'amount_total', 'state']]
    )
    
    print("Sample bills:\n")
    for bill in bills:
        partner_name = bill['partner_id'][1] if bill['partner_id'] else 'Unknown'
        date = bill.get('invoice_date', 'N/A')
        state = bill.get('state', 'N/A')
        total = bill.get('amount_total', 0)
        print(f"   • {bill['name']:20} | {partner_name:40} | {date} | €{total:10.2f} | {state}")
    
    if len(bill_ids) > 10:
        print(f"\n   ... and {len(bill_ids) - 10} more")
else:
    print("ℹ️  No vendor bills found")
    print("   This is expected - bills are created manually or imported")

print()

# Check credit notes
print("="*80)
print("CREDIT NOTES (Notas de crédito)")
print("="*80 + "\n")

credit_note_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move', 'search',
    [[['move_type', 'in', ['out_refund', 'in_refund']]]]
)

print(f"📊 Total credit notes: {len(credit_note_ids)}\n")

if credit_note_ids:
    print("Credit notes exist")
else:
    print("ℹ️  No credit notes found")

print()

# Summary
print("="*80)
print("SUMMARY")
print("="*80 + "\n")

print(f"Customer invoices (out_invoice): {len(invoice_ids)}")
print(f"Vendor bills (in_invoice): {len(bill_ids)}")
print(f"Credit notes (refunds): {len(credit_note_ids)}")
print()

if len(invoice_ids) == 0 and len(bill_ids) == 0:
    print("ℹ️  No invoices or bills found in the system")
    print("   This is expected for a fresh migration")
    print("   Invoices will be generated from subscriptions")
    print("   Bills are created manually or imported separately")
else:
    print("✅ Found accounting documents in the system")
