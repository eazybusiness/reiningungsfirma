# Invoice Import Guide

## 📋 Overview

Your friend wants to import sales invoices for 2024 and 2025 (2026 later).

**Current status:** ⚠️ **No invoice CSV files provided yet**

---

## 📁 Required Files

### File 1: Sales Invoices 2024-2025
**Filename:** `invoices_2024_2025.csv` (or similar)

**Required columns:**
- `Invoice Number` or `Name` - Invoice reference (e.g., INV/2024/0001)
- `Customer` or `Partner` - Customer name or VAT
- `Invoice Date` - Date of invoice (YYYY-MM-DD)
- `Due Date` - Payment due date (YYYY-MM-DD)
- `State` - Invoice status (draft, posted, paid, cancelled)
- `Amount Total` - Total invoice amount including tax
- `Amount Tax` - Total tax amount
- `Amount Untaxed` - Subtotal before tax

**Optional but recommended:**
- `Payment Terms` - Payment term name
- `Currency` - Currency code (EUR)
- `Reference` - Customer reference
- `Invoice Origin` - Source document (e.g., subscription)

### File 2: Invoice Lines (if separate)
**Filename:** `invoice_lines_2024_2025.csv`

**Required columns:**
- `Invoice Number` - Link to invoice
- `Product` - Product name or internal reference
- `Description` - Line description
- `Quantity` - Quantity sold
- `Unit Price` - Price per unit
- `Tax` - Tax rate or name
- `Subtotal` - Line total before tax

---

## 📤 How to Export from Old Odoo

### Step 1: Access Invoices
1. Go to: **Contabilidad → Clientes → Facturas**
2. Or: **Facturación → Clientes → Facturas**

### Step 2: Filter by Date
1. Click **Filtros**
2. Add filter: **Fecha de factura**
3. Set range: **2024-01-01 to 2025-12-31**
4. Apply filter

### Step 3: Select All Invoices
1. Click checkbox at top to select all
2. If more than 80 records, select all pages

### Step 4: Export
1. Click **Acción → Exportar**
2. Select format: **CSV**
3. Select fields to export:
   - ✅ Número (Number)
   - ✅ Cliente (Customer/Partner)
   - ✅ Fecha de factura (Invoice Date)
   - ✅ Fecha de vencimiento (Due Date)
   - ✅ Estado (State)
   - ✅ Total (Amount Total)
   - ✅ Impuestos (Amount Tax)
   - ✅ Base imponible (Amount Untaxed)
   - ✅ Condiciones de pago (Payment Terms)
   - ✅ Referencia (Reference)

4. Click **Exportar**
5. Save file as `invoices_2024_2025.csv`

### Step 5: Export Invoice Lines (Optional)
1. Go to: **Contabilidad → Clientes → Líneas de factura**
2. Filter by invoice date range
3. Export with fields:
   - ✅ Factura (Invoice)
   - ✅ Producto (Product)
   - ✅ Descripción (Description)
   - ✅ Cantidad (Quantity)
   - ✅ Precio unitario (Unit Price)
   - ✅ Impuesto (Tax)
   - ✅ Subtotal (Subtotal)

---

## 🔍 Data Validation Before Import

Before importing, validate the CSV:

### Check 1: Customer Matching
All customers in invoices must exist in Odoo Online:
```bash
python3 validate_invoice_customers.py invoices_2024_2025.csv
```

### Check 2: Product Matching
All products in invoice lines must exist in Odoo Online:
```bash
python3 validate_invoice_products.py invoice_lines_2024_2025.csv
```

### Check 3: Date Format
Dates must be in YYYY-MM-DD format:
- ✅ 2024-03-15
- ❌ 15/03/2024
- ❌ 03-15-2024

### Check 4: Currency
All amounts should be in EUR (or consistent currency)

---

## 🚀 Import Process

### Step 1: Prepare Data
```bash
# Validate customers exist
python3 validate_invoice_customers.py invoices_2024_2025.csv

# Validate products exist
python3 validate_invoice_products.py invoice_lines_2024_2025.csv

# Check for duplicates
python3 check_duplicate_invoices.py invoices_2024_2025.csv
```

### Step 2: Test Import (5 invoices)
```bash
python3 import_invoices.py --test --limit 5
```

### Step 3: Review Test Results
- Check invoices created correctly
- Verify customer assignment
- Verify amounts match
- Verify dates correct
- Verify tax calculations

### Step 4: Full Import
```bash
python3 import_invoices.py --confirm
```

### Step 5: Validation
```bash
# Count invoices imported
python3 check_invoices_and_bills.py

# Verify totals match
python3 validate_invoice_totals.py
```

---

## ⚠️ Important Considerations

### 1. Invoice Numbering
- Old invoice numbers should be preserved
- Use `name` field for invoice number
- Odoo may add prefix/suffix based on sequence

### 2. Invoice State
- **draft:** Not validated yet
- **posted:** Validated and posted
- **paid:** Fully paid
- **cancel:** Cancelled

**Recommendation:** Import as **posted** (validated) to preserve history

### 3. Payment Reconciliation
- Invoices can be imported as paid or unpaid
- If paid, payment records should also be imported
- If unpaid, they remain open for payment

### 4. Tax Mapping
- Tax rates must match between old and new Odoo
- 21% IVA should map to existing tax in Odoo Online
- Verify tax configuration before import

### 5. Fiscal Year
- 2024 and 2025 invoices are historical
- Ensure fiscal years are configured in Odoo Online
- Lock periods may prevent editing old invoices

---

## 📊 Expected Results

### For 2024-2025 Invoices:
- **Estimated count:** 500-2000 invoices (depends on business volume)
- **Import time:** 5-30 minutes (depends on count)
- **Validation time:** 10-20 minutes

### After Import:
- ✅ All historical invoices visible in Odoo Online
- ✅ Customer balances reflect historical data
- ✅ Accounting reports show 2024-2025 revenue
- ✅ Invoice numbers preserved from old system

---

## 🛠️ Scripts to Create

Once CSV files are provided, I will create:

1. **`validate_invoice_customers.py`** - Check all customers exist
2. **`validate_invoice_products.py`** - Check all products exist
3. **`check_duplicate_invoices.py`** - Find duplicate invoice numbers
4. **`import_invoices.py`** - Main import script
5. **`validate_invoice_totals.py`** - Verify imported amounts

---

## 📝 Next Steps

**For you:**
1. Ask your friend to export invoice CSV from old Odoo
2. Provide export instructions (see above)
3. Wait for CSV file(s)

**For your friend:**
1. Export invoices 2024-2025 from old Odoo Community
2. Send CSV file(s) to you
3. Optionally: Export invoice lines if needed

**For me (when CSV arrives):**
1. Analyze CSV structure
2. Create import scripts
3. Validate data
4. Test import
5. Full import
6. Verification

---

## ❓ Questions to Ask Your Friend

1. **How many invoices** are there for 2024-2025? (approximate)
2. **Are invoices paid or unpaid?** (or mixed)
3. **Should we import payment records** too?
4. **Are there credit notes** to import?
5. **What about 2026 invoices?** (import separately or together)
6. **Invoice format:** Single CSV or separate invoice + lines?

---

## 🎯 Summary

**Status:** ⚠️ Waiting for invoice CSV files from your friend

**Action required:** Your friend needs to export invoices from old Odoo and send the CSV

**Ready to proceed:** Once CSV is provided, I can create import scripts and complete the migration

The data migration is otherwise complete - this is the final piece.
