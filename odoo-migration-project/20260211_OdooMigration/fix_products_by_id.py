#!/usr/bin/env python3
"""
Fix Product Internal References by manually mapping Odoo IDs to Product IDs
This is more reliable than name matching since many products have similar names
"""

import xmlrpc.client

# Odoo connection settings
ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

# Manual mapping: Odoo Product ID -> Internal Reference
# Based on the order and content from products.csv
PRODUCT_MAPPING = {
    119: 'SRV-SETUP-RGPD',
    120: 'SRV-SETUP-LSSI',
    121: 'SRV-SETUP-CD',
    122: 'SRV-SETUP-DPD',
    123: 'SRV-SETUP-PA',
    124: 'SRV-SETUP-DD',
    125: 'SRV-SETUP-AW',
    126: 'SRV-SETUP-AR',
    127: 'SRV-FORMACION',  # Already has reference
    128: 'SRV-MANT-RGPD',
    129: 'SRV-MANT-LSSI',
    130: 'SRV-MANT-RGPD-LSSI',
    131: 'SRV-MANT-TRIMESTRAL-RGPD-LSSI',  # Already has reference
    132: 'SRV-MANT-AR',  # Already has reference
    133: 'SRV-MANT-CD',
    134: 'SRV-MANT-DPD',
    135: 'SRV-MANT-PA',
    136: 'SRV-MANT-DD',
    137: 'SRV-MANT-AW',
}

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

def update_products(models, uid):
    """Update products with Internal References"""
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    print(f"\n📝 Updating {len(PRODUCT_MAPPING)} products...")
    print("="*80)
    
    for odoo_id, internal_ref in PRODUCT_MAPPING.items():
        try:
            # Get current product data
            product = models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'product.template', 'read',
                [[odoo_id], ['name', 'default_code']]
            )
            
            if not product:
                print(f"⚠️  Product ID {odoo_id} not found")
                error_count += 1
                continue
            
            current_ref = product[0]['default_code']
            name = product[0]['name'][:50]
            
            # Skip if already has the correct reference
            if current_ref == internal_ref:
                print(f"⏭️  ID {odoo_id}: {internal_ref} (already set)")
                skipped_count += 1
                continue
            
            # Update the Internal Reference
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'product.template', 'write',
                [[odoo_id], {'default_code': internal_ref}]
            )
            
            print(f"✅ ID {odoo_id}: {internal_ref:<30} | {name}...")
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Error updating ID {odoo_id}: {e}")
            error_count += 1
    
    print("\n" + "="*80)
    print(f"📊 SUMMARY:")
    print(f"   ✅ Updated: {updated_count}")
    print(f"   ⏭️  Skipped (already set): {skipped_count}")
    print(f"   ❌ Errors: {error_count}")
    print("="*80)

def main():
    print("="*80)
    print("FIX PRODUCT INTERNAL REFERENCES (BY ID)")
    print("="*80)
    
    try:
        models, uid = connect_odoo()
        update_products(models, uid)
        print("\n✅ Process completed!")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
