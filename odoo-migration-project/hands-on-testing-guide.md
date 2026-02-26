# Hands-On Testing Guide - Odoo Pricelist Import

## 🎯 Goal
Test pricelist import directly in Odoo Online Enterprise with login access.

---

## 📋 Pre-Testing Checklist

Before starting, verify you have:
- [ ] Odoo Online login credentials
- [ ] Access to data files: `/home/nop/Downloads/20260211_OdooMigration/`
- [ ] Import scripts ready: `import_pricelist_rules.py`
- [ ] Python 3 installed on your machine

---

## 🚀 Step-by-Step Testing Process

### Phase 1: Initial Assessment (15 min)

#### 1.1 Login to Odoo Online
- URL: `https://[instance].odoo.com`
- Login with provided credentials
- Verify you can access: Sales, Subscriptions, Settings

#### 1.2 Check Current Status
Navigate and count existing records:

**Pricelists**:
- Sales → Configuration → Pricelists
- Count: Should have ~70 pricelists
- Note: Are they named correctly? (LP_ACORDIA, LP_AIRMATIC, etc.)

**Products**:
- Sales → Products → Products
- Count: Should have ~20 products
- Check one product: Does it have "Internal Reference" field set?
  - Click a product → General Information tab
  - Look for "Internal Reference" field
  - Should be something like: `SRV-MANT-RGPD-LSSI`

**Pricelist Items** (Current state):
- Enable Developer Mode: Settings → Activate Developer Mode
- Settings → Technical → Database Structure → Models
- Search: `product.pricelist.item`
- Click "Records"
- Count: How many exist? (Should be 0 or very few if import failed)

**Document findings**:
```
Pricelists: ___ found
Products: ___ found
Products with Internal Reference: ___
Pricelist Items: ___ found (should be 104 after import)
```

---

### Phase 2: Product Validation (15-30 min)

#### 2.1 Export Products
- Sales → Products → Products
- Select all products (checkbox at top)
- Action → Export
- Fields to export:
  - Name
  - Internal Reference
  - Product ID (database ID)
- Download CSV

#### 2.2 Check Internal References
Open exported CSV and verify:
- Does every product have "Internal Reference" filled?
- Does it match the Product ID from source data?
  - Example: Product should have Internal Reference = `SRV-MANT-RGPD-LSSI`

**If Internal References are MISSING or WRONG**:
- We need to fix this before importing pricelist rules
- Pricelist rules reference products by Internal Reference
- Share the exported CSV with me → I'll create fix script

**If Internal References are CORRECT**:
- ✅ Proceed to pricelist import

---

### Phase 3: Pricelist Import - API Method (30-60 min)

#### 3.1 Get Odoo API Key
- Settings → Users & Companies → Users
- Click your user
- Preferences tab → API Keys section
- Click "New API Key"
- Description: "Pricelist Import"
- Copy the API key (save it securely)

#### 3.2 Configure Import Script
Edit `/home/nop/Downloads/20260211_OdooMigration/import_pricelist_rules.py`:

```python
# Update these lines:
ODOO_URL = 'https://yourinstance.odoo.com'  # Your actual URL
ODOO_DB = 'yourdb'  # Your database name
ODOO_USERNAME = 'your@email.com'  # Your login email
ODOO_API_KEY = 'paste_api_key_here'  # The key you just created
```

#### 3.3 Test with Sample Data (IMPORTANT)
Before importing all 104 rules, test with 5 rules:

**Create test file**:
```bash
cd /home/nop/Downloads/20260211_OdooMigration/
head -6 pricelist_rules.csv > pricelist_rules_test.csv
```

**Update script to use test file**:
```python
CSV_FILE = 'pricelist_rules_test.csv'  # Change this line temporarily
```

**Run test import**:
```bash
python3 import_pricelist_rules.py
```

**Expected output**:
```
✅ Connected to Odoo as user ID: 123
📊 Found 5 pricelist rules to import

[1/5] Processing: LP_ACORDIA → SRV-MANT-RGPD-LSSI @ 41.90€
  ✅ Created pricelist item ID: 456
[2/5] Processing: LP_AIRMATIC → SRV-MANT-CD @ 105.42€
  ✅ Created pricelist item ID: 457
...

✅ Successfully imported: 5
❌ Errors: 0
```

