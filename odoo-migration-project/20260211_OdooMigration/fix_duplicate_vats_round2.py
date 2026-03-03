#!/usr/bin/env python3
"""
Fix duplicate VAT issues for ILV Silver Transactions S.L. and Beyond the Universe Group, S.L.
Similar to the previous duplicate cleanup, we'll keep the record with higher customer_rank
and delete the duplicate.
"""

import xmlrpc.client

# Odoo connection
ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

print("="*80)
print("FIX DUPLICATE VAT ISSUES - ROUND 2")
print("="*80 + "\n")

# Connect to Odoo
print("Connecting to Odoo...")
common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
print(f"✅ Connected as user ID: {uid}\n")

# Statistics
stats = {
    'checked': 0,
    'deleted': 0,
    'kept': 0,
    'errors': []
}

print("="*80)
print("DUPLICATE VAT ANALYSIS")
print("="*80 + "\n")

# The two duplicate VATs we found
duplicates = {
    'B64823123': [
        {'id': 553, 'name': 'ILV & Lawtaxfin, S.L.', 'customer_rank': 7},
        {'id': 609, 'name': 'ILV Silver Transactions S.L.', 'customer_rank': 1}
    ],
    'B72773096': [
        {'id': 608, 'name': 'Beyond the Universe Group, S.L.', 'customer_rank': 25},
        {'id': 416, 'name': 'Beyond the Universe Group, S.L.', 'customer_rank': 0}
    ]
}

for vat, partners in duplicates.items():
    print(f"VAT: {vat}")
    for p in partners:
        print(f"  ID {p['id']:4} | {p['name']:60} | Customer rank: {p['customer_rank']}")
    print()

print("="*80)
print("RESOLUTION STRATEGY")
print("="*80 + "\n")

print("For each duplicate VAT:")
print("  1. Keep the record with HIGHER customer_rank (more invoices)")
print("  2. Delete the record with LOWER customer_rank")
print("  3. This preserves invoice relationships\n")

# Process each duplicate
for vat, partners in duplicates.items():
    print(f"\nProcessing VAT {vat}:")
    stats['checked'] += 1
    
    # Sort by customer_rank (descending)
    sorted_partners = sorted(partners, key=lambda x: x['customer_rank'], reverse=True)
    
    # Keep the first (highest rank), delete the rest
    to_keep = sorted_partners[0]
    to_delete = sorted_partners[1:]
    
    print(f"  ✅ KEEP:   ID {to_keep['id']:4} | {to_keep['name']:60} | Rank: {to_keep['customer_rank']}")
    stats['kept'] += 1
    
    for partner in to_delete:
        print(f"  ❌ DELETE: ID {partner['id']:4} | {partner['name']:60} | Rank: {partner['customer_rank']}")
        
        try:
            # Delete the duplicate
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'res.partner', 'unlink',
                [[partner['id']]]
            )
            print(f"     → Deleted successfully")
            stats['deleted'] += 1
        except Exception as e:
            error_msg = str(e)[:100]
            print(f"     → ERROR: {error_msg}")
            stats['errors'].append({
                'vat': vat,
                'id': partner['id'],
                'name': partner['name'],
                'error': error_msg
            })

# SUMMARY
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print(f"\nVATs processed: {stats['checked']}")
print(f"Records kept: {stats['kept']}")
print(f"Records deleted: {stats['deleted']}")

if stats['errors']:
    print(f"\n❌ ERRORS ({len(stats['errors'])}):")
    for i, error in enumerate(stats['errors'], 1):
        print(f"   {i}. VAT {error['vat']} - ID {error['id']} ({error['name']})")
        print(f"      Error: {error['error']}")

print("\n" + "="*80)
print("✅ DUPLICATE CLEANUP COMPLETE")
print("="*80)

# Verify no more duplicates
print("\nVerifying no duplicates remain...")
all_partners = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'res.partner', 'search_read',
    [[['vat', '!=', False]]],
    {'fields': ['id', 'name', 'vat', 'customer_rank']}
)

from collections import defaultdict
vat_groups = defaultdict(list)
for p in all_partners:
    if p.get('vat'):
        vat_groups[p['vat']].append(p)

remaining_duplicates = {vat: partners for vat, partners in vat_groups.items() if len(partners) > 1}

if remaining_duplicates:
    print(f"⚠️  WARNING: {len(remaining_duplicates)} duplicate VATs still remain")
    for vat, partners in remaining_duplicates.items():
        print(f"   VAT {vat}: {len(partners)} records")
else:
    print("✅ No duplicate VATs found - all clean!")

print("\n" + "="*80)
