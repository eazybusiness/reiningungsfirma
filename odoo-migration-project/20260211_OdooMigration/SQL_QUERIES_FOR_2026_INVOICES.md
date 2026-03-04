# SQL Queries to Extract 2026 Invoices

## 📋 Instructions 

These SQL queries will extract all 2026 invoice data from the PostgreSQL backup, including headers, lines, and notes.

---

## 🔧 Prerequisites

1. **Restore the backup to PostgreSQL:**
   ```bash
   createdb odoo_backup_2026
   pg_restore -d odoo_backup_2026 /path/to/backup.dump
   ```

2. **Connect to the database:**
   ```bash
   psql -d odoo_backup_2026
   ```

---

## 📄 Query 1: Customer Invoice Headers (2026)

This query extracts all customer invoice headers for 2026.

```sql
COPY (
    SELECT 
        am.name as "Invoice Number",
        am.invoice_date as "Invoice Date",
        am.invoice_date_due as "Due Date",
        rp.name as "Customer Name",
        rp.vat as "Customer VAT",
        rp.email as "Customer Email",
        am.state as "State",
        am.payment_state as "Payment State",
        am.amount_untaxed as "Amount Untaxed",
        am.amount_tax as "Amount Tax",
        am.amount_total as "Amount Total",
        am.amount_residual as "Amount Residual",
        apt.name as "Payment Term",
        am.ref as "Reference",
        am.invoice_origin as "Origin",
        rc.name as "Currency",
        am.narration as "Notes"
    FROM account_move am
    LEFT JOIN res_partner rp ON am.partner_id = rp.id
    LEFT JOIN account_payment_term apt ON am.invoice_payment_term_id = apt.id
    LEFT JOIN res_currency rc ON am.currency_id = rc.id
    WHERE am.move_type = 'out_invoice'
        AND EXTRACT(YEAR FROM am.invoice_date) = 2026
    ORDER BY am.invoice_date, am.name
) TO '/tmp/customer_invoices_2026.csv' WITH CSV HEADER;
```

**Output file:** `/tmp/customer_invoices_2026.csv`

---

## 📄 Query 2: Invoice Lines (2026) - Product Lines Only

This query extracts product/service lines from 2026 invoices.

```sql
COPY (
    SELECT 
        am.name as "Invoice Number",
        CASE 
            WHEN aml.display_type IS NULL OR aml.display_type = 'product' THEN 'product'
            ELSE aml.display_type
        END as "Type",
        pp.default_code as "Product Code",
        pt.name as "Product Name",
        aml.name as "Description",
        aml.quantity as "Quantity",
        aml.price_unit as "Unit Price",
        aml.price_subtotal as "Subtotal",
        aml.price_total as "Total",
        string_agg(at.name, ', ') as "Taxes"
    FROM account_move_line aml
    JOIN account_move am ON aml.move_id = am.id
    LEFT JOIN product_product pp ON aml.product_id = pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
    LEFT JOIN account_move_line_account_tax_rel amlat ON aml.id = amlat.account_move_line_id
    LEFT JOIN account_tax at ON amlat.account_tax_id = at.id
    WHERE am.move_type = 'out_invoice'
        AND EXTRACT(YEAR FROM am.invoice_date) = 2026
        AND (aml.display_type IS NULL OR aml.display_type = 'product')
        AND aml.exclude_from_invoice_tab = false
    GROUP BY am.name, aml.id, pp.default_code, pt.name, aml.name, 
             aml.quantity, aml.price_unit, aml.price_subtotal, 
             aml.price_total, aml.display_type
    ORDER BY am.name, aml.sequence
) TO '/tmp/invoice_lines_2026.csv' WITH CSV HEADER;
```

**Output file:** `/tmp/invoice_lines_2026.csv`

---

## 📄 Query 3: Invoice Note Lines (2026)

This query extracts note lines (important course details, participant names, etc.) from 2026 invoices.

