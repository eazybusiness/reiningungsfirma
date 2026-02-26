#!/usr/bin/env python3
"""
Import pricelist rules to Odoo Online via XML-RPC API
"""
import xmlrpc.client
import csv
from datetime import datetime

# ============================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================
ODOO_URL = 'https://yourinstance.odoo.com'  # Your Odoo Online URL
ODOO_DB = 'yourdb'  # Your database name
ODOO_USERNAME = 'your@email.com'  # Your login email
ODOO_API_KEY = 'your_api_key_here'  # Generate in Settings → Users → API Keys

CSV_FILE = 'pricelist_rules.csv'

# ============================================
# HELPER FUNCTIONS
# ============================================

def convert_date(date_str):
    """Convert MM/DD/YYYY to YYYY-MM-DD"""
    if not date_str or date_str.strip() == '':
        return False
    try:
        dt = datetime.strptime(date_str.strip(), '%m/%d/%Y')
        return dt.strftime('%Y-%m-%d')
    except:
        return False

def connect_odoo():
    """Connect to Odoo and return models proxy"""
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_API_KEY, {})
    
    if not uid:
        raise Exception("Authentication failed! Check credentials.")
    
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    print(f"✅ Connected to Odoo as user ID: {uid}")
    return uid, models

def get_pricelist_id(models, uid, pricelist_name):
    """Get pricelist database ID by name"""
    pricelist_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_API_KEY,
        'product.pricelist', 'search',
        [[['name', '=', pricelist_name]]],
        {'limit': 1}
    )
    
    if not pricelist_ids:
        print(f"⚠️  Pricelist not found: {pricelist_name}")
        return None
    
    return pricelist_ids[0]

def get_product_id_by_code(models, uid, product_code):
    """Get product template ID by Internal Reference (default_code)"""
    product_ids = models.execute_kw(
        ODOO_DB, uid, ODOO_API_KEY,
        'product.template', 'search',
        [[['default_code', '=', product_code]]],
        {'limit': 1}
    )
    
    if not product_ids:
        print(f"⚠️  Product not found: {product_code}")
        return None
    
    return product_ids[0]

def create_pricelist_item(models, uid, pricelist_id, product_id, price, date_start, date_end):
    """Create a pricelist item"""
    values = {
        'pricelist_id': pricelist_id,
        'product_tmpl_id': product_id,
        'applied_on': '3_product',
        'compute_price': 'fixed',
        'fixed_price': float(price),
        'min_quantity': 1,
    }
    
    if date_start:
        values['date_start'] = date_start
    if date_end:
        values['date_end'] = date_end
    
    try:
        item_id = models.execute_kw(
            ODOO_DB, uid, ODOO_API_KEY,
            'product.pricelist.item', 'create',
            [values]
        )
        return item_id
    except Exception as e:
        print(f"❌ Error creating item: {e}")
        return None

# ============================================
# MAIN IMPORT LOGIC
# ============================================

def main():
    print("=" * 60)
    print("ODOO PRICELIST RULES IMPORT")
    print("=" * 60)
    
    # Connect to Odoo
    try:
        uid, models = connect_odoo()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nPlease update the configuration at the top of this script:")
        print("- ODOO_URL")
        print("- ODOO_DB")
        print("- ODOO_USERNAME")
        print("- ODOO_API_KEY")
        return
    
    # Read CSV
    print(f"\n📂 Reading CSV: {CSV_FILE}")
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"❌ File not found: {CSV_FILE}")
        return
    
    print(f"📊 Found {len(rows)} pricelist rules to import\n")
    
    # Import statistics
    success_count = 0
    error_count = 0
    errors = []
    
    # Process each row
    for i, row in enumerate(rows, 1):
        pricelist_name = row['Price list'].strip()
        product_code = row['Product ID'].strip()
        price = row['Price'].strip()
        date_start = convert_date(row['Start date'])
        date_end = convert_date(row['End date'])
        
        print(f"[{i}/{len(rows)}] Processing: {pricelist_name} → {product_code} @ {price}€")
        
        # Get pricelist ID
        pricelist_id = get_pricelist_id(models, uid, pricelist_name)
        if not pricelist_id:
            error_count += 1
            errors.append(f"Row {i}: Pricelist '{pricelist_name}' not found")
            continue
        
        # Get product ID
        product_id = get_product_id_by_code(models, uid, product_code)
        if not product_id:
            error_count += 1
            errors.append(f"Row {i}: Product '{product_code}' not found")
            continue
        
        # Create pricelist item
        item_id = create_pricelist_item(
            models, uid, 
            pricelist_id, product_id, 
            price, date_start, date_end
        )
        
        if item_id:
            print(f"  ✅ Created pricelist item ID: {item_id}")
            success_count += 1
        else:
            error_count += 1
            errors.append(f"Row {i}: Failed to create item")
    
    # Summary
    print("\n" + "=" * 60)
    print("IMPORT SUMMARY")
    print("=" * 60)
    print(f"✅ Successfully imported: {success_count}")
    print(f"❌ Errors: {error_count}")
    
    if errors:
        print("\n⚠️  ERRORS:")
        for error in errors:
            print(f"  - {error}")
    
    print("\n✅ Import complete!")

if __name__ == '__main__':
    main()
