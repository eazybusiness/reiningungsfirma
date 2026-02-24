# Pricelist Rules Import Solution

## 🔍 PROBLEM IDENTIFIED

After analyzing your data files, I've identified the exact issue:

### Current Data Structure
**`pricelist_rules.csv`**:
```csv
Price list,Product ID,Price,Start date,End date
LP_ACORDIA,SRV-MANT-RGPD-LSSI,41.90,12/10/2024,
LP_AIRMATIC,SRV-MANT-CD,105.42,11/29/2023,
```

**`products.csv`**:
```csv
Product ID,Name,Type of product,...
SRV-SETUP-RGPD,"Inicio proyecto...",service,...
SRV-MANT-RGPD,"Cuota mensual...",service,...
```

**`pricelists.csv`**:
```csv
Price list name
LP_ACORDIA
LP_AIRMATIC
```

### The Issue
Your CSV has **human-readable references** (pricelist names, product IDs), but Odoo's import requires **database IDs or External IDs** to link records.

**What's happening**:
- Pricelist rules reference: `LP_ACORDIA` (name)
- Odoo needs: Database ID (e.g., `123`) or External ID (e.g., `__import__.pricelist_lp_acordia`)
- Same for products: `SRV-MANT-RGPD-LSSI` (Product ID) needs to map to database/external ID

---

## ✅ SOLUTION: 3 Methods (Choose Best for Your Situation)

### Method 1: CSV Import with External IDs (Recommended)
**Best for**: Clean, repeatable imports

### Method 2: API Script (Most Reliable)
**Best for**: Complex data, guaranteed success

### Method 3: Manual Mapping CSV (Quick Fix)
**Best for**: Small datasets, one-time import

---

## 📝 METHOD 1: CSV Import with External IDs

### Step 1: Create Corrected CSV with Odoo Field Names

**File**: `pricelist_items_import.csv`

```csv
pricelist_id/id,product_tmpl_id/id,applied_on,compute_price,fixed_price,min_quantity,date_start,date_end
__import__.pricelist_lp_acordia,__import__.product_srv_mant_rgpd_lssi,3_product,fixed,41.90,1,2024-12-10,
__import__.pricelist_lp_airmatic,__import__.product_srv_mant_cd,3_product,fixed,105.42,1,2023-11-29,
__import__.pricelist_lp_airmatic,__import__.product_srv_mant_dpd,3_product,fixed,42.14,1,2023-11-29,
```

**Field Explanations**:
- `pricelist_id/id`: External ID of pricelist (format: `__import__.pricelist_<name_lowercase>`)
- `product_tmpl_id/id`: External ID of product template (format: `__import__.product_<product_id_lowercase>`)
- `applied_on`: `3_product` (applies to specific product variant)
- `compute_price`: `fixed` (fixed price, not percentage/formula)
- `fixed_price`: The actual price for this customer
- `min_quantity`: `1` (applies from quantity 1)
- `date_start`: Start date in `YYYY-MM-DD` format
- `date_end`: End date (leave empty if no end date)

### Step 2: Generate Full Import CSV

I'll create a Python script to convert your current CSV to the correct format:

**Script**: `convert_pricelist_rules.py`

```python
#!/usr/bin/env python3
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

# Read source file
input_file = '/home/nop/Downloads/20260211_OdooMigration/pricelist_rules.csv'
output_file = '/home/nop/Downloads/20260211_OdooMigration/pricelist_items_import.csv'

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

print(f"✅ Converted {output_file}")
print("Next: Import this file via Odoo Developer Mode → Technical → Pricelist Items → Import")
```

### Step 3: Run Conversion Script

```bash
cd /home/nop/Downloads/20260211_OdooMigration/
python3 convert_pricelist_rules.py
```

### Step 4: Import via Odoo Developer Mode

1. **Enable Developer Mode**:
   - Odoo Online → Settings (gear icon) → Activate Developer Mode

2. **Navigate to Pricelist Items**:
   - Settings → Technical → Database Structure → Models
   - Search: "product.pricelist.item"
   - Click "Records" button
   - OR: Direct URL: `https://yourinstance.odoo.com/web#model=product.pricelist.item`

3. **Import CSV**:
   - Click "Favorites" (⭐) → Import records
   - Upload: `pricelist_items_import.csv`
   - **IMPORTANT**: Check "Use External IDs"
   - Map fields (should auto-map if column names match)
   - Click "Test" → Verify no errors
   - Click "Import" → Confirm

4. **Validate**:
   - Go to Sales → Configuration → Pricelists
   - Open a pricelist (e.g., LP_ACORDIA)
   - Check "Price Rules" tab
   - Should see imported rules with correct products and prices

---

## 🐍 METHOD 2: API Script (Most Reliable)

This method uses Odoo's XML-RPC API to import pricelist rules programmatically.

**Advantages**:
- No CSV field mapping issues
- Better error handling
- Can validate data before import
- Works even if CSV import fails

### Full Import Script

**File**: `import_pricelist_rules.py`

