#!/usr/bin/env python3
"""
Convert pricelist rules CSV to Odoo-compatible import format
"""
import csv
from datetime import datetime

def convert_date(date_str):
    """Convert MM/DD/YYYY to YYYY-MM-DD"""
    if not date_str or date_str.strip() == '':
        return ''
    try:
        dt = datetime.strptime(date_str.strip(), '%m/%d/%Y')
        return dt.strftime('%Y-%m-%d')
    except:
        return ''

def normalize_id(text):
    """Convert text to lowercase external ID format"""
    return text.lower().replace('-', '_').replace(' ', '_')

# File paths
input_file = 'pricelist_rules.csv'
output_file = 'pricelist_items_import.csv'

print("=" * 60)
print("PRICELIST RULES CSV CONVERTER")
print("=" * 60)

with open(input_file, 'r', encoding='utf-8') as f_in:
    reader = csv.DictReader(f_in)
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
        fieldnames = [
            'pricelist_id/id',
            'product_tmpl_id/id', 
            'applied_on',
            'compute_price',
            'fixed_price',
            'min_quantity',
            'date_start',
            'date_end'
        ]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        
        count = 0
        for row in reader:
            pricelist_name = row['Price list'].strip()
            product_id = row['Product ID'].strip()
            price = row['Price'].strip()
            start_date = convert_date(row['Start date'])
            end_date = convert_date(row['End date'])
            
            # Create external IDs
            pricelist_ext_id = f"__import__.pricelist_{normalize_id(pricelist_name)}"
            product_ext_id = f"__import__.product_{normalize_id(product_id)}"
            
            writer.writerow({
                'pricelist_id/id': pricelist_ext_id,
                'product_tmpl_id/id': product_ext_id,
                'applied_on': '3_product',
                'compute_price': 'fixed',
                'fixed_price': price,
                'min_quantity': '1',
                'date_start': start_date,
                'date_end': end_date
            })
            count += 1

print(f"✅ Converted {count} pricelist rules")
print(f"📄 Output file: {output_file}")
print("\nNext steps:")
print("1. Enable Developer Mode in Odoo")
print("2. Go to Settings → Technical → Database Structure → Models")
print("3. Search 'product.pricelist.item' → Click 'Records'")
print("4. Click Favorites → Import records")
print("5. Upload pricelist_items_import.csv")
print("6. Enable 'Use External IDs' checkbox")
print("7. Click 'Test' then 'Import'")
