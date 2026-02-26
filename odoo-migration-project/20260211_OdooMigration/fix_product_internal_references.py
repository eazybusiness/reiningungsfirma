#!/usr/bin/env python3
"""
Fix Product Internal References in Odoo Online
Updates all products with their correct Internal Reference (default_code) field
"""

import xmlrpc.client
import csv

# Odoo connection settings
ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

# File paths
PRODUCTS_CSV = 'products.csv'

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

def load_products_from_csv():
    """Load products with their IDs from CSV"""
    products = []
    
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(PRODUCTS_CSV, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    product_id = row['Product ID'].strip()
                    name = row['Name'].strip()
                    if product_id:
                        products.append({
                            'product_id': product_id,
                            'name': name
                        })
            print(f"📄 Loaded {len(products)} products from CSV (encoding: {encoding})")
            return products
        except UnicodeDecodeError:
            continue
    
    raise Exception("Could not read CSV file with any supported encoding")
    return products

def update_product_internal_references(models, uid):
    """Update all products with their Internal Reference"""
    products = load_products_from_csv()
    
    updated_count = 0
    not_found_count = 0
    error_count = 0
    
    for product in products:
        product_id = product['product_id']
        name_snippet = product['name'][:50]  # First 50 chars for matching
        
        try:
            # Search for product by name (partial match)
            product_ids = models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'product.template', 'search',
                [[['name', 'ilike', name_snippet]]], 
                {'limit': 1}
            )
            
            if not product_ids:
                print(f"⚠️  Product not found: {product_id} - {name_snippet}...")
                not_found_count += 1
                continue
            
            # Update the Internal Reference (default_code)
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'product.template', 'write',
                [product_ids, {'default_code': product_id}]
            )
            
            print(f"✅ Updated: {product_id}")
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Error updating {product_id}: {e}")
            error_count += 1
    
    print("\n" + "="*60)
    print(f"📊 SUMMARY:")
    print(f"   ✅ Updated: {updated_count}")
    print(f"   ⚠️  Not found: {not_found_count}")
    print(f"   ❌ Errors: {error_count}")
    print("="*60)

def main():
    print("="*60)
    print("FIX PRODUCT INTERNAL REFERENCES")
    print("="*60)
    
    try:
        models, uid = connect_odoo()
        update_product_internal_references(models, uid)
        print("\n✅ Process completed!")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
