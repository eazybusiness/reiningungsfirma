#!/usr/bin/env python3
"""
Check for duplicate pricelist items (rules) in Odoo
Also check for active subscriptions
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

def check_pricelist_items(models, uid):
    """Check for duplicate pricelist items"""
    
    print("="*80)
    print("CHECKING PRICELIST ITEMS (RULES)")
    print("="*80 + "\n")
    
    # Get all pricelist items
    item_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.pricelist.item', 'search',
        [[]]
    )
    
    items = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.pricelist.item', 'read',
        [item_ids, ['id', 'pricelist_id', 'product_tmpl_id', 'fixed_price', 'min_quantity']]
    )
    
    print(f"📊 Total pricelist items: {len(items)}\n")
    
    # Group by pricelist + product
    item_groups = defaultdict(list)
    for item in items:
        pricelist_name = item['pricelist_id'][1] if item['pricelist_id'] else 'Unknown'
        product_name = item['product_tmpl_id'][1] if item['product_tmpl_id'] else 'Unknown'
        key = f"{pricelist_name}|{product_name}"
        item_groups[key].append(item)
    
    # Find duplicates
    duplicates = {key: items_list for key, items_list in item_groups.items() if len(items_list) > 1}
    
    if duplicates:
        print("="*80)
        print(f"⚠️  DUPLICATE PRICELIST ITEMS FOUND: {len(duplicates)}")
        print("="*80 + "\n")
        
        total_duplicate_items = 0
        for key, items_list in sorted(duplicates.items()):
            pricelist_name, product_name = key.split('|')
            print(f"Pricelist: {pricelist_name}")
            print(f"Product: {product_name}")
            print(f"   Found {len(items_list)} duplicate items:\n")
            
            for item in items_list:
                print(f"   • ID: {item['id']:4} | Price: €{item['fixed_price']:.2f} | Min Qty: {item['min_quantity']}")
            
            total_duplicate_items += len(items_list) - 1  # Count extras only
            print()
        
        print("="*80)
        print(f"📊 SUMMARY:")
        print(f"   Total duplicate combinations: {len(duplicates)}")
        print(f"   Total extra items to remove: {total_duplicate_items}")
        print("="*80)
    else:
        print("✅ No duplicate pricelist items found!")
    
    # Count items per pricelist
    print("\n" + "="*80)
    print("PRICELIST ITEM COUNT")
    print("="*80 + "\n")
    
    pricelist_counts = defaultdict(int)
    for item in items:
        pricelist_name = item['pricelist_id'][1] if item['pricelist_id'] else 'Unknown'
        pricelist_counts[pricelist_name] += 1
    
    # Show pricelists with most items
    print("Top pricelists by item count:\n")
    for pricelist, count in sorted(pricelist_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {pricelist:40} | {count:3} items")
    
    return duplicates

def check_subscriptions(models, uid):
    """Check for active subscriptions"""
    
    print("\n" + "="*80)
    print("CHECKING SUBSCRIPTIONS")
    print("="*80 + "\n")
    
    # Try to find subscription model
    try:
        # Try sale.subscription first
        subscription_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'sale.subscription', 'search',
            [[]]
        )
        
        if subscription_ids:
            subscriptions = models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'sale.subscription', 'read',
                [subscription_ids, ['id', 'name', 'partner_id', 'stage_id', 'recurring_total']]
            )
            
            print(f"📊 Total subscriptions: {len(subscriptions)}\n")
            
            # Group by stage
            stage_groups = defaultdict(list)
            for sub in subscriptions:
                stage_name = sub['stage_id'][1] if sub['stage_id'] else 'No Stage'
                stage_groups[stage_name].append(sub)
            
            print("Subscriptions by stage:\n")
            for stage, subs in sorted(stage_groups.items()):
                print(f"   {stage:30} | {len(subs):3} subscriptions")
            
            print("\n" + "="*80)
            print("Sample subscriptions:\n")
            for sub in subscriptions[:5]:
                partner_name = sub['partner_id'][1] if sub['partner_id'] else 'Unknown'
                stage_name = sub['stage_id'][1] if sub['stage_id'] else 'No Stage'
                total = sub.get('recurring_total', 0)
                print(f"   • {sub['name']:30} | {partner_name:40} | {stage_name:20} | €{total:.2f}")
            
            if len(subscriptions) > 5:
                print(f"\n   ... and {len(subscriptions) - 5} more")
            
        else:
            print("ℹ️  No subscriptions found in the system")
            
    except Exception as e:
        if 'doesn\'t exist' in str(e):
            print("ℹ️  Subscription module not installed or not available")
            print("   This is normal if subscriptions haven't been created yet")
        else:
            print(f"⚠️  Error checking subscriptions: {e}")

def main():
    try:
        models, uid = connect_odoo()
        
        # Check pricelist items
        duplicates = check_pricelist_items(models, uid)
        
        # Check subscriptions
        check_subscriptions(models, uid)
        
        if duplicates:
            print("\n" + "="*80)
            print("⚠️  ACTION REQUIRED:")
            print("="*80)
            print("Duplicate pricelist items found. You may want to:")
            print("1. Review the duplicates above")
            print("2. Run a cleanup script to remove extras")
            print("3. Keep only the most recent or correct item")
            print("="*80)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
