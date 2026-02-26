#!/usr/bin/env python3
"""
Check what data is missing in products and customers in Odoo
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
    
    print(f"✅ Connected as user ID: {uid}\n")
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return models, uid

def check_products(models, uid):
    """Check products for missing data"""
    print("="*80)
    print("CHECKING PRODUCTS")
    print("="*80)
    
    # Get all products
    product_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.template', 'search',
        [[]]
    )
    
    # Get product details with all important fields
    products = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.template', 'read',
        [product_ids, ['name', 'default_code', 'list_price', 'type', 'categ_id', 'taxes_id']]
    )
    
    print(f"\n📦 Total products: {len(products)}\n")
    
    missing_internal_ref = []
    missing_category = []
    missing_taxes = []
    
    for product in products:
        issues = []
        
        if not product['default_code']:
            missing_internal_ref.append(product['name'][:50])
            issues.append("NO INTERNAL REF")
        
        if not product['categ_id']:
            missing_category.append(product['name'][:50])
            issues.append("NO CATEGORY")
        
        if not product['taxes_id']:
            missing_taxes.append(product['name'][:50])
            issues.append("NO TAXES")
        
        if issues:
            print(f"⚠️  {product['name'][:60]}")
            print(f"   Issues: {', '.join(issues)}")
            print(f"   Internal Ref: {product['default_code'] or '(EMPTY)'}")
            print()
    
    print("\n" + "="*80)
    print("PRODUCT SUMMARY:")
    print(f"  ⚠️  Missing Internal Reference: {len(missing_internal_ref)}")
    print(f"  ⚠️  Missing Category: {len(missing_category)}")
    print(f"  ⚠️  Missing Taxes: {len(missing_taxes)}")
    print("="*80)

def check_customers(models, uid):
    """Check customers for missing data"""
    print("\n" + "="*80)
    print("CHECKING CUSTOMERS")
    print("="*80)
    
    # Get all customers (partners that are customers)
    customer_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'res.partner', 'search',
        [[['customer_rank', '>', 0]]]
    )
    
    # Get customer details with all important fields
    customers = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'res.partner', 'read',
        [customer_ids, ['name', 'ref', 'email', 'phone', 'street', 'city', 'zip', 
                        'country_id', 'vat', 'property_payment_term_id', 
                        'property_product_pricelist', 'bank_ids']]
    )
    
    print(f"\n👥 Total customers: {len(customers)}\n")
    
    missing_ref = []
    missing_email = []
    missing_address = []
    missing_country = []
    missing_vat = []
    missing_payment_term = []
    missing_pricelist = []
    missing_bank = []
    
    for customer in customers:
        issues = []
        
        if not customer['ref']:
            missing_ref.append(customer['name'])
            issues.append("NO CUSTOMER REF")
        
        if not customer['email']:
            missing_email.append(customer['name'])
            issues.append("NO EMAIL")
        
        if not customer['street'] or not customer['city']:
            missing_address.append(customer['name'])
            issues.append("INCOMPLETE ADDRESS")
        
        if not customer['country_id']:
            missing_country.append(customer['name'])
            issues.append("NO COUNTRY")
        
        if not customer['vat']:
            missing_vat.append(customer['name'])
            issues.append("NO VAT/TAX ID")
        
        if not customer['property_payment_term_id']:
            missing_payment_term.append(customer['name'])
            issues.append("NO PAYMENT TERM")
        
        if not customer['property_product_pricelist']:
            missing_pricelist.append(customer['name'])
            issues.append("NO PRICELIST")
        
        if not customer['bank_ids']:
            missing_bank.append(customer['name'])
            issues.append("NO BANK ACCOUNT")
        
        if issues:
            print(f"⚠️  {customer['name'][:60]}")
            print(f"   Issues: {', '.join(issues)}")
            if not customer['ref']:
                print(f"   Customer Ref: (EMPTY)")
            if not customer['property_product_pricelist']:
                print(f"   Pricelist: (EMPTY)")
            print()
    
    print("\n" + "="*80)
    print("CUSTOMER SUMMARY:")
    print(f"  ⚠️  Missing Customer Reference: {len(missing_ref)}")
    print(f"  ⚠️  Missing Email: {len(missing_email)}")
    print(f"  ⚠️  Missing/Incomplete Address: {len(missing_address)}")
    print(f"  ⚠️  Missing Country: {len(missing_country)}")
    print(f"  ⚠️  Missing VAT/Tax ID: {len(missing_vat)}")
    print(f"  ⚠️  Missing Payment Term: {len(missing_payment_term)}")
    print(f"  ⚠️  Missing Pricelist: {len(missing_pricelist)}")
    print(f"  ⚠️  Missing Bank Account: {len(missing_bank)}")
    print("="*80)

def main():
    try:
        models, uid = connect_odoo()
        check_products(models, uid)
        check_customers(models, uid)
        
        print("\n" + "="*80)
        print("💡 RECOMMENDATION:")
        print("="*80)
        print("Based on the issues found above, you may need to:")
        print("1. Update products with missing Internal References")
        print("2. Update customers with missing Customer References")
        print("3. Assign pricelists to customers")
        print("4. Add bank accounts (IBAN) to customers")
        print("5. Normalize country and payment terms")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