```python
#!/usr/bin/env python3
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

CSV_FILE = '/home/nop/Downloads/20260211_OdooMigration/pricelist_rules.csv'

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
        'applied_on': '3_product',  # Apply to product variant
        'compute_price': 'fixed',
        'fixed_price': float(price),
        'min_quantity': 1,
    }
    
    # Add dates if provided
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
    uid, models = connect_odoo()
    
    # Read CSV
    print(f"\n📂 Reading CSV: {CSV_FILE}")
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
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
```

### How to Use API Script

1. **Install Python XML-RPC** (if not already installed):
```bash
# Usually pre-installed with Python
python3 -c "import xmlrpc.client" && echo "✅ xmlrpc.client available"
```

2. **Get Odoo API Key**:
   - Odoo Online → Settings → Users & Companies → Users
   - Click your user → Preferences tab
   - API Keys section → New API Key
   - Copy the key

3. **Update Script Configuration**:
   - Edit `import_pricelist_rules.py`
   - Set `ODOO_URL`, `ODOO_DB`, `ODOO_USERNAME`, `ODOO_API_KEY`

4. **Run Script**:
```bash
cd /home/nop/Downloads/20260211_OdooMigration/
python3 import_pricelist_rules.py
```

5. **Validate Results**:
   - Check script output for success/error count
   - Verify in Odoo: Sales → Pricelists → Price Rules

---

## ⚡ METHOD 3: Quick Manual Mapping (For Testing)

If you want to test with just a few rules first:

### Step 1: Get Database IDs

**Get Pricelist IDs**:
```python
# In Odoo developer console or via API
pricelists = models.execute_kw(db, uid, password,
    'product.pricelist', 'search_read',
    [[['name', 'in', ['LP_ACORDIA', 'LP_AIRMATIC']]]],
    {'fields': ['id', 'name']})
# Returns: [{'id': 123, 'name': 'LP_ACORDIA'}, ...]
```

**Get Product IDs**:
```python
products = models.execute_kw(db, uid, password,
    'product.template', 'search_read',
    [[['default_code', 'in', ['SRV-MANT-RGPD-LSSI', 'SRV-MANT-CD']]]],
    {'fields': ['id', 'default_code', 'name']})
```

### Step 2: Create CSV with Database IDs

```csv
pricelist_id/.id,product_tmpl_id/.id,applied_on,compute_price,fixed_price,min_quantity
123,456,3_product,fixed,41.90,1
124,457,3_product,fixed,105.42,1
```

Note: Use `.id` (not `/id`) for database IDs

---

## 🎯 RECOMMENDED APPROACH

**For your situation, I recommend**:

### Option A: API Script (Best for 100+ rules)
- Most reliable
- Better error handling
- Can re-run if needed
- Validates data before import

### Option B: CSV with External IDs (Good for clean data)
- Repeatable
- Can version control
- Good for documentation

---

## 📋 PRE-IMPORT CHECKLIST

Before importing pricelist rules, verify:

- [ ] All pricelists exist in Odoo Online (check: Sales → Configuration → Pricelists)
- [ ] All products exist with correct Internal Reference (check: Sales → Products)
- [ ] Product Internal Reference = Product ID from CSV (e.g., `SRV-MANT-RGPD-LSSI`)
- [ ] No duplicate pricelist rules already exist (check existing rules first)

---

## 🔍 VALIDATION AFTER IMPORT

1. **Check Total Count**:
   - Your CSV has 104 rules
   - After import, verify 104 pricelist items exist
   - Settings → Technical → Pricelist Items → Count

2. **Spot Check Specific Rules**:
   - Sales → Configuration → Pricelists → LP_ACORDIA
   - Price Rules tab → Should show: SRV-MANT-RGPD-LSSI @ 41.90€

3. **Test Subscription Pricing**:
   - Create test subscription for customer with pricelist
   - Add product (e.g., SRV-MANT-RGPD-LSSI)
   - Verify price = pricelist price (not product list price)

---

## 🚨 TROUBLESHOOTING

### Error: "Product not found"
**Cause**: Product Internal Reference doesn't match Product ID in CSV
**Fix**: 
1. Export products from Odoo
2. Check `Internal Reference` field
3. Update products or CSV to match

### Error: "Pricelist not found"
**Cause**: Pricelist name doesn't match exactly
**Fix**: Check pricelist names in Odoo (case-sensitive)

### Error: "Field 'applied_on' invalid value"
**Cause**: Wrong value for applied_on field
**Fix**: Use `3_product` (not `3` or `product`)

### Import succeeds but prices wrong in subscription
**Cause**: Customer not linked to correct pricelist
**Fix**: 
1. Open customer record
2. Sales & Purchase tab → Pricelist field
3. Set correct pricelist

---

## ⏱️ TIME ESTIMATE

| Method | Setup | Import | Validation | Total |
|--------|-------|--------|------------|-------|
| API Script | 30 min | 10 min | 30 min | 1-1.5h |
| CSV External IDs | 20 min | 15 min | 30 min | 1-1.5h |
| Manual Mapping | 1h | 20 min | 30 min | 2h |

**Recommended**: API Script (most reliable, best error handling)
