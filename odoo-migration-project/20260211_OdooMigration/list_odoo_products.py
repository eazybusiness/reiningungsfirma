#!/usr/bin/env python3
"""
List all products in Odoo to see what we're working with
"""

import xmlrpc.client

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
    
    print(f"✅ Connected as user ID: {uid}")
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return models, uid

def list_products(models, uid):
    """List all products"""
    
    # Get all products
    product_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.template', 'search',
        [[]]
    )
    
    print(f"\n📦 Total products in Odoo: {len(product_ids)}")
    
    # Get product details
    products = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.template', 'read',
        [product_ids, ['id', 'name', 'default_code']]
    )
    
    print("\n" + "="*100)
    print(f"{'ID':<6} | {'Internal Ref':<30} | {'Name':<60}")
    print("="*100)
    
    for product in sorted(products, key=lambda x: x['id']):
        pid = product['id']
        ref = product['default_code'] or '(EMPTY)'
        name = product['name'][:60]
        print(f"{pid:<6} | {ref:<30} | {name}")

def main():
    try:
        models, uid = connect_odoo()
        list_products(models, uid)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