#### 3.4 Validate Test Import in Odoo
- Sales → Configuration → Pricelists
- Open "LP_ACORDIA"
- Go to "Price Rules" tab
- Should see: SRV-MANT-RGPD-LSSI with price 41.90€

**If test successful** → Proceed to full import
**If errors** → Share error message, I'll debug

#### 3.5 Full Import (All 104 Rules)
**Update script back to full file**:
```python
CSV_FILE = 'pricelist_rules.csv'  # Use full file
```

**Run full import**:
```bash
python3 import_pricelist_rules.py
```

**Monitor output**:
- Should process all 104 rules
- Note any errors
- Final count: "✅ Successfully imported: 104"

#### 3.6 Validate Full Import
**Check total count**:
- Settings → Technical → Pricelist Items
- Count should be 104 (or close to it)

**Spot check multiple pricelists**:
- LP_ACORDIA → Should have 1 rule
- LP_AIRMATIC → Should have 4 rules (CD, DPD, RGPD, LSSI)
- LP_SCA → Should have 6 rules

**Document results**:
```
Total pricelist items imported: ___
Errors encountered: ___
Sample pricelists checked: ✅/❌
```

---

### Phase 4: Subscription Workflow Test (30-60 min)

#### 4.1 Select Test Customer
Choose a customer with pricelist:
- Sales → Customers
- Open a customer (e.g., one linked to LP_AIRMATIC)
- Check: Sales & Purchase tab → Pricelist field
- Should show their pricelist (e.g., LP_AIRMATIC)

**If pricelist NOT assigned**:
- Set it manually for testing
- Select pricelist from dropdown
- Save

#### 4.2 Create Test Subscription
- Subscriptions → Subscriptions → Create
- Customer: Select test customer (e.g., with LP_AIRMATIC)
- Subscription Template: PLANTILLA_MANTENIMIENTO_MENSUAL
- Add products:
  - Product: SRV-MANT-CD
  - Quantity: 1
  - **Check price**: Should show 105.42€ (from pricelist), NOT 0€ (product list price)
- Start Date: Today
- Confirm subscription

#### 4.3 Generate Test Invoice
- On the subscription, click "Create Invoice"
- Check invoice lines:
  - Product: SRV-MANT-CD
  - Price: Should be 105.42€ (pricelist price)
  - Total: Should match

**Critical validation**:
- ✅ Invoice price = Pricelist price (105.42€)
- ❌ Invoice price = Product list price (0€) → Pricelist not working

#### 4.4 Test Multiple Products
Add another product to subscription:
- Edit subscription
- Add line: SRV-MANT-DPD
- Quantity: 1
- **Check price**: Should be 42.14€ (from LP_AIRMATIC pricelist)
- Generate invoice
- Validate pricing

**Document results**:
```
Test Customer: ___
Pricelist: ___
Product 1: ___ @ ___€ (expected: ___€) ✅/❌
Product 2: ___ @ ___€ (expected: ___€) ✅/❌
Invoice total correct: ✅/❌
```

---

### Phase 5: Final Validation (15-30 min)

#### 5.1 Data Integrity Checks

**All customers have pricelists**:
- Sales → Customers
- Export: Name, Pricelist
- Check: Every customer should have pricelist assigned

**All pricelists have rules**:
- Sales → Configuration → Pricelists
- Spot check 5-10 pricelists
- Each should have at least 1 price rule

**Product references correct**:
- All products have Internal Reference
- Pricelist rules reference correct products

#### 5.2 Edge Case Testing

**Test customer with multiple products**:
- Customer: LP_COMERGRUP (has 4 products)
- Create subscription with all 4 products
- Verify each has correct price

**Test quarterly subscription** (if applicable):
- Customer: LP_SANGUESA (has quarterly template)
- Create subscription
- Verify pricing and billing frequency

