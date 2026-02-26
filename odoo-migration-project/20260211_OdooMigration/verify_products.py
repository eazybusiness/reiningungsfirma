#!/usr/bin/env python3
"""
Verify Product Internal References in Odoo Online
Checks if all products have correct Internal Reference field set
"""

import xmlrpc.client
import csv

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

def verify_products(models, uid):
    """Verify all products have Internal Reference set"""
    
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
        [product_ids, ['name', 'default_code']]
    )
    
    with_reference = 0
    without_reference = 0
    
    print("\n" + "="*80)
    print("PRODUCT VERIFICATION REPORT")
    print("="*80)
    
    for product in products:
        name = product['name'][:60]
        ref = product['default_code'] or '(EMPTY)'
        
        if product['default_code']:
            print(f"✅ {ref:30} | {name}")
            with_reference += 1
        else:
            print(f"❌ {'(NO REFERENCE)':30} | {name}")
            without_reference += 1
    
    print("\n" + "="*80)
    print(f"📊 SUMMARY:")
    print(f"   ✅ Products WITH Internal Reference: {with_reference}")
    print(f"   ❌ Products WITHOUT Internal Reference: {without_reference}")
    print("="*80)
    
    if without_reference == 0:
        print("\n🎉 ALL PRODUCTS HAVE INTERNAL REFERENCES! Ready to import pricelist rules.")
    else:
        print(f"\n⚠️  {without_reference} products need Internal Reference. Run fix_product_internal_references.py")

def main():
    try:
        models, uid = connect_odoo()
        verify_products(models, uid)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
