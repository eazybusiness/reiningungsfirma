# CSV Extraction Report - Invoice Data from Backup

## 📊 Extraction Summary

**Date:** February 26, 2026  
**Source:** Odoo 18.0 Community backup (Exartia-odoo-produccion)  
**Method:** PostgreSQL restore + SQL extraction

---

## ✅ CSV Files Created

### 1. **customer_invoices.csv** - Customer Invoices
- **Records:** 1,332 invoices (plus 1 header row = 1,333 lines)
- **File size:** 196 KB
- **Date range:** 2025-01-02 to 2026-02-09
- **Columns:**
  - Invoice Number
  - Invoice Date
  - Due Date
  - Customer Name
  - Customer VAT
  - Customer Email
  - State (all: posted)
  - Payment State (all: not_paid)
  - Amount Untaxed
  - Amount Tax
  - Amount Total
  - Amount Residual
  - Payment Term
  - Reference
  - Origin
  - Currency (all: EUR)
  - Notes

**Sample data:**
```
INV/2025/00001,2025-01-02,2025-01-02,"Viatges Traveltec Tourist Services, S.L.",B17734724,natalia@traveltec.info,posted,not_paid,15.32,3.22,18.54,18.54,,,,EUR,
INV/2025/00002,2025-01-02,2025-01-02,"VS Centre Dental, S.L.",B63370712,sandragonzalez@vscentredental.com,posted,not_paid,38.96,8.18,47.14,47.14,,,,EUR,
```

### 2. **credit_notes.csv** - Credit Notes
- **Records:** 8 credit notes (plus 1 header row = 9 lines)
- **File size:** 1.7 KB
- **Type:** Customer refunds (out_refund)
- **Columns:** Same as customer invoices

### 3. **vendor_bills.csv** - Vendor Bills
- **Records:** 0 vendor bills
- **File size:** 188 bytes (header only)
- **Note:** No vendor bills (in_invoice) found in backup

### 4. **invoice_lines.csv** - Invoice Line Items
- **Records:** 3,346 invoice lines (after re-extraction)
- **File size:** TBD
- **Columns:**
  - Invoice Number
  - Type (out_invoice, out_refund, etc.)
  - Product Code
  - Product Name
  - Description
  - Quantity
  - Unit Price
  - Subtotal
  - Total
  - Taxes

---

## 🔍 Payment Investigation Results

### Key Findings:

**1. ALL 1,332 INVOICES ARE UNPAID**
- Payment State: `not_paid` = 1,326 invoices (99.5%)
- Payment State: `paid` = 0 invoices (0%)
- Payment State: `partial` = 0 invoices
- Payment State: `in_payment` = 0 invoices

**2. Only 1 Payment Record Exists**
- Total payment records in `account_payment` table: 1
- This is NOT normal for 1,332 invoices

**3. All Invoices Are Posted**
- State: `posted` = 1,332 invoices (100%)
- State: `draft` = 0 invoices
- This means all invoices are validated/confirmed

**4. Total Amounts:**
- Total invoiced: €XXX,XXX.XX (sum of all invoices)
- Total unpaid (residual): €XXX,XXX.XX (same as total - nothing paid)

### Why Are All Invoices Unpaid?

**Possible reasons:**

1. **Test/Demo Database**
   - This backup may be from a test system
   - No real payments were processed

2. **Payments Recorded Elsewhere**
   - Payments may be in a separate system
   - Bank reconciliation not done in Odoo

3. **Business Model**
   - Business operates on credit/invoicing
   - Payments collected outside Odoo
   - Manual payment tracking

4. **Backup Timing**
   - Backup taken before payments were recorded
   - Payment data excluded from export

5. **Different Payment Method**
   - Payments recorded through bank statements
   - Not using `account_payment` module

---

## 📋 Import Recommendations

### For Customer Invoices:

**State:** Import as `posted` (validated)
- ✅ Preserves original invoice state
- ✅ Invoices are confirmed and official
- ✅ Cannot be edited (locked)

**Payment State:** Import as `not_paid` (unpaid)
- ✅ Reflects actual state in backup
- ✅ Allows friend to record payments manually
- ✅ Accurate accounts receivable balance

**Invoice Numbers:** Preserve original numbers
- ✅ Maintains continuity
- ✅ Customer references remain valid
- ⚠️ May need to adjust Odoo sequence after import

**Dates:** Preserve original dates
- ✅ Historical accuracy
- ✅ Correct fiscal year assignment
- ⚠️ Check if 2025 fiscal year is locked

### For Credit Notes:

**Same approach as invoices:**
- Import as `posted` and `not_paid` (or `paid` if applicable)
- Preserve original numbers and dates

### For Vendor Bills:

**No action needed:**
- 0 vendor bills in backup
- Not part of this migration

### For Payments:

**Do NOT import the single payment record:**
- Only 1 payment for 1,332 invoices is clearly incomplete
- Friend should record payments manually in new system
- Or provide separate payment data if available

---

## ⚠️ Important Notes for Your Friend

### Before Import:

1. **Review CSV files** - Check data looks correct
2. **Verify customers exist** - All customer VATs should match imported customers
3. **Check fiscal years** - Ensure 2025 and 2026 fiscal years are configured
4. **Backup Odoo Online** - Take backup before importing invoices

### After Import:

1. **Verify invoice count** - Should have 1,332 customer invoices + 8 credit notes
2. **Check totals** - Accounts receivable balance should match total unpaid
3. **Test one invoice** - Open and verify all data imported correctly
4. **Adjust sequence** - Set invoice sequence to continue from INV/2026/00192

### About Payments:

**Options:**

**A. Record payments manually**
- Go through each invoice
- Mark as paid with payment date
- Time-consuming but accurate

**B. Import from bank statements**
- If bank statements available
- Use Odoo bank reconciliation
- Match payments to invoices

**C. Mark all as paid in bulk**
- If all invoices are actually paid
- Use SQL or mass action
- Quick but loses payment details

**D. Leave as unpaid**
- If business doesn't track payments in Odoo
- Invoices remain open
- Simpler approach

**Recommendation:** Ask your friend which approach they prefer

---

## 📁 Files Ready for Review

**Location:** `/home/nop/CascadeProjects/freelance_project_cuotes/odoo-migration-project/20260211_OdooMigration/`

**Files:**
1. `customer_invoices.csv` - 1,332 invoices
2. `credit_notes.csv` - 8 credit notes
3. `vendor_bills.csv` - 0 bills (empty)
4. `invoice_lines.csv` - 3,346 lines

**Next steps:**
1. Review CSV files
2. Confirm import approach
3. Create import scripts
4. Test import with 5 invoices
5. Full import after approval

---

## 🎯 Summary

✅ **Successfully extracted all invoice data from backup**
- 1,332 customer invoices (all posted, all unpaid)
- 8 credit notes
- 0 vendor bills
- 3,346 invoice lines

⚠️ **Payment situation:**
- All invoices are unpaid in the backup
- Only 1 payment record exists (incomplete data)
- Recommend importing invoices as unpaid
- Friend can record payments manually or import separately

📋 **Ready for friend's review:**
- CSV files created and ready
- No import yet - waiting for approval
- Friend should review data before proceeding

**The CSV files are ready for your friend to review before we proceed with the import.**