```sql
COPY (
    SELECT 
        am.name as "Invoice Number",
        aml.sequence as "Sequence",
        aml.name as "Note Text",
        aml.display_type as "Display Type"
    FROM account_move_line aml
    JOIN account_move am ON aml.move_id = am.id
    WHERE am.move_type = 'out_invoice'
        AND EXTRACT(YEAR FROM am.invoice_date) = 2026
        AND aml.display_type = 'line_note'
    ORDER BY am.name, aml.sequence
) TO '/tmp/invoice_note_lines_2026.csv' WITH CSV HEADER;
```

**Output file:** `/tmp/invoice_note_lines_2026.csv`

---

## 📄 Query 4: Credit Notes (2026)

This query extracts credit notes for 2026.

```sql
COPY (
    SELECT 
        am.name as "Credit Note Number",
        am.invoice_date as "Date",
        am.invoice_date_due as "Due Date",
        rp.name as "Customer Name",
        rp.vat as "Customer VAT",
        rp.email as "Customer Email",
        am.state as "State",
        am.payment_state as "Payment State",
        am.amount_untaxed as "Amount Untaxed",
        am.amount_tax as "Amount Tax",
        am.amount_total as "Amount Total",
        am.amount_residual as "Amount Residual",
        apt.name as "Payment Term",
        am.ref as "Reference",
        am.invoice_origin as "Origin",
        rc.name as "Currency",
        am.narration as "Notes"
    FROM account_move am
    LEFT JOIN res_partner rp ON am.partner_id = rp.id
    LEFT JOIN account_payment_term apt ON am.invoice_payment_term_id = apt.id
    LEFT JOIN res_currency rc ON am.currency_id = rc.id
    WHERE am.move_type = 'out_refund'
        AND EXTRACT(YEAR FROM am.invoice_date) = 2026
    ORDER BY am.invoice_date, am.name
) TO '/tmp/credit_notes_2026.csv' WITH CSV HEADER;
```

**Output file:** `/tmp/credit_notes_2026.csv`

---

## 📄 Query 5: Vendor Bills (2026)

This query extracts vendor bills for 2026.

```sql
COPY (
    SELECT 
        am.name as "Bill Number",
        am.invoice_date as "Bill Date",
        am.invoice_date_due as "Due Date",
        rp.name as "Vendor Name",
        rp.vat as "Vendor VAT",
        rp.email as "Vendor Email",
        am.state as "State",
        am.payment_state as "Payment State",
        am.amount_untaxed as "Amount Untaxed",
        am.amount_tax as "Amount Tax",
        am.amount_total as "Amount Total",
        am.amount_residual as "Amount Residual",
        apt.name as "Payment Term",
        am.ref as "Reference",
        am.invoice_origin as "Origin",
        rc.name as "Currency",
        am.narration as "Notes"
    FROM account_move am
    LEFT JOIN res_partner rp ON am.partner_id = rp.id
    LEFT JOIN account_payment_term apt ON am.invoice_payment_term_id = apt.id
    LEFT JOIN res_currency rc ON am.currency_id = rc.id
    WHERE am.move_type = 'in_invoice'
        AND EXTRACT(YEAR FROM am.invoice_date) = 2026
    ORDER BY am.invoice_date, am.name
) TO '/tmp/vendor_bills_2026.csv' WITH CSV HEADER;
```

**Output file:** `/tmp/vendor_bills_2026.csv`

---

## 🚀 Quick Start Script

You can create a shell script to run all queries at once:

**File: `extract_2026_invoices.sh`**

