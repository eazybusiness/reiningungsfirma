#!/usr/bin/env python3
"""
Import Pricelist Rules to Odoo Online
Uses the corrected pricelist_items_import.csv with external IDs
"""

import xmlrpc.client
import csv
from datetime import datetime

# Odoo connection settings
ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

# File path
PRICELIST_ITEMS_CSV = 'pricelist_items_import.csv'

def connect_odoo():
    """Connect to Odoo and return models object"""
    print(f"Connecting to {ODOO_URL}...")
    
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    
    if not uid:
        raise Exception("Authentication failed! Check credentials.")
    
    print(f"✅ Connected as user ID: {uid}")
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return models, uid

def get_pricelist_by_name(models, uid, pricelist_name):
    """Get pricelist ID by name"""
    pricelist_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.pricelist', 'search',
        [[['name', '=', pricelist_name]]], 
        {'limit': 1}
    )
    return pricelist_ids[0] if pricelist_ids else None

def get_product_by_internal_ref(models, uid, internal_ref):
    """Get product template ID by Internal Reference (default_code)"""
    product_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.template', 'search',
        [[['default_code', '=', internal_ref]]], 
        {'limit': 1}
    )
    return product_ids[0] if product_ids else None

def parse_external_id(external_id, is_pricelist=False):
    """Parse external ID to extract the actual name/code"""
    # __import__.pricelist_lp_acordia -> LP_ACORDIA
    # __import__.product_srv_mant_rgpd -> SRV-MANT-RGPD
    
    if not external_id:
        return None
    
    # Remove __import__. prefix
    clean_id = external_id.replace('__import__.', '')
    
    # Remove pricelist_ or product_ prefix
    if clean_id.startswith('pricelist_'):
        clean_id = clean_id.replace('pricelist_', '')
        is_pricelist = True
    elif clean_id.startswith('product_'):
        clean_id = clean_id.replace('product_', '')
    
    # For pricelists: keep underscores, just uppercase
    # For products: convert underscores to hyphens
    if is_pricelist:
        clean_id = clean_id.upper()
    else:
        clean_id = clean_id.replace('_', '-').upper()
    
    return clean_id

def load_pricelist_items_from_csv():
    """Load pricelist items from CSV"""
    items = []
    with open(PRICELIST_ITEMS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append({
                'pricelist_external_id': row['pricelist_id/id'],
                'product_external_id': row['product_tmpl_id/id'],
                'applied_on': row['applied_on'],
                'compute_price': row['compute_price'],
                'fixed_price': float(row['fixed_price']) if row['fixed_price'] else 0.0,
                'min_quantity': int(row['min_quantity']) if row['min_quantity'] else 1,
                'date_start': row['date_start'] if row['date_start'] else False,
                'date_end': row['date_end'] if row['date_end'] else False,
            })
    print(f"📄 Loaded {len(items)} pricelist items from CSV")
    return items

def import_pricelist_items(models, uid, test_mode=True, limit=5):
    """Import pricelist items"""
    items = load_pricelist_items_from_csv()
    
    if test_mode:
        items = items[:limit]
        print(f"\n🧪 TEST MODE: Importing only {limit} items")
    else:
        print(f"\n🚀 PRODUCTION MODE: Importing all {len(items)} items")
    
    imported_count = 0
    error_count = 0
    errors = []
    
    for idx, item in enumerate(items, 1):
        pricelist_name = parse_external_id(item['pricelist_external_id'], is_pricelist=True)
        product_ref = parse_external_id(item['product_external_id'], is_pricelist=False)
        
        try:
            # Get pricelist ID
            pricelist_id = get_pricelist_by_name(models, uid, pricelist_name)
            if not pricelist_id:
                error_msg = f"Pricelist not found: {pricelist_name}"
                print(f"❌ [{idx}/{len(items)}] {error_msg}")
                errors.append(error_msg)
                error_count += 1
                continue
            
            # Get product ID by Internal Reference
            product_id = get_product_by_internal_ref(models, uid, product_ref)
            if not product_id:
                error_msg = f"Product not found (Internal Ref): {product_ref}"
                print(f"❌ [{idx}/{len(items)}] {error_msg}")
                errors.append(error_msg)
                error_count += 1
                continue
            
            # Create pricelist item
            # applied_on values: 0=All Products, 1=Product Category, 2=Product, 3=Product Variant
            item_data = {
                'pricelist_id': pricelist_id,
                'product_tmpl_id': product_id,
                'compute_price': 'fixed',
                'fixed_price': item['fixed_price'],
                'min_quantity': item['min_quantity'],
            }
            
            # Add dates if present
            if item['date_start']:
                item_data['date_start'] = item['date_start']
            if item['date_end']:
                item_data['date_end'] = item['date_end']
            
            item_id = models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'product.pricelist.item', 'create',
                [item_data]
            )
            
            print(f"✅ [{idx}/{len(items)}] {pricelist_name} | {product_ref} | €{item['fixed_price']:.2f}")
            imported_count += 1
            
        except Exception as e:
            error_msg = f"Error importing {pricelist_name}/{product_ref}: {e}"
            print(f"❌ [{idx}/{len(items)}] {error_msg}")
            errors.append(error_msg)
            error_count += 1
    
    print("\n" + "="*80)
    print(f"📊 IMPORT SUMMARY:")
    print(f"   ✅ Imported: {imported_count}")
    print(f"   ❌ Errors: {error_count}")
    print("="*80)
    
    if errors and len(errors) <= 10:
        print("\n⚠️  ERRORS:")
        for error in errors:
            print(f"   - {error}")
    
    return imported_count, error_count

def main():
    print("="*80)
    print("IMPORT PRICELIST RULES TO ODOO ONLINE")
    print("="*80)
    
    try:
        models, uid = connect_odoo()
        
        # Test mode first
        print("\n" + "="*80)
        print("STEP 1: TEST IMPORT (5 items)")
        print("="*80)
        imported, errors = import_pricelist_items(models, uid, test_mode=True, limit=5)
        
        if errors > 0:
            print("\n⚠️  Errors found in test import. Please fix before continuing.")
            return 1
        
        # Ask for confirmation
        print("\n" + "="*80)
        response = input("Test successful! Import all items? (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Import cancelled by user.")
            return 0
        
        # Production import
        print("\n" + "="*80)
        print("STEP 2: FULL IMPORT (all items)")
        print("="*80)
        imported, errors = import_pricelist_items(models, uid, test_mode=False)
        
        print("\n✅ Import completed!")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
