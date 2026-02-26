#!/usr/bin/env python3
"""
Investigate duplicate customer issue reported by friend
Check for ALL partners (including archived/inactive) with same VAT
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

print("="*80)
print("INVESTIGATING DUPLICATE CUSTOMER ISSUE")
print("="*80 + "\n")

models, uid = connect_odoo()

# Search for ALL partners (including archived/inactive)
# The key is to NOT filter by customer_rank and to include archived records
print("Searching for ALL partners (including archived/inactive)...\n")

partner_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'res.partner', 'search',
    [[]],  # No filters - get ALL partners
    {'context': {'active_test': False}}  # Include archived records
)

print(f"📊 Total partners found (including archived): {len(partner_ids)}\n")

# Get partner details
partners = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'res.partner', 'read',
    [partner_ids, ['id', 'name', 'vat', 'active', 'customer_rank', 'supplier_rank']],
    {'context': {'active_test': False}}
)

# Group by VAT
vat_groups = defaultdict(list)
for partner in partners:
    if partner['vat']:
        vat_groups[partner['vat']].append(partner)

# Find duplicates
duplicates = {vat: partners_list for vat, partners_list in vat_groups.items() if len(partners_list) > 1}

print("="*80)
print(f"DUPLICATE VAT ANALYSIS")
print("="*80 + "\n")

if duplicates:
    print(f"⚠️  Found {len(duplicates)} VATs with duplicate records\n")
    
    for vat, partners_list in sorted(duplicates.items()):
        print(f"VAT: {vat}")
        print(f"   Found {len(partners_list)} records:\n")
        
        for p in sorted(partners_list, key=lambda x: x['id']):
            active_status = "✅ Active" if p['active'] else "❌ Archived"
            customer_status = f"Customer(rank={p['customer_rank']})" if p['customer_rank'] > 0 else ""
            supplier_status = f"Supplier(rank={p['supplier_rank']})" if p['supplier_rank'] > 0 else ""
            
            print(f"   • ID {p['id']:4} | {active_status:12} | {p['name'][:50]:50} | {customer_status} {supplier_status}")
        
        print()
else:
    print("✅ No duplicate VATs found!")

# Check specific case mentioned by friend: COMERGROUP
print("="*80)
print("CHECKING SPECIFIC CASE: COMERGROUP")
print("="*80 + "\n")

comergroup_ids = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'res.partner', 'search',
    [[['name', 'ilike', 'COMERGROUP']]],
    {'context': {'active_test': False}}
)

if comergroup_ids:
    comergroup = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'res.partner', 'read',
        [comergroup_ids, ['id', 'name', 'vat', 'active', 'customer_rank', 'parent_id', 'is_company']],
        {'context': {'active_test': False}}
    )
    
    print(f"Found {len(comergroup)} COMERGROUP records:\n")
    
    for c in comergroup:
        active_status = "✅ Active" if c['active'] else "❌ Archived"
        parent = c['parent_id'][1] if c['parent_id'] else "No parent"
        company_type = "Company" if c.get('is_company', False) else "Contact"
        
        print(f"ID {c['id']:4} | {active_status:12} | {c['name']:40} | VAT: {c['vat']} | {company_type} | Parent: {parent}")
    
    print()
else:
    print("No COMERGROUP records found\n")

# Check IDs mentioned in URL: 531 and 428
print("="*80)
print("CHECKING IDs FROM URL: 531 and 428")
print("="*80 + "\n")

for check_id in [531, 428]:
    try:
        partner = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'res.partner', 'read',
            [[check_id], ['id', 'name', 'vat', 'active', 'customer_rank', 'parent_id', 'is_company', 'type']],
            {'context': {'active_test': False}}
        )
        
        if partner:
            p = partner[0]
            active_status = "✅ Active" if p['active'] else "❌ Archived"
            parent = p['parent_id'][1] if p['parent_id'] else "No parent"
            company_type = "Company" if p.get('is_company', False) else "Contact"
            record_type = p.get('type', 'contact')
            
            print(f"ID {p['id']:4} | {active_status:12} | {p['name']:40}")
            print(f"       VAT: {p['vat']} | Type: {record_type} | {company_type}")
            print(f"       Parent: {parent} | Customer rank: {p['customer_rank']}")
            print()
    except Exception as e:
        print(f"ID {check_id}: Not found or error - {e}\n")

# Summary
print("="*80)
print("SUMMARY")
print("="*80 + "\n")

print(f"Total partners (all): {len(partners)}")
print(f"Active partners: {sum(1 for p in partners if p['active'])}")
print(f"Archived partners: {sum(1 for p in partners if not p['active'])}")
print(f"Customers (rank > 0): {sum(1 for p in partners if p['customer_rank'] > 0)}")
print(f"Duplicate VATs: {len(duplicates)}")
print()

if duplicates:
    print("⚠️  ACTION REQUIRED:")
    print("   Duplicate VAT records found (including archived)")
    print("   These may be:")
    print("   1. Archived records from previous cleanup")
    print("   2. Contact records (child) vs Company records (parent)")
    print("   3. Different record types (invoice address, delivery address, etc.)")
    print()
    print("   Solution: Delete or permanently remove archived duplicates")