```bash
#!/bin/bash

# Database name
DB_NAME="odoo_backup_2026"

echo "Extracting 2026 invoice data..."

# Extract customer invoices
echo "1. Extracting customer invoice headers..."
psql -d $DB_NAME -c "
COPY (
    SELECT 
        am.name as \"Invoice Number\",
        am.invoice_date as \"Invoice Date\",
        am.invoice_date_due as \"Due Date\",
        rp.name as \"Customer Name\",
        rp.vat as \"Customer VAT\",
        rp.email as \"Customer Email\",
        am.state as \"State\",
        am.payment_state as \"Payment State\",
        am.amount_untaxed as \"Amount Untaxed\",
        am.amount_tax as \"Amount Tax\",
        am.amount_total as \"Amount Total\",
        am.amount_residual as \"Amount Residual\",
        apt.name as \"Payment Term\",
        am.ref as \"Reference\",
        am.invoice_origin as \"Origin\",
        rc.name as \"Currency\",
        am.narration as \"Notes\"
    FROM account_move am
    LEFT JOIN res_partner rp ON am.partner_id = rp.id
    LEFT JOIN account_payment_term apt ON am.invoice_payment_term_id = apt.id
    LEFT JOIN res_currency rc ON am.currency_id = rc.id
    WHERE am.move_type = 'out_invoice'
        AND EXTRACT(YEAR FROM am.invoice_date) = 2026
    ORDER BY am.invoice_date, am.name
) TO '/tmp/customer_invoices_2026.csv' WITH CSV HEADER;
"

# Extract invoice lines
echo "2. Extracting invoice lines..."
psql -d $DB_NAME -c "
COPY (
    SELECT 
        am.name as \"Invoice Number\",
        CASE 
            WHEN aml.display_type IS NULL OR aml.display_type = 'product' THEN 'product'
            ELSE aml.display_type
        END as \"Type\",
        pp.default_code as \"Product Code\",
        pt.name as \"Product Name\",
        aml.name as \"Description\",
        aml.quantity as \"Quantity\",
        aml.price_unit as \"Unit Price\",
        aml.price_subtotal as \"Subtotal\",
        aml.price_total as \"Total\",
        string_agg(at.name, ', ') as \"Taxes\"
    FROM account_move_line aml
    JOIN account_move am ON aml.move_id = am.id
    LEFT JOIN product_product pp ON aml.product_id = pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
    LEFT JOIN account_move_line_account_tax_rel amlat ON aml.id = amlat.account_move_line_id
    LEFT JOIN account_tax at ON amlat.account_tax_id = at.id
    WHERE am.move_type = 'out_invoice'
        AND EXTRACT(YEAR FROM am.invoice_date) = 2026
        AND (aml.display_type IS NULL OR aml.display_type = 'product')
        AND aml.exclude_from_invoice_tab = false
    GROUP BY am.name, aml.id, pp.default_code, pt.name, aml.name, 
             aml.quantity, aml.price_unit, aml.price_subtotal, 
             aml.price_total, aml.display_type
    ORDER BY am.name, aml.sequence
) TO '/tmp/invoice_lines_2026.csv' WITH CSV HEADER;
"

# Extract note lines
echo "3. Extracting invoice note lines..."
psql -d $DB_NAME -c "
COPY (
    SELECT 
        am.name as \"Invoice Number\",
        aml.sequence as \"Sequence\",
        aml.name as \"Note Text\",
        aml.display_type as \"Display Type\"
    FROM account_move_line aml
    JOIN account_move am ON aml.move_id = am.id
    WHERE am.move_type = 'out_invoice'
        AND EXTRACT(YEAR FROM am.invoice_date) = 2026
        AND aml.display_type = 'line_note'
    ORDER BY am.name, aml.sequence
) TO '/tmp/invoice_note_lines_2026.csv' WITH CSV HEADER;
"

# Extract credit notes
echo "4. Extracting credit notes..."
psql -d $DB_NAME -c "
COPY (
    SELECT 
        am.name as \"Credit Note Number\",
        am.invoice_date as \"Date\",
        am.invoice_date_due as \"Due Date\",
        rp.name as \"Customer Name\",
        rp.vat as \"Customer VAT\",
        rp.email as \"Customer Email\",
        am.state as \"State\",
        am.payment_state as \"Payment State\",
        am.amount_untaxed as \"Amount Untaxed\",
        am.amount_tax as \"Amount Tax\",
        am.amount_total as \"Amount Total\",
        am.amount_residual as \"Amount Residual\",
        apt.name as \"Payment Term\",
        am.ref as \"Reference\",
        am.invoice_origin as \"Origin\",
        rc.name as \"Currency\",
        am.narration as \"Notes\"
    FROM account_move am
    LEFT JOIN res_partner rp ON am.partner_id = rp.id
    LEFT JOIN account_payment_term apt ON am.invoice_payment_term_id = apt.id
    LEFT JOIN res_currency rc ON am.currency_id = rc.id
    WHERE am.move_type = 'out_refund'
        AND EXTRACT(YEAR FROM am.invoice_date) = 2026
    ORDER BY am.invoice_date, am.name
) TO '/tmp/credit_notes_2026.csv' WITH CSV HEADER;
"

echo ""
echo "✅ Extraction complete!"
echo ""
echo "Files created in /tmp/:"
echo "  - customer_invoices_2026.csv"
echo "  - invoice_lines_2026.csv"
echo "  - invoice_note_lines_2026.csv"
echo "  - credit_notes_2026.csv"
echo ""
echo "You can now import these files to Odoo Online."
```

