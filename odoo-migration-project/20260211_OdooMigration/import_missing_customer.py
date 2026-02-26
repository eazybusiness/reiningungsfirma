#!/usr/bin/env python3
"""
Import the missing customer: Beyond the Universe Group, S.L.
"""

import xmlrpc.client
import csv

ODOO_URL = 'https://exartia.odoo.com'
ODOO_DB = 'exartia'
ODOO_USERNAME = 'eduardo.mateo@exartia.net'
ODOO_PASSWORD = 'ExartiaTemporal2026'

print("="*80)
print("IMPORTING MISSING CUSTOMER")
print("="*80 + "\n")

common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

print(f"✅ Connected as user ID: {uid}\n")

# Load CSV
for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
    try:
        with open('customers.csv', 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            customers = list(reader)
            break
    except UnicodeDecodeError:
        continue

# Find Beyond the Universe Group
target_customer = None
for cust in customers:
    if 'beyond the universe' in cust.get('Name', '').lower():
        target_customer = cust
        break

if not target_customer:
    print("❌ Customer not found in CSV")
    exit(1)

print(f"Found customer in CSV:")
print(f"   Name: {target_customer.get('Name')}")
print(f"   VAT: {target_customer.get('VAT')}")
print(f"   Pricelist: {target_customer.get('Price list')}")
print()

# Get pricelist ID
pricelist_name = target_customer.get('Price list', '').strip()
pricelist_id = None

if pricelist_name:
    pricelist_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'product.pricelist', 'search',
        [[['name', '=', pricelist_name]]]
    )
    if pricelist_ids:
        pricelist_id = pricelist_ids[0]
        print(f"✅ Found pricelist: {pricelist_name} (ID: {pricelist_id})")
    else:
        print(f"⚠️  Pricelist not found: {pricelist_name}")

# Get payment term ID
payment_term_name = target_customer.get('Payment terms', '').strip()
payment_term_id = None

if payment_term_name:
    payment_term_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'account.payment.term', 'search',
        [[['name', '=', payment_term_name]]]
    )
    if payment_term_ids:
        payment_term_id = payment_term_ids[0]
        print(f"✅ Found payment term: {payment_term_name} (ID: {payment_term_id})")

# Get country ID (Spain)
country_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'res.country', 'search',
    [[['code', '=', 'ES']]]
)
country_id = country_ids[0] if country_ids else None

print()

# Create customer
customer_data = {
    'name': target_customer.get('Name'),
    'vat': target_customer.get('VAT'),
    'is_company': True,
    'customer_rank': 1,
    'email': target_customer.get('Email', ''),
    'phone': target_customer.get('Phone', ''),
    'street': target_customer.get('Address', ''),
    'country_id': country_id,
}

if pricelist_id:
    customer_data['property_product_pricelist'] = pricelist_id

if payment_term_id:
    customer_data['property_payment_term_id'] = payment_term_id

try:
    partner_id = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'res.partner', 'create',
        [customer_data]
    )
    
    print(f"✅ Customer created with ID: {partner_id}")
    print(f"   Name: {customer_data['name']}")
    print(f"   VAT: {customer_data['vat']}")
    
    # Create bank account if IBAN exists
    iban = target_customer.get('IBAN', '').strip()
    if iban:
        bank_data = {
            'partner_id': partner_id,
            'acc_number': iban,
        }
        
        bank_id = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.partner.bank', 'create',
            [bank_data]
        )
        
        print(f"✅ Bank account created with ID: {bank_id}")
        print(f"   IBAN: {iban}")
    
    print("\n✅ Customer successfully imported!")
    
except Exception as e:
    print(f"\n❌ Error creating customer: {e}")
    import traceback
    traceback.print_exc()