#### 5.3 Document Completion Status

**What's working**:
- [ ] All 104 pricelist rules imported
- [ ] Products have correct Internal References
- [ ] Customers linked to pricelists
- [ ] Subscriptions create with correct pricing
- [ ] Invoices generate with pricelist prices

**What still needs to be done** (for your friend):
- [ ] Bank accounts (IBAN/SEPA) configuration
- [ ] VeriFactu setup (if required)
- [ ] User training
- [ ] Production subscriptions creation
- [ ] Ongoing support setup

---

## 🐛 Troubleshooting Guide

### Error: "Authentication failed"
**Cause**: Wrong API credentials
**Fix**: 
- Double-check ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_API_KEY
- Regenerate API key if needed

### Error: "Pricelist not found: LP_ACORDIA"
**Cause**: Pricelist name doesn't match exactly
**Fix**:
- Check pricelist names in Odoo (case-sensitive)
- Export pricelists, compare with CSV
- Update CSV or Odoo to match

### Error: "Product not found: SRV-MANT-RGPD-LSSI"
**Cause**: Product Internal Reference not set or doesn't match
**Fix**:
- Export products, check Internal Reference field
- Update products to have correct Internal Reference
- OR update CSV to match existing Internal References

### Invoice shows wrong price (0€ instead of pricelist price)
**Cause**: Customer not linked to pricelist OR pricelist rule not imported
**Fix**:
- Check customer → Sales & Purchase tab → Pricelist field
- Check pricelist → Price Rules tab → Verify rule exists
- Re-import pricelist rules if missing

### Subscription doesn't use pricelist price
**Cause**: Subscription template or product configuration issue
**Fix**:
- Check subscription uses customer's pricelist (not default)
- Verify product is in pricelist rules
- Check pricelist rule is active (no end date or future end date)

---

## 📊 Success Criteria

**You'll know it's working when**:
1. ✅ Import script completes with 104 rules imported
2. ✅ Pricelists show correct price rules
3. ✅ Test subscription shows pricelist prices (not 0€)
4. ✅ Test invoice has correct totals
5. ✅ Multiple products in subscription all have correct prices

**Then you can tell your friend**:
"Pricelist import is working! I've tested subscriptions and invoicing - prices are correct. You can now create production subscriptions. Still need to configure bank accounts and VeriFactu if required."

---

## 🤝 When to Ask for Help

**Share with me if you encounter**:
- Import script errors (copy full error message)
- Products missing Internal References (share exported CSV)
- Pricing not working in subscriptions (screenshot)
- Any other unexpected behavior

**I'll help debug**:
- Fix import script
- Create product fix script
- Troubleshoot pricelist configuration
- Validate workflow

---

## ⏱️ Estimated Time

| Phase | Time |
|-------|------|
| Initial assessment | 15 min |
| Product validation | 15-30 min |
| Pricelist import | 30-60 min |
| Subscription testing | 30-60 min |
| Final validation | 15-30 min |
| **TOTAL** | **2-3 hours** |

Add 1-2 hours for troubleshooting if issues arise.

---

## 📝 Testing Checklist

Print this and check off as you go:

**Pre-Testing**:
- [ ] Odoo login works
- [ ] Data files accessible
- [ ] Python 3 installed

**Product Validation**:
- [ ] Products exported
- [ ] Internal References checked
- [ ] All products have correct references

**Pricelist Import**:
- [ ] API key generated
- [ ] Script configured
- [ ] Test import (5 rules) successful
- [ ] Full import (104 rules) successful
- [ ] Validated in Odoo UI

**Subscription Testing**:
- [ ] Test customer selected
- [ ] Pricelist assigned to customer
- [ ] Subscription created
- [ ] Prices match pricelist
- [ ] Invoice generated
- [ ] Invoice totals correct

**Final Validation**:
- [ ] All customers have pricelists
- [ ] All pricelists have rules
- [ ] Edge cases tested
- [ ] Documentation complete

**Handoff**:
- [ ] Documented what's working
- [ ] Documented remaining tasks
- [ ] Shared results with friend
