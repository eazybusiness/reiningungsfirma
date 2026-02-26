#!/usr/bin/env python3
"""
Comprehensive validation script to verify customer import completeness
Compares customers.csv with Odoo database to find missing or extra records
"""

import xmlrpc.client
import csv
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

def load_csv_customers():
    """Load customers from CSV file"""
    
    csv_file = 'customers.csv'
    
    print(f"Loading customers from {csv_file}...")
    
    # Try different encodings
    for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
        try:
            with open(csv_file, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                customers = list(reader)
                print(f"✅ Loaded {len(customers)} customers from CSV (encoding: {encoding})\n")
                return customers
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"❌ File not found: {csv_file}")
            return []
    
    print(f"❌ Could not read CSV file with any encoding")
    return []

def get_odoo_customers(models, uid):
    """Get all customers from Odoo"""
    
    print("Loading customers from Odoo...")
    
    # Get all partners with customer_rank > 0
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
    
    print(f"✅ Loaded {len(partners)} customers from Odoo\n")
    
    return partners

def normalize_name(name):
    """Normalize customer name for comparison"""
    if not name:
        return ""
    # Remove extra spaces, convert to lowercase, remove special chars
    return ' '.join(name.lower().strip().split())

def normalize_vat(vat):
    """Normalize VAT for comparison"""
    if not vat:
        return ""
    # Remove spaces and convert to uppercase
    return vat.replace(' ', '').upper().strip()

def main():
    try:
        models, uid = connect_odoo()
        
        # Load data
        csv_customers = load_csv_customers()
        odoo_customers = get_odoo_customers(models, uid)
        
        if not csv_customers:
            print("❌ No CSV data to compare")
            return 1
        
        print("="*80)
        print("VALIDATION ANALYSIS")
        print("="*80 + "\n")
        
        # Create lookup dictionaries
        csv_by_vat = {}
        csv_by_name = {}
        
        for cust in csv_customers:
            vat = normalize_vat(cust.get('VAT', ''))
            name = normalize_name(cust.get('Name', ''))
            
            if vat:
                csv_by_vat[vat] = cust
            if name:
                csv_by_name[name] = cust
        
        odoo_by_vat = {}
        odoo_by_name = {}
        
        for cust in odoo_customers:
            vat = normalize_vat(cust.get('vat', ''))
            name = normalize_name(cust.get('name', ''))
            
            if vat:
                odoo_by_vat[vat] = cust
            if name:
                odoo_by_name[name] = cust
        
        # Find missing customers (in CSV but not in Odoo)
        missing_customers = []
        
        for cust in csv_customers:
            vat = normalize_vat(cust.get('VAT', ''))
            name = normalize_name(cust.get('Name', ''))
            
            found = False
            
            # Try to find by VAT first
            if vat and vat in odoo_by_vat:
                found = True
            # Try to find by name
            elif name and name in odoo_by_name:
                found = True
            
            if not found:
                missing_customers.append(cust)
        
        # Find extra customers (in Odoo but not in CSV)
        extra_customers = []
        
        for cust in odoo_customers:
            vat = normalize_vat(cust.get('vat', ''))
            name = normalize_name(cust.get('name', ''))
            
            found = False
            
            # Try to find by VAT first
            if vat and vat in csv_by_vat:
                found = True
            # Try to find by name
            elif name and name in csv_by_name:
                found = True
            
            if not found:
                extra_customers.append(cust)
        
        # Report results
        print(f"📊 CSV customers: {len(csv_customers)}")
        print(f"📊 Odoo customers: {len(odoo_customers)}")
        print(f"📊 Missing from Odoo: {len(missing_customers)}")
        print(f"📊 Extra in Odoo: {len(extra_customers)}\n")
        
        if missing_customers:
            print("="*80)
            print("❌ MISSING CUSTOMERS (in CSV but NOT in Odoo)")
            print("="*80 + "\n")
            
            for cust in missing_customers:
                name = cust.get('Name', 'N/A')
                vat = cust.get('VAT', 'N/A')
                pricelist = cust.get('Price list', 'N/A')
                print(f"   • {name:50} | VAT: {vat:15} | Pricelist: {pricelist}")
            
            print()
        
        if extra_customers:
            print("="*80)
            print("⚠️  EXTRA CUSTOMERS (in Odoo but NOT in CSV)")
            print("="*80 + "\n")
            
            for cust in extra_customers:
                name = cust.get('name', 'N/A')
                vat = cust.get('vat', 'N/A')
                pricelist = cust.get('property_product_pricelist', [False, 'N/A'])[1]
                print(f"   • ID {cust['id']:4} | {name:50} | VAT: {vat:15} | Pricelist: {pricelist}")
            
            print()
        
        # Check specific customer mentioned by friend
        print("="*80)
        print("CHECKING SPECIFIC CUSTOMER: Beyond the Universe Group, S.L.")
        print("="*80 + "\n")
        
        # Search in CSV
        found_in_csv = False
        for cust in csv_customers:
            if 'beyond the universe' in cust.get('Name', '').lower():
                found_in_csv = True
                print(f"✅ Found in CSV:")
                print(f"   Name: {cust.get('Name')}")
                print(f"   VAT: {cust.get('VAT')}")
                print(f"   Pricelist: {cust.get('Price list')}")
                print()
                break
        
        if not found_in_csv:
            print("❌ NOT found in CSV\n")
        
        # Search in Odoo
        found_in_odoo = False
        for cust in odoo_customers:
            if 'beyond the universe' in cust.get('name', '').lower():
                found_in_odoo = True
                print(f"✅ Found in Odoo:")
                print(f"   ID: {cust['id']}")
                print(f"   Name: {cust.get('name')}")
                print(f"   VAT: {cust.get('vat')}")
                print(f"   Pricelist: {cust.get('property_product_pricelist', [False, 'N/A'])[1]}")
                print()
                break
        
        if not found_in_odoo:
            print("❌ NOT found in Odoo\n")
        
        # Summary
        print("="*80)
        print("SUMMARY")
        print("="*80 + "\n")
        
        if len(missing_customers) == 0 and len(extra_customers) == 0:
            print("✅ PERFECT MATCH!")
            print("   All customers from CSV are in Odoo")
            print("   No extra customers in Odoo")
        else:
            print("⚠️  DISCREPANCIES FOUND:")
            if missing_customers:
                print(f"   {len(missing_customers)} customer(s) from CSV are MISSING in Odoo")
            if extra_customers:
                print(f"   {len(extra_customers)} customer(s) in Odoo are NOT in CSV")
        
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit(main())
