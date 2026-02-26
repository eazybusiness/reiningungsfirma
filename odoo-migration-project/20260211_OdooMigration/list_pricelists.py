#!/usr/bin/env python3
"""
List all pricelists in Odoo to see their exact names
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

def list_pricelists(models, uid):
    """List all pricelists"""
    
    # Get all pricelists
    pricelist_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.pricelist', 'search',
        [[]]
    )
    
    print(f"\n📋 Total pricelists in Odoo: {len(pricelist_ids)}")
    
    # Get pricelist details
    pricelists = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.pricelist', 'read',
        [pricelist_ids, ['id', 'name']]
    )
    
    print("\n" + "="*80)
    print(f"{'ID':<6} | {'Pricelist Name':<70}")
    print("="*80)
    
    for pl in sorted(pricelists, key=lambda x: x['name']):
        print(f"{pl['id']:<6} | {pl['name']}")

def main():
    try:
        models, uid = connect_odoo()
        list_pricelists(models, uid)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
