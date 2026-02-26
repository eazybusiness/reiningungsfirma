#!/usr/bin/env python3
"""
Check for duplicate customers in Odoo
Identifies duplicates by VAT, name, and checks for duplicate pricelists
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

def check_duplicates(models, uid):
    """Check for duplicate customers"""
    
    print("="*80)
    print("CHECKING FOR DUPLICATE CUSTOMERS")
    print("="*80 + "\n")
    
    # Get all partners (customers and non-customers)
    partner_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'res.partner', 'search',
        [[]]
    )
    
    # Get partner details
    partners = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'res.partner', 'read',
        [partner_ids, ['id', 'name', 'vat', 'customer_rank', 'supplier_rank', 
                       'property_product_pricelist', 'active']]
    )
    
    print(f"📊 Total partners in database: {len(partners)}")
    
    # Filter only customers
    customers = [p for p in partners if p['customer_rank'] > 0]
    print(f"👥 Total customers: {len(customers)}\n")
    
    # Check for duplicates by VAT
    vat_groups = defaultdict(list)
    name_groups = defaultdict(list)
    
    for customer in customers:
        if customer['vat']:
            vat_groups[customer['vat']].append(customer)
        name_groups[customer['name']].append(customer)
    
    # Find duplicates by VAT
    duplicate_vats = {vat: custs for vat, custs in vat_groups.items() if len(custs) > 1}
    duplicate_names = {name: custs for name, custs in name_groups.items() if len(custs) > 1}
    
    print("="*80)
    print(f"🔍 DUPLICATE ANALYSIS")
    print("="*80)
    print(f"Customers with duplicate VAT: {len(duplicate_vats)}")
    print(f"Customers with duplicate Name: {len(duplicate_names)}")
    print()
    
    if duplicate_vats:
        print("="*80)
        print("⚠️  DUPLICATE CUSTOMERS BY VAT (Tax ID)")
        print("="*80 + "\n")
        
        for vat, custs in sorted(duplicate_vats.items()):
            print(f"VAT: {vat}")
            print(f"   Found {len(custs)} customers with same VAT:\n")
            
            for cust in custs:
                pricelist_name = cust['property_product_pricelist'][1] if cust['property_product_pricelist'] else '(none)'
                active = "✅ Active" if cust['active'] else "❌ Inactive"
                print(f"   • ID: {cust['id']:4} | {active} | {cust['name'][:50]}")
                print(f"     Pricelist: {pricelist_name}")
            print()
    
    if duplicate_names:
        print("="*80)
        print("⚠️  DUPLICATE CUSTOMERS BY NAME")
        print("="*80 + "\n")
        
        for name, custs in sorted(duplicate_names.items()):
            if len(custs) > 1:
                print(f"Name: {name[:60]}")
                print(f"   Found {len(custs)} customers with same name:\n")
                
                for cust in custs:
                    vat_display = cust['vat'] if cust['vat'] else '(no VAT)'
                    pricelist_name = cust['property_product_pricelist'][1] if cust['property_product_pricelist'] else '(none)'
                    active = "✅" if cust['active'] else "❌"
                    print(f"   • ID: {cust['id']:4} | {active} | VAT: {vat_display}")
                    print(f"     Pricelist: {pricelist_name}")
                print()
    
    # Check for triplicate pricelists
    print("="*80)
    print("🔍 CHECKING FOR DUPLICATE PRICELISTS")
    print("="*80 + "\n")
    
    pricelist_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.pricelist', 'search',
        [[]]
    )
    
    pricelists = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.pricelist', 'read',
        [pricelist_ids, ['id', 'name', 'active']]
    )
    
    pricelist_name_groups = defaultdict(list)
    for pl in pricelists:
        pricelist_name_groups[pl['name']].append(pl)
    
    duplicate_pricelists = {name: pls for name, pls in pricelist_name_groups.items() if len(pls) > 1}
    
    if duplicate_pricelists:
        print(f"⚠️  Found {len(duplicate_pricelists)} pricelists with duplicate names:\n")
        
        for name, pls in sorted(duplicate_pricelists.items()):
            print(f"Pricelist: {name}")
            print(f"   Found {len(pls)} pricelists with same name:\n")
            
            for pl in pls:
                active = "✅ Active" if pl['active'] else "❌ Inactive"
                print(f"   • ID: {pl['id']:4} | {active}")
            print()
    else:
        print("✅ No duplicate pricelists found")
    
    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)
    print(f"Total customers: {len(customers)}")
    print(f"Duplicate VATs: {len(duplicate_vats)}")
    print(f"Duplicate Names: {len(duplicate_names)}")
    print(f"Duplicate Pricelists: {len(duplicate_pricelists)}")
    
    total_duplicate_customers = sum(len(custs) for custs in duplicate_vats.values())
    print(f"\n⚠️  Total customer records that are duplicates: {total_duplicate_customers}")
    print("="*80)

def main():
    try:
        models, uid = connect_odoo()
        check_duplicates(models, uid)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
