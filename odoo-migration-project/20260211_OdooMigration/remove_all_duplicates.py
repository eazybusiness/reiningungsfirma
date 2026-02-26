#!/usr/bin/env python3
"""
Remove ALL duplicate customer records
Keep the record with customer_rank > 0 (the actual customer)
Delete the record with customer_rank = 0 (the duplicate)
"""

import xmlrpc.client
from collections import defaultdict

ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

print("="*80)
print("REMOVING ALL DUPLICATE CUSTOMER RECORDS")
print("="*80 + "\n")

common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

print(f"✅ Connected as user ID: {uid}\n")

# Get ALL partners
partner_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'res.partner', 'search',
    [[]],
    {'context': {'active_test': False}}
)

partners = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'res.partner', 'read',
    [partner_ids, ['id', 'name', 'vat', 'active', 'customer_rank']],
    {'context': {'active_test': False}}
)

print(f"📊 Total partners: {len(partners)}\n")

# Group by VAT
vat_groups = defaultdict(list)
for partner in partners:
    if partner['vat']:
        vat_groups[partner['vat']].append(partner)

# Find duplicates
duplicates = {vat: partners_list for vat, partners_list in vat_groups.items() if len(partners_list) > 1}

print(f"Found {len(duplicates)} VATs with duplicates\n")

deleted_count = 0
kept_count = 0
error_count = 0

for vat, partners_list in sorted(duplicates.items()):
    # Sort by customer_rank (descending) then by ID (ascending)
    # This ensures we keep the customer record (rank > 0) and delete the non-customer (rank = 0)
    partners_sorted = sorted(partners_list, key=lambda x: (-x['customer_rank'], x['id']))
    
    keep = partners_sorted[0]
    remove = partners_sorted[1:]
    
    print(f"VAT: {vat}")
    print(f"   ✅ KEEP:   ID {keep['id']:4} | {keep['name'][:50]:50} | Rank: {keep['customer_rank']}")
    
    for partner in remove:
        try:
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'res.partner', 'unlink',
                [[partner['id']]]
            )
            print(f"   ❌ DELETED: ID {partner['id']:4} | {partner['name'][:50]:50} | Rank: {partner['customer_rank']}")
            deleted_count += 1
        except Exception as e:
            print(f"   ⚠️  ERROR:  ID {partner['id']:4} | Could not delete: {str(e)[:60]}")
            error_count += 1
    
    kept_count += 1

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"VATs processed: {len(duplicates)}")
print(f"Records kept: {kept_count}")
print(f"Records deleted: {deleted_count}")
print(f"Errors: {error_count}")
print("="*80)

if error_count > 0:
    print("\n⚠️  Some records could not be deleted (may have related data)")
    print("   These will need manual review in the UI")
else:
    print("\n✅ All duplicates successfully removed!")