**Usage:**
```bash
chmod +x extract_2026_invoices.sh
./extract_2026_invoices.sh
```

---

## 📊 Expected Output

After running the queries, you will have these CSV files:

1. **customer_invoices_2026.csv** - Invoice headers
2. **invoice_lines_2026.csv** - Product/service lines
3. **invoice_note_lines_2026.csv** - Note lines (course details, participants)
4. **credit_notes_2026.csv** - Credit notes
5. **vendor_bills_2026.csv** - Vendor bills (if any)

---

## ⚠️ Important Notes

### File Permissions
The PostgreSQL user must have write permissions to `/tmp/`. If not, change the output path:
```sql
TO '/home/username/invoices_2026.csv' WITH CSV HEADER;
```

### Character Encoding
If you encounter encoding issues, add encoding specification:
```sql
TO '/tmp/customer_invoices_2026.csv' WITH CSV HEADER ENCODING 'UTF8';
```

### Large Files
For very large datasets, consider adding a limit for testing:
```sql
WHERE am.move_type = 'out_invoice'
    AND EXTRACT(YEAR FROM am.invoice_date) = 2026
LIMIT 100  -- Test with 100 records first
```

---

## 🔍 Verification Queries

Before extracting, you can check the data:

**Count 2026 invoices:**
```sql
SELECT COUNT(*) 
FROM account_move 
WHERE move_type = 'out_invoice' 
    AND EXTRACT(YEAR FROM invoice_date) = 2026;
```

**Count 2026 invoice lines:**
```sql
SELECT COUNT(*) 
FROM account_move_line aml
JOIN account_move am ON aml.move_id = am.id
WHERE am.move_type = 'out_invoice' 
    AND EXTRACT(YEAR FROM am.invoice_date) = 2026
    AND (aml.display_type IS NULL OR aml.display_type = 'product')
    AND aml.exclude_from_invoice_tab = false;
```

**Count 2026 note lines:**
```sql
SELECT COUNT(*) 
FROM account_move_line aml
JOIN account_move am ON aml.move_id = am.id
WHERE am.move_type = 'out_invoice' 
    AND EXTRACT(YEAR FROM am.invoice_date) = 2026
    AND aml.display_type = 'line_note';
```

---

## 📞 Support

If you encounter any issues:
1. Check PostgreSQL logs: `tail -f /var/log/postgresql/postgresql-*.log`
2. Verify database connection: `psql -d odoo_backup_2026 -c "SELECT version();"`
3. Check file permissions: `ls -la /tmp/`

**The queries are ready to use - just copy and paste into psql or the shell script!**
