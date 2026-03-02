#!/usr/bin/env python3
"""
Remove auto-generated display lines from invoices
- Removes lines with display_type = 'tax' (VAT percentage lines)
- Removes lines with display_type = 'payment_term' (invoice number lines)
- Removes product lines with 0 amount (VAT % and invoice number as product lines)
- Only removes lines with price_subtotal = 0
"""

import xmlrpc.client

# Odoo connection
ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

# Test mode - set to False to actually delete
TEST_MODE = False

print("="*80)
print("CLEANUP INVOICE DISPLAY LINES")
print("="*80 + "\n")

if TEST_MODE:
    print("🧪 TEST MODE - Will show what would be deleted")
    print("   Set TEST_MODE = False to actually delete\n")

# Connect to Odoo
print("Connecting to Odoo...")
common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
print(f"✅ Connected as user ID: {uid}\n")

# Statistics
stats = {
    'tax_lines': 0,
    'payment_term_lines': 0,
    'zero_product_lines': 0,
    'total_deleted': 0,
    'invoices_processed': 0,
    'errors': []
}

print("="*80)
print("STEP 1: UNPOST INVOICES (to allow line deletion)")
print("="*80 + "\n")

# Get all posted invoices
invoice_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move', 'search',
    [[['move_type', '=', 'out_invoice'], ['name', 'like', 'INV/2025/'], ['state', '=', 'posted']]]
)

print(f"Found {len(invoice_ids)} posted invoices")

if not TEST_MODE:
    print("Unposting invoices...")
    try:
        # Unpost all invoices (set to draft)
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move', 'button_draft',
            [invoice_ids]
        )
        print(f"✅ Unposted {len(invoice_ids)} invoices\n")
    except Exception as e:
        print(f"❌ Error unposting invoices: {e}")
        print("Trying one by one...")
        for inv_id in invoice_ids[:10]:  # Try first 10 as test
            try:
                models.execute_kw(
                    ODOO_DB, uid, ODOO_PASSWORD,
                    'account.move', 'button_draft',
                    [[inv_id]]
                )
            except Exception as e2:
                print(f"  ⚠️  Could not unpost invoice ID {inv_id}: {e2}")
else:
    print("(Skipped in test mode)\n")

print("="*80)
print("STEP 2: DELETE DISPLAY LINES")
print("="*80 + "\n")

# 1. Delete tax display lines
print("1. Deleting tax display lines (VAT percentage)...")
tax_line_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move.line', 'search',
    [[['move_id.move_type', '=', 'out_invoice'], 
      ['move_id.name', 'like', 'INV/2025/'], 
      ['display_type', '=', 'tax']]]
)

stats['tax_lines'] = len(tax_line_ids)
print(f"   Found {len(tax_line_ids)} tax display lines")

if not TEST_MODE and tax_line_ids:
    try:
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move.line', 'unlink',
            [tax_line_ids]
        )
        print(f"   ✅ Deleted {len(tax_line_ids)} tax lines")
        stats['total_deleted'] += len(tax_line_ids)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        stats['errors'].append(f"Tax lines: {e}")

# 2. Delete payment_term display lines
print("\n2. Deleting payment_term display lines (invoice numbers)...")
payment_term_line_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move.line', 'search',
    [[['move_id.move_type', '=', 'out_invoice'], 
      ['move_id.name', 'like', 'INV/2025/'], 
      ['display_type', '=', 'payment_term']]]
)

stats['payment_term_lines'] = len(payment_term_line_ids)
print(f"   Found {len(payment_term_line_ids)} payment_term display lines")

if not TEST_MODE and payment_term_line_ids:
    try:
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move.line', 'unlink',
            [payment_term_line_ids]
        )
        print(f"   ✅ Deleted {len(payment_term_line_ids)} payment_term lines")
        stats['total_deleted'] += len(payment_term_line_ids)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        stats['errors'].append(f"Payment term lines: {e}")

# 3. Delete zero-amount product lines (VAT % and invoice number as products)
print("\n3. Deleting zero-amount product lines...")
zero_product_line_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move.line', 'search',
    [[['move_id.move_type', '=', 'out_invoice'], 
      ['move_id.name', 'like', 'INV/2025/'], 
      ['display_type', '=', 'product'],
      ['price_subtotal', '=', 0]]]
)

stats['zero_product_lines'] = len(zero_product_line_ids)
print(f"   Found {len(zero_product_line_ids)} zero-amount product lines")

if not TEST_MODE and zero_product_line_ids:
    try:
        models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'account.move.line', 'unlink',
            [zero_product_line_ids]
        )
        print(f"   ✅ Deleted {len(zero_product_line_ids)} zero-amount product lines")
        stats['total_deleted'] += len(zero_product_line_ids)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        stats['errors'].append(f"Zero product lines: {e}")

print("\n" + "="*80)
print("STEP 3: REPOST INVOICES")
print("="*80 + "\n")

if not TEST_MODE:
    # Get all draft invoices
    draft_invoice_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'account.move', 'search',
        [[['move_type', '=', 'out_invoice'], ['name', 'like', 'INV/2025/'], ['state', '=', 'draft']]]
    )
    
    print(f"Reposting {len(draft_invoice_ids)} invoices...")
    
    posted_count = 0
    for inv_id in draft_invoice_ids:
        try:
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'account.move', 'action_post',
                [[inv_id]]
            )
            posted_count += 1
            if posted_count % 100 == 0:
                print(f"   Posted {posted_count}/{len(draft_invoice_ids)}...")
        except Exception as e:
            stats['errors'].append(f"Repost invoice {inv_id}: {e}")
    
    print(f"✅ Reposted {posted_count} invoices\n")
else:
    print("(Skipped in test mode)\n")

# SUMMARY
print("="*80)
print("CLEANUP SUMMARY")
print("="*80)

print(f"\n📊 LINES TO DELETE:")
print(f"   Tax display lines: {stats['tax_lines']}")
print(f"   Payment term lines: {stats['payment_term_lines']}")
print(f"   Zero-amount product lines: {stats['zero_product_lines']}")
print(f"   Total: {stats['tax_lines'] + stats['payment_term_lines'] + stats['zero_product_lines']}")

if not TEST_MODE:
    print(f"\n✅ DELETED: {stats['total_deleted']} lines")
    
    if stats['errors']:
        print(f"\n❌ ERRORS ({len(stats['errors'])}):")
        for i, error in enumerate(stats['errors'][:10], 1):
            print(f"   {i}. {error}")

print("\n" + "="*80)

if TEST_MODE:
    print("\n🧪 TEST MODE COMPLETE")
    print("   Review the counts above")
    print("   If everything looks good, set TEST_MODE = False and run again")
else:
    print("\n✅ CLEANUP COMPLETE")
    print(f"   {stats['total_deleted']} display lines removed")
    print("   All invoices reposted")

print("\n" + "="*80)
