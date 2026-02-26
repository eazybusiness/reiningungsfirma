#!/usr/bin/env python3
"""
Import Customers from CSV to Odoo Online
Includes: contact info, address, pricelist assignment, bank accounts
"""

import xmlrpc.client
import csv

# Odoo connection settings
ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

# File path
CUSTOMERS_CSV = 'customers.csv'

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

def get_country_id(models, uid, country_name):
    """Get country ID by name"""
    if not country_name:
        return False
    
    country_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'res.country', 'search',
        [[['name', '=', country_name]]]
    )
    
    return country_ids[0] if country_ids else False

def get_pricelist_id(models, uid, pricelist_name):
    """Get pricelist ID by name"""
    if not pricelist_name:
        return False
    
    pricelist_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.pricelist', 'search',
        [[['name', '=', pricelist_name]]]
    )
    
    return pricelist_ids[0] if pricelist_ids else False

def get_payment_term_id(models, uid, payment_term_name):
    """Get payment term ID by name"""
    if not payment_term_name:
        return False
    
    payment_term_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'account.payment.term', 'search',
        [[['name', '=', payment_term_name]]]
    )
    
    return payment_term_ids[0] if payment_term_ids else False

def load_customers_from_csv():
    """Load customers from CSV"""
    customers = []
    
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(CUSTOMERS_CSV, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    customers.append(row)
            print(f"📄 Loaded {len(customers)} customers from CSV (encoding: {encoding})\n")
            return customers
        except UnicodeDecodeError:
            continue
    
    raise Exception("Could not read CSV file with any supported encoding")

def import_customers(models, uid, test_mode=True, limit=5):
    """Import customers"""
    customers = load_customers_from_csv()
    
    if test_mode:
        customers = customers[:limit]
        print(f"🧪 TEST MODE: Importing only {limit} customers\n")
    else:
        print(f"🚀 PRODUCTION MODE: Importing all {len(customers)} customers\n")
    
    imported_count = 0
    error_count = 0
    errors = []
    
    # Cache for lookups
    country_cache = {}
    pricelist_cache = {}
    payment_term_cache = {}
    
    for idx, customer in enumerate(customers, 1):
        try:
            name = customer['Name'].strip()
            vat = customer['VAT'].strip() if customer['VAT'] else False
            
            # Skip if no name
            if not name:
                continue
            
            # Get country ID (cached)
            country_name = customer['Country'].strip() if customer['Country'] else False
            country_id = False
            if country_name:
                if country_name not in country_cache:
                    country_cache[country_name] = get_country_id(models, uid, country_name)
                country_id = country_cache[country_name]
            
            # Get pricelist ID (cached)
            pricelist_name = customer['Price list'].strip() if customer['Price list'] else False
            pricelist_id = False
            if pricelist_name:
                if pricelist_name not in pricelist_cache:
                    pricelist_cache[pricelist_name] = get_pricelist_id(models, uid, pricelist_name)
                pricelist_id = pricelist_cache[pricelist_name]
            
            # Get payment term ID (cached)
            payment_term_name = customer['Payment terms'].strip() if customer['Payment terms'] else False
            payment_term_id = False
            if payment_term_name:
                if payment_term_name not in payment_term_cache:
                    payment_term_cache[payment_term_name] = get_payment_term_id(models, uid, payment_term_name)
                payment_term_id = payment_term_cache[payment_term_name]
            
            # Prepare customer data
            customer_data = {
                'name': name,
                'customer_rank': 1,  # Mark as customer
                'is_company': True,  # Mark as company (not individual)
            }
            
            # Add optional fields
            if vat:
                customer_data['vat'] = vat
            if customer['Email']:
                customer_data['email'] = customer['Email'].strip()
            if customer['Phone']:
                customer_data['phone'] = customer['Phone'].strip()
            # Mobile field not available in Odoo 19 - skip it
            if customer['Website']:
                customer_data['website'] = customer['Website'].strip()
            if customer['Street']:
                customer_data['street'] = customer['Street'].strip()
            if customer['City']:
                customer_data['city'] = customer['City'].strip()
            if customer['Zip']:
                customer_data['zip'] = customer['Zip'].strip()
            if country_id:
                customer_data['country_id'] = country_id
            if customer['Lang']:
                customer_data['lang'] = customer['Lang'].strip()
            if pricelist_id:
                customer_data['property_product_pricelist'] = pricelist_id
            if payment_term_id:
                customer_data['property_payment_term_id'] = payment_term_id
            
            # Create customer
            partner_id = models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'res.partner', 'create',
                [customer_data]
            )
            
            # Add bank account if IBAN provided
            iban = customer['IBAN'].strip() if customer['IBAN'] else False
            if iban and partner_id:
                try:
                    bank_data = {
                        'partner_id': partner_id,
                        'acc_number': iban,
                    }
                    
                    models.execute_kw(
                        ODOO_DB, uid, ODOO_PASSWORD,
                        'res.partner.bank', 'create',
                        [bank_data]
                    )
                except Exception as e:
                    # Bank account creation failed, but customer created
                    pass
            
            pricelist_info = f" | PL: {pricelist_name}" if pricelist_name else ""
            print(f"✅ [{idx}/{len(customers)}] {name[:50]}{pricelist_info}")
            imported_count += 1
            
        except Exception as e:
            error_msg = f"Error importing {customer.get('Name', 'Unknown')}: {e}"
            print(f"❌ [{idx}/{len(customers)}] {error_msg}")
            errors.append(error_msg)
            error_count += 1
    
    print("\n" + "="*80)
    print(f"📊 IMPORT SUMMARY:")
    print(f"   ✅ Imported: {imported_count}")
    print(f"   ❌ Errors: {error_count}")
    print("="*80)
    
    if errors and len(errors) <= 10:
        print("\n⚠️  ERRORS:")
        for error in errors[:10]:
            print(f"   - {error}")
    
    return imported_count, error_count

def main():
    print("="*80)
    print("IMPORT CUSTOMERS TO ODOO ONLINE")
    print("="*80 + "\n")
    
    try:
        models, uid = connect_odoo()
        
        # Test mode first
        print("="*80)
        print("STEP 1: TEST IMPORT (5 customers)")
        print("="*80 + "\n")
        imported, errors = import_customers(models, uid, test_mode=True, limit=5)
        
        if errors > 0:
            print("\n⚠️  Errors found in test import. Please review before continuing.")
            response = input("Continue anyway? (yes/no): ").strip().lower()
            if response != 'yes':
                print("❌ Import cancelled by user.")
                return 0
        
        # Ask for confirmation
        print("\n" + "="*80)
        response = input("Test successful! Import all customers? (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Import cancelled by user.")
            return 0
        
        # Production import
        print("\n" + "="*80)
        print("STEP 2: FULL IMPORT (all customers)")
        print("="*80 + "\n")
        imported, errors = import_customers(models, uid, test_mode=False)
        
        print("\n✅ Import completed!")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
