# Missing Data Report - Odoo Migration

## 🚨 CRITICAL FINDING

### **0 CUSTOMERS IN ODOO!**

The diagnostic script found **ZERO customers** in the Odoo Online instance. This is a critical blocker - customers need to be imported before testing subscriptions.

---

## 📊 Issues Found

### **Products: 3 Issues**

1. **Missing Internal Reference: 1 product**
   - "Booking Fees" (not critical - not used in pricelists)

2. **Missing Category: 19 products** ⚠️ IMPORTANT
   - All SRV-SETUP-* products (8 products)
   - All SRV-MANT-* products (10 products)
   - SRV-FORMACION (1 product)
   - Should be: "Services" category

3. **Missing Taxes: 4 products**
   - DUA10, DUA21, DUA4 (VAT valuation products)
   - Booking Fees
   - Should have: 21% IVA tax

### **Customers: CRITICAL** 🚨

**0 customers imported!**

Expected fields from customers.csv:
- VAT (Tax ID)
- Name
- Email
- Phone
- Street, City, Zip, Country
- Price list (e.g., LP_ACORDIA)
- Payment terms
- IBAN (bank account)
- Payment method
- SEPA mandate

---

## 🎯 What Your Friend Meant

When he said:
> "plz update product (missing product ID) and customer (missing some field with csv files) import"

He meant:

1. **Products:** Missing **category** field (not Product ID - that's the Internal Reference we already fixed)
   - 19 products have no category assigned
   - Should be "Services" category

2. **Customers:** **Not imported at all!**
   - CSV has ~70 customers
   - Odoo has 0 customers
   - Need to import from customers.csv

---

## ✅ Solutions

### Solution 1: Fix Product Categories & Taxes
Script: `fix_product_categories.py`
- Assign "Services" category to all SRV-* products
- Assign 21% IVA tax to products missing taxes

### Solution 2: Import Customers
Script: `import_customers.py`
- Import all customers from customers.csv
- Include: VAT, contact info, address, pricelist assignment
- Include: IBAN/bank accounts
- Include: payment terms

---

## ⏱️ Time Estimate

| Task | Time |
|------|------|
| Fix product categories/taxes | 15 min |
| Import customers | 1-2 hours |
| Validate customer-pricelist links | 30 min |
| **TOTAL** | **2-3 hours** |

---

## 🔴 Priority Order

1. **Import customers** (CRITICAL - can't test subscriptions without customers)
2. **Fix product categories** (IMPORTANT - for proper organization)
3. **Validate pricelist assignments** (ensure customers have correct pricelists)
4. **Test subscription workflow** (final validation)
