# Odoo Migration - Step-by-Step Execution Guide

## 🎯 Current Situation
- ✅ Products imported BUT missing Internal Reference field
- ✅ Pricelists created BUT no price rules
- ❌ Cannot import pricelist rules (products have no Internal Reference to match)

## 🔧 Solution: 3-Step Process

---

## STEP 1: Fix Product Internal References (30 minutes)

### What This Does
Updates all products in Odoo to have their correct Internal Reference field (e.g., `SRV-MANT-RGPD`).

### Execute

```bash
cd /home/nop/CascadeProjects/freelance_project_cuotes/odoo-migration-project/20260211_OdooMigration

# Run the fix script
python3 fix_product_internal_references.py
```

### Expected Output
```
Connecting to https://exartia.odoo.com...
✅ Connected as user ID: 2
📄 Loaded 18 products from CSV
✅ Updated: SRV-SETUP-RGPD
✅ Updated: SRV-SETUP-LSSI
✅ Updated: SRV-MANT-RGPD
...
📊 SUMMARY:
   ✅ Updated: 18
   ⚠️  Not found: 0
   ❌ Errors: 0
```

### Verify in Odoo
1. Go to: `Ventas → Productos → Productos` (Sales → Products → Products)
2. Click any product
3. Check field "Referencia" (Internal Reference)
4. Should now show: `SRV-MANT-RGPD` (or similar)

---

## STEP 2: Verify Products (5 minutes)

### What This Does
Confirms all products have Internal References set correctly.

### Execute

```bash
python3 verify_products.py
```

### Expected Output
```
📦 Total products in Odoo: 18
PRODUCT VERIFICATION REPORT
✅ SRV-SETUP-RGPD              | Inicio proyecto: Adecuación completa al RGPD...
✅ SRV-MANT-RGPD               | Cuota mensual correspondiente a los siguientes...
...
📊 SUMMARY:
   ✅ Products WITH Internal Reference: 18
   ❌ Products WITHOUT Internal Reference: 0

🎉 ALL PRODUCTS HAVE INTERNAL REFERENCES! Ready to import pricelist rules.
```

### If Any Products Missing References
Run `fix_product_internal_references.py` again or manually set in Odoo UI.

---

## STEP 3: Import Pricelist Rules (1-2 hours)

### What This Does
Imports all 104 pricelist rules using the corrected CSV and product Internal References.

### Execute

```bash
python3 import_pricelist_rules_fixed.py
```

### Expected Output - Test Phase
```
STEP 1: TEST IMPORT (5 items)
Connecting to https://exartia.odoo.com...
✅ Connected as user ID: 2
📄 Loaded 104 pricelist items from CSV
🧪 TEST MODE: Importing only 5 items
✅ [1/5] LP-ACORDIA | SRV-MANT-RGPD-LSSI | €41.90
✅ [2/5] LP-AIRMATIC | SRV-MANT-CD | €105.42
✅ [3/5] LP-AIRMATIC | SRV-MANT-DPD | €42.14
✅ [4/5] LP-AIRMATIC | SRV-MANT-RGPD | €57.85
✅ [5/5] LP-AIRMATIC | SRV-MANT-LSSI | €20.03

📊 IMPORT SUMMARY:
   ✅ Imported: 5
   ❌ Errors: 0

Test successful! Import all items? (yes/no):
```

### Type: `yes`

### Expected Output - Full Import
```
STEP 2: FULL IMPORT (all items)
🚀 PRODUCTION MODE: Importing all 104 items
✅ [1/104] LP-ACORDIA | SRV-MANT-RGPD-LSSI | €41.90
✅ [2/104] LP-AIRMATIC | SRV-MANT-CD | €105.42
...
✅ [104/104] LP-ZUMEX | SRV-MANT-RGPD-LSSI | €38.00

📊 IMPORT SUMMARY:
   ✅ Imported: 104
   ❌ Errors: 0

✅ Import completed!
```

### Verify in Odoo
1. Go to: `Ventas → Configuración → Tarifas` (Sales → Configuration → Pricelists)
2. Click any pricelist (e.g., "LP_ACORDIA")
3. Click tab "Reglas de precio" (Price Rules)
4. Should see price rules listed with products and prices

---

## STEP 4: Test Subscription Workflow (30 minutes)

### Create Test Subscription

