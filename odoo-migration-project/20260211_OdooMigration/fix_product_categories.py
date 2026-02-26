#!/usr/bin/env python3
"""
Fix Product Categories and Taxes
Assigns "Services" category and 21% IVA tax to products missing them
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
    
    print(f"✅ Connected as user ID: {uid}\n")
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return models, uid

def get_or_create_services_category(models, uid):
    """Get Services category ID, create if doesn't exist"""
    
    # Search for Services category
    category_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.category', 'search',
        [[['name', '=', 'Services']]]
    )
    
    if category_ids:
        print(f"✅ Found 'Services' category (ID: {category_ids[0]})")
        return category_ids[0]
    
    # Create Services category if not found
    category_id = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.category', 'create',
        [{'name': 'Services'}]
    )
    
    print(f"✅ Created 'Services' category (ID: {category_id})")
    return category_id

def get_tax_21_percent(models, uid):
    """Get 21% IVA tax ID"""
    
    # Search for 21% tax
    tax_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'account.tax', 'search',
        [[['amount', '=', 21], ['type_tax_use', '=', 'sale']]]
    )
    
    if tax_ids:
        print(f"✅ Found 21% IVA tax (ID: {tax_ids[0]})")
        return tax_ids[0]
    
    print("⚠️  21% IVA tax not found - products will be updated without tax")
    return None

def fix_products(models, uid):
    """Fix product categories and taxes"""
    
    print("="*80)
    print("FIXING PRODUCT CATEGORIES AND TAXES")
    print("="*80 + "\n")
    
    # Get Services category
    services_category_id = get_or_create_services_category(models, uid)
    
    # Get 21% tax
    tax_21_id = get_tax_21_percent(models, uid)
    
    print()
    
    # Get all products
    product_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.template', 'search',
        [[]]
    )
    
    # Get product details
    products = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.template', 'read',
        [product_ids, ['name', 'default_code', 'categ_id', 'taxes_id']]
    )
    
    updated_category = 0
    updated_taxes = 0
    skipped = 0
    
    for product in products:
        updates = {}
        actions = []
        
        # Check if category is missing
        if not product['categ_id']:
            updates['categ_id'] = services_category_id
            actions.append("SET CATEGORY")
        
        # Check if taxes are missing (only for service products)
        if not product['taxes_id'] and tax_21_id and product['default_code'] and product['default_code'].startswith('SRV'):
            updates['taxes_id'] = [(6, 0, [tax_21_id])]  # Replace taxes with 21% IVA
            actions.append("SET TAX 21%")
        
        if updates:
            # Update product
            models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'product.template', 'write',
                [[product['id']], updates]
            )
            
            if 'categ_id' in updates:
                updated_category += 1
            if 'taxes_id' in updates:
                updated_taxes += 1
            
            ref = product['default_code'] or '(no ref)'
            print(f"✅ {ref:30} | {' + '.join(actions)}")
        else:
            skipped += 1
    
    print("\n" + "="*80)
    print("SUMMARY:")
    print(f"  ✅ Updated category: {updated_category}")
    print(f"  ✅ Updated taxes: {updated_taxes}")
    print(f"  ⏭️  Skipped (already OK): {skipped}")
    print("="*80)

def main():
    try:
        models, uid = connect_odoo()
        fix_products(models, uid)
        print("\n✅ Process completed!")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
