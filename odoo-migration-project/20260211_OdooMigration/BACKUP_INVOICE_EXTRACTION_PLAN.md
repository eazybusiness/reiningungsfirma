# Backup Invoice Extraction & Import Plan

## 📦 Backup Analysis

**Backup source:** Odoo 18.0 Community (Production database: "Exartia-odoo-produccion")  
**Backup date:** December 26, 2024  
**Backup size:** 48.3 MB (SQL dump)  
**Filestore:** 1,759 files (attachments, PDFs, etc.)

---

## ✅ YES - We Can Extract and Import Invoices!

The backup contains complete invoice and payment data in PostgreSQL format.

### Available Data Tables:

1. **`account_move`** - Invoices and accounting entries
   - Contains: Invoice headers, totals, dates, customer info, payment status
   - Estimated: ~1,340 records (includes all move types)

2. **`account_move_line`** - Invoice lines and journal entries
   - Contains: Products, quantities, prices, taxes per line
   - Estimated: Several thousand lines

3. **`account_payment`** - Payment records
   - Contains: Payment amounts, dates, methods, reconciliation
   - Available in backup

---

## 🎯 Extraction Strategy

### Option 1: Direct SQL Extraction (Recommended)

**Restore backup to local PostgreSQL and query directly:**

```bash
# 1. Create local database
createdb odoo_backup_analysis

# 2. Restore backup
psql odoo_backup_analysis < odoo_backup/dump.sql

# 3. Extract invoices with SQL queries
psql odoo_backup_analysis -c "
SELECT 
    am.name as invoice_number,
    rp.name as customer_name,
    rp.vat as customer_vat,
    am.invoice_date,
    am.invoice_date_due,
    am.state,
    am.move_type,
    am.amount_untaxed,
    am.amount_tax,
    am.amount_total,
    am.payment_state
FROM account_move am
LEFT JOIN res_partner rp ON am.partner_id = rp.id
WHERE am.move_type = 'out_invoice'
  AND am.invoice_date >= '2024-01-01'
  AND am.invoice_date <= '2025-12-31'
ORDER BY am.invoice_date
" -o invoices_2024_2025.csv --csv
```

**Pros:**
- ✅ Complete control over data
- ✅ Can query any field
- ✅ Can join tables for complete data
- ✅ Fast and reliable

**Cons:**
- ⚠️ Requires PostgreSQL installed locally
- ⚠️ 48MB database restore

---

### Option 2: Parse SQL Dump Directly

**Extract data from dump.sql without restoring:**

```python
# Parse COPY statements from dump.sql
# Extract account_move records
# Match with res_partner for customer names
# Export to CSV
```

**Pros:**
- ✅ No database restore needed
- ✅ Faster for single-table extraction

**Cons:**
- ⚠️ More complex parsing
- ⚠️ Harder to join tables
- ⚠️ May miss relationships

---

## 📋 Data We Can Extract

### Invoice Headers (account_move)
- Invoice number (`name`)
- Customer ID and name (`partner_id`)
- Invoice date (`invoice_date`)
- Due date (`invoice_date_due`)
- Invoice type (`move_type`: out_invoice, out_refund, etc.)
- State (`state`: draft, posted, cancel)
- Payment state (`payment_state`: not_paid, in_payment, paid)
- Amounts:
  - Untaxed (`amount_untaxed`)
  - Tax (`amount_tax`)
  - Total (`amount_total`)
  - Residual/unpaid (`amount_residual`)
- Payment terms (`invoice_payment_term_id`)
- Currency (`currency_id`)
- Reference (`ref`)
- Origin (`invoice_origin`)

### Invoice Lines (account_move_line)
- Product (`product_id`)
- Description (`name`)
- Quantity (`quantity`)
- Unit price (`price_unit`)
- Tax (`tax_ids`)
- Subtotal (`price_subtotal`)
- Total with tax (`price_total`)

### Payments (account_payment)
- Payment number (`name`)
- Partner/customer (`partner_id`)
- Amount (`amount`)
- Date (`date`)
- Payment method (`payment_method_id`)
- State (`state`)
- Reference (`ref`)

---

## 🚀 Import Process

### Step 1: Extract Data from Backup

**Using PostgreSQL (recommended):**

```bash
# Restore backup
createdb odoo_backup
psql odoo_backup < odoo_backup/dump.sql

# Extract invoices 2024-2025
python3 extract_invoices_from_backup.py --year 2024-2025 --output invoices_2024_2025.csv

# Extract invoice lines
python3 extract_invoice_lines_from_backup.py --year 2024-2025 --output invoice_lines_2024_2025.csv

# Extract payments
python3 extract_payments_from_backup.py --year 2024-2025 --output payments_2024_2025.csv
```

### Step 2: Validate Extracted Data

```bash
# Check customer matching
python3 validate_invoice_customers.py invoices_2024_2025.csv

# Check product matching
python3 validate_invoice_products.py invoice_lines_2024_2025.csv

# Check for duplicates
python3 check_duplicate_invoices.py invoices_2024_2025.csv
```

### Step 3: Transform Data for Odoo Online

**Map fields from Community to Online:**
- Customer IDs → Match by VAT
- Product IDs → Match by internal reference
- Payment term IDs → Match by name
- Tax IDs → Match by rate/name
- Journal IDs → Use default sales journal

### Step 4: Import to Odoo Online