1. Go to: `Suscripciones → Suscripciones` (Subscriptions → Subscriptions)
2. Click "Crear" (Create)
3. Select customer: "ACORDIA" (or any customer with pricelist)
4. Add product: "SRV-MANT-RGPD-LSSI"
5. **CRITICAL CHECK:** Price should be €41.90 (from pricelist), NOT €1.00 (product list price)
6. If price is correct → Click "Confirmar" (Confirm)
7. Generate first invoice

### Validate Invoice

1. Click "Crear factura" (Create Invoice)
2. Check invoice line price: Should match pricelist (€41.90)
3. Check total: Should be correct with tax
4. If all correct → **SUCCESS!** 🎉

### If Price is Wrong

**Problem:** Subscription using product list price instead of pricelist price

**Possible Causes:**
1. Customer doesn't have pricelist assigned
2. Pricelist rules not imported correctly
3. Subscription not using customer's pricelist

**Fix:**
1. Check customer record → Tab "Ventas y compras" → Field "Tarifa"
2. Should show customer's pricelist (e.g., "LP_ACORDIA")
3. If empty, assign correct pricelist
4. Delete test subscription and create new one

---

## 🚨 Troubleshooting

### Error: "Authentication failed"
**Fix:** Check credentials in script:
- URL: `https://exartia.odoo.com`
- DB: `exartia`
- Username: `eduardo.mateo@exartia.net`
- Password: `ExartiaTemporal2026`

### Error: "Product not found (Internal Ref): SRV-MANT-RGPD"
**Fix:** Product Internal Reference not set correctly
1. Run `verify_products.py` to check
2. Run `fix_product_internal_references.py` again
3. Or manually set in Odoo UI

### Error: "Pricelist not found: LP-ACORDIA"
**Fix:** Pricelist name mismatch
1. Check pricelist names in Odoo
2. They should be: `LP_ACORDIA` (with underscore)
3. If different, update `parse_external_id()` function in script

### Error: Module 'xmlrpc.client' not found
**Fix:** Install Python (already included in Python 3)
```bash
python3 --version  # Should show Python 3.x
```

---

## 📊 Database Backup

### Option 1: Via Odoo.sh (If Available)
1. Go to Odoo.sh dashboard
2. Select database
3. Click "Backup"
4. Download backup file

### Option 2: Via Settings (Odoo Online)
**Note:** Backup option may not be available in Odoo Online trial/standard

### Option 3: Export Data Manually
1. Export customers: `Contactos → Exportar`
2. Export products: `Productos → Exportar`
3. Export pricelists: `Tarifas → Exportar`
4. Save all CSV files with timestamp

### Recommended: Manual Export Before Each Step
Before running each script, export:
- Products list
- Pricelists list
- Current pricelist items (if any)

---

## ✅ Success Checklist

- [ ] Step 1: Products have Internal References (verify_products.py shows 100%)
- [ ] Step 2: Pricelist rules imported (104 items in Odoo)
- [ ] Step 3: Test subscription created
- [ ] Step 4: Invoice generated with correct pricelist pricing
- [ ] Step 5: Customer can see correct prices in subscription

---

## 📞 What to Tell Your Friend

"I've debugged the issue. The problem was products were imported without Internal Reference field, so pricelist rules couldn't match them. I've created 3 scripts to fix everything:

1. **fix_product_internal_references.py** - Sets Internal References for all products
2. **verify_products.py** - Confirms all products are ready
3. **import_pricelist_rules_fixed.py** - Imports all 104 pricelist rules

Run them in order, should take 2-3 hours total. Then test a subscription to confirm pricing works. The scripts handle everything automatically - no manual UI work needed."

---

## ⏱️ Time Estimate

| Task | Time |
|------|------|
| Fix product references | 30 min |
| Verify products | 5 min |
| Import pricelist rules | 1-2 hours |
| Test subscription | 30 min |
| **TOTAL** | **2-3 hours** |

---

## 🎯 After This is Done

Your friend still needs to handle:
- ❌ Bank accounts (IBAN/SEPA) - Manual configuration
- ❌ Customer data normalization - If needed
- ❌ VeriFactu setup - If required for Spain
- ❌ Azure AD / Outlook integration - Separate task
- ❌ User training - Separate task

But the **CRITICAL BLOCKER** (pricelist rules) will be resolved! 🎉
