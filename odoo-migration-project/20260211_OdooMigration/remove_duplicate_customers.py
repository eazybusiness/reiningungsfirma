#!/usr/bin/env python3
"""
Remove duplicate customers from Odoo
Keeps the OLDER customer (lower ID) and deactivates/deletes the newer duplicate
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

def find_duplicates(models, uid):
    """Find duplicate customers by VAT"""
    
    # Get all customers
    partner_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'res.partner', 'search',
        [[['customer_rank', '>', 0]]]
    )
    
    partners = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'res.partner', 'read',
        [partner_ids, ['id', 'name', 'vat', 'property_product_pricelist']]
    )
    
    # Group by VAT
    vat_groups = defaultdict(list)
    for partner in partners:
        if partner['vat']:
            vat_groups[partner['vat']].append(partner)
    
    # Find duplicates (more than 1 customer with same VAT)
    duplicates = {vat: custs for vat, custs in vat_groups.items() if len(custs) > 1}
    
    return duplicates

def check_related_records(models, uid, partner_id):
    """Check if customer has related records (invoices, sales orders, etc.)"""
    
    # Check for invoices
    invoice_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'account.move', 'search',
        [[['partner_id', '=', partner_id], ['move_type', 'in', ['out_invoice', 'out_refund']]]]
    )
    
    # Check for sales orders
    sale_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'sale.order', 'search',
        [[['partner_id', '=', partner_id]]]
    )
    
    return {
        'invoices': len(invoice_ids),
        'sales': len(sale_ids),
        'has_records': len(invoice_ids) > 0 or len(sale_ids) > 0
    }

def remove_duplicates(models, uid, test_mode=True):
    """Remove duplicate customers"""
    
    print("="*80)
    print("REMOVING DUPLICATE CUSTOMERS")
    print("="*80 + "\n")
    
    duplicates = find_duplicates(models, uid)
    
    if not duplicates:
        print("✅ No duplicates found!")
        return
    
    print(f"Found {len(duplicates)} VATs with duplicate customers\n")
    
    if test_mode:
        print("🧪 TEST MODE - No changes will be made\n")
    else:
        print("🚀 PRODUCTION MODE - Duplicates will be removed\n")
    
    removed_count = 0
    kept_count = 0
    skipped_count = 0
    
    for vat, customers in sorted(duplicates.items()):
        print(f"VAT: {vat}")
        print(f"   Found {len(customers)} customers:\n")
        
        # Sort by ID (keep the oldest one - lowest ID)
        customers_sorted = sorted(customers, key=lambda x: x['id'])
        
        keep_customer = customers_sorted[0]
        remove_customers = customers_sorted[1:]
        
        print(f"   ✅ KEEP:   ID {keep_customer['id']:4} | {keep_customer['name'][:50]}")
        
        for cust in remove_customers:
            # Check for related records
            related = check_related_records(models, uid, cust['id'])
            
            if related['has_records']:
                print(f"   ⚠️  SKIP:   ID {cust['id']:4} | {cust['name'][:50]}")
                print(f"              Has {related['invoices']} invoice(s), {related['sales']} sale(s) - CANNOT DELETE")
                skipped_count += 1
            else:
                print(f"   ❌ REMOVE: ID {cust['id']:4} | {cust['name'][:50]}")
                
                if not test_mode:
                    try:
                        # Try to delete the customer
                        models.execute_kw(
                            ODOO_DB, uid, ODOO_PASSWORD,
                            'res.partner', 'unlink',
                            [[cust['id']]]
                        )
                        print(f"              ✅ Deleted successfully")
                        removed_count += 1
                    except Exception as e:
                        # If delete fails, try to deactivate
                        try:
                            models.execute_kw(
                                ODOO_DB, uid, ODOO_PASSWORD,
                                'res.partner', 'write',
                                [[cust['id']], {'active': False}]
                            )
                            print(f"              ⚠️  Could not delete, deactivated instead")
                            removed_count += 1
                        except Exception as e2:
                            print(f"              ❌ Error: {e2}")
                            skipped_count += 1
                else:
                    removed_count += 1
        
        kept_count += 1
        print()
    
    print("="*80)
    print("📊 SUMMARY")
    print("="*80)
    print(f"Customers kept: {kept_count}")
    print(f"Duplicates removed: {removed_count}")
    print(f"Skipped (has subscriptions): {skipped_count}")
    print("="*80)

def main():
    print("="*80)
    print("DUPLICATE CUSTOMER CLEANUP")
    print("="*80 + "\n")
    
    try:
        models, uid = connect_odoo()
        
        # Test mode first
        print("="*80)
        print("STEP 1: TEST RUN")
        print("="*80 + "\n")
        remove_duplicates(models, uid, test_mode=True)
        
        # Ask for confirmation
        print("\n" + "="*80)
        response = input("Proceed with removing duplicates? (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Cleanup cancelled by user.")
            return 0
        
        # Production run
        print("\n" + "="*80)
        print("STEP 2: REMOVING DUPLICATES")
        print("="*80 + "\n")
        remove_duplicates(models, uid, test_mode=False)
        
        print("\n✅ Cleanup completed!")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