```bash
# Test import (5 invoices)
python3 import_invoices.py --test --limit 5

# Review in Odoo UI

# Full import
python3 import_invoices.py --confirm --year 2024-2025
```

### Step 5: Import Payments (Optional)

```bash
# Import payments and reconcile with invoices
python3 import_payments.py --confirm
```

---

## ⚠️ Important Considerations

### 1. Invoice Numbering
- **Preserve original numbers:** Use `name` field from backup
- **Sequence conflict:** Odoo Online may have different sequence
- **Solution:** Import with original numbers, adjust sequence after

### 2. Customer Matching
- **Match by VAT:** All customers already imported with VAT
- **Validation:** Check all invoice customers exist in Odoo Online
- **Missing customers:** Import before invoices

### 3. Product Matching
- **Match by internal reference:** All products have `default_code`
- **Validation:** Check all invoice products exist in Odoo Online
- **Missing products:** Import before invoices

### 4. Tax Configuration
- **Spain taxes:** 21% IVA standard
- **Verify:** Tax rates match between systems
- **Map:** Old tax IDs → New tax IDs

### 5. Payment State
- **Preserve state:** Import as paid/unpaid based on `payment_state`
- **Reconciliation:** If paid, import payment records too
- **Bank statements:** May need separate import

### 6. Fiscal Periods
- **2024-2025 closed?** Check if fiscal years are locked
- **Posting:** Import as `posted` (validated) state
- **Dates:** Preserve original invoice dates

### 7. Invoice Types
- **out_invoice:** Customer invoices (import these)
- **out_refund:** Credit notes (import these)
- **in_invoice:** Vendor bills (optional)
- **in_refund:** Vendor credit notes (optional)
- **entry:** Journal entries (skip)

---

## 📊 Expected Results

### Invoices 2024-2025:
Based on backup sample, we can see invoices from 2026 (recent), so likely:
- **2024 invoices:** 200-800 (estimate)
- **2025 invoices:** 200-800 (estimate)
- **Total:** 400-1,600 invoices

### Invoice Lines:
- **Average 3-5 lines per invoice**
- **Total lines:** 1,200-8,000 (estimate)

### Payments:
- **Depends on payment state**
- **If most paid:** Similar count to invoices
- **If unpaid:** Fewer payment records

---

## 🛠️ Scripts to Create

### 1. `extract_invoices_from_backup.py`
Restore backup and extract invoice data to CSV

### 2. `extract_invoice_lines_from_backup.py`
Extract invoice line items with products

### 3. `extract_payments_from_backup.py`
Extract payment records

### 4. `validate_invoice_data.py`
Validate customers, products, taxes exist in Odoo Online

### 5. `import_invoices.py`
Import invoices to Odoo Online via XML-RPC

### 6. `import_payments.py`
Import payments and reconcile with invoices

---

## ✅ Advantages of Using Backup

### vs. CSV Export from UI:
1. **Complete data:** All fields, not just visible ones
2. **Relationships:** Can join tables (customer, products, taxes)
3. **No manual work:** Automated extraction
4. **Consistent format:** SQL data is structured
5. **Bulk processing:** Can extract thousands of records
6. **Historical data:** Even deleted/archived records

### vs. ngrok/Remote Access:
1. **Offline work:** No need for server running
2. **No time limit:** Can take as long as needed
3. **Repeatable:** Can re-extract if needed
4. **No security concerns:** One-time backup transfer

---

## 🎯 Recommended Approach

**Use the backup for invoice extraction:**

1. ✅ Restore `dump.sql` to local PostgreSQL
2. ✅ Create SQL queries to extract invoices, lines, payments
3. ✅ Export to CSV files
4. ✅ Validate data against Odoo Online
5. ✅ Import using XML-RPC scripts
6. ✅ Verify imported data

**Timeline:**
- Restore backup: 5 minutes
- Create extraction scripts: 30 minutes
- Extract data: 5 minutes
- Validate data: 15 minutes
- Create import scripts: 45 minutes
- Test import: 15 minutes
- Full import: 30 minutes
- **Total: ~2.5 hours**

---

## 📝 Next Steps

**For you:**
1. Confirm you want to proceed with backup extraction
2. Install PostgreSQL locally (if not already installed)
3. Provide any specific requirements (date ranges, invoice types, etc.)

**For me:**
1. Create backup restoration script
2. Create SQL extraction queries
3. Create CSV export scripts
4. Create validation scripts
5. Create import scripts
6. Test with sample data
7. Full import

---

## ❓ Questions Before Starting

1. **PostgreSQL installed?** Do you have PostgreSQL on your system?
2. **Date range:** Only 2024-2025, or include 2026 too?
3. **Invoice types:** Customer invoices only, or credit notes too?
4. **Payments:** Import payment records, or just invoices?
5. **Paid vs unpaid:** Import all, or only unpaid invoices?
6. **Vendor bills:** Import vendor bills (in_invoice) too?

---

## 🎉 Summary

**YES - We can extract invoices from the backup!**

The backup contains complete invoice data in PostgreSQL format. We can:
- ✅ Extract all invoices from 2024-2025 (or any date range)
- ✅ Extract invoice lines with products
- ✅ Extract payment records
- ✅ Import to Odoo Online
- ✅ Preserve original invoice numbers and dates
- ✅ Match customers and products automatically

This is actually **better than CSV export** because we have complete control over the data and can extract everything we need programmatically.

Ready to proceed when you are!
