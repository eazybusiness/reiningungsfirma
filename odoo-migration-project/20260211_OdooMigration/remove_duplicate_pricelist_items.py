#!/usr/bin/env python3
"""
Remove duplicate pricelist items from Odoo
Keeps the OLDEST item (lowest ID) and deletes newer duplicates
"""

import xmlrpc.client
from collections import defaultdict

# Odoo connection settings
ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

def connect_odoo():
    """Connect to Odoo and return models object"""
    print(f"Connecting to {ODOO_URL}...")
    
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    
    if not uid:
        raise Exception("Authentication failed! Check credentials.")
    
    print(f"✅ Connected as user ID: {uid}\n")
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return models, uid

print("="*80)
print("REMOVING DUPLICATE PRICELIST ITEMS")
print("="*80 + "\n")

models, uid = connect_odoo()

# Get all pricelist items
item_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'product.pricelist.item', 'search',
    [[]]
)

items = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'product.pricelist.item', 'read',
    [item_ids, ['id', 'pricelist_id', 'product_tmpl_id', 'fixed_price']]
)

print(f"📊 Total pricelist items before cleanup: {len(items)}\n")

# Group by pricelist + product
item_groups = defaultdict(list)
for item in items:
    pricelist_id = item['pricelist_id'][0] if item['pricelist_id'] else 0
    product_id = item['product_tmpl_id'][0] if item['product_tmpl_id'] else 0
    key = f"{pricelist_id}|{product_id}"
    item_groups[key].append(item)

# Find and remove duplicates
duplicates = {key: items_list for key, items_list in item_groups.items() if len(items_list) > 1}

if not duplicates:
    print("✅ No duplicates found!")
else:
    print(f"Found {len(duplicates)} duplicate combinations\n")
    
    deleted_count = 0
    
    for key, items_list in sorted(duplicates.items()):
        # Sort by ID (keep oldest - lowest ID)
        items_sorted = sorted(items_list, key=lambda x: x['id'])
        
        keep_item = items_sorted[0]
        remove_items = items_sorted[1:]
        
        pricelist_name = keep_item['pricelist_id'][1] if keep_item['pricelist_id'] else 'Unknown'
        product_name = keep_item['product_tmpl_id'][1] if keep_item['product_tmpl_id'] else 'Unknown'
        
        print(f"{pricelist_name}")
        print(f"   Product: {product_name[:60]}")
        print(f"   ✅ KEEP:   ID {keep_item['id']:4} | €{keep_item['fixed_price']:.2f}")
        
        for item in remove_items:
            try:
                models.execute_kw(
                    ODOO_DB, uid, ODOO_PASSWORD,
                    'product.pricelist.item', 'unlink',
                    [[item['id']]]
                )
                print(f"   ❌ DELETED: ID {item['id']:4} | €{item['fixed_price']:.2f}")
                deleted_count += 1
            except Exception as e:
                print(f"   ⚠️  ERROR deleting ID {item['id']}: {e}")
        
        print()
    
    print("="*80)
    print(f"📊 SUMMARY:")
    print(f"   Duplicate combinations found: {len(duplicates)}")
    print(f"   Items deleted: {deleted_count}")
    print(f"   Items remaining: {len(items) - deleted_count}")
    print("="*80)
    
    print("\n✅ Cleanup completed!")
