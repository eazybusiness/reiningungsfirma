#!/usr/bin/env python3
"""
Investigate why there's only 1 payment record but 1332 invoices
"""

import psycopg2

DB_NAME = 'odoo_backup_analysis'

print("="*80)
print("INVESTIGATING PAYMENT SITUATION")
print("="*80 + "\n")

conn = psycopg2.connect(dbname=DB_NAME)
cur = conn.cursor()

# Check payment states
print("1. Invoice payment states:")
cur.execute("""
SELECT 
    payment_state,
    COUNT(*) as count,
    SUM(amount_total) as total_amount
FROM account_move
WHERE move_type = 'out_invoice'
GROUP BY payment_state
ORDER BY count DESC;
""")

for row in cur.fetchall():
    print(f"   {row[0]:15} {row[1]:5} invoices  €{row[2]:,.2f}")

# Check the single payment record
print("\n2. The single payment record:")
cur.execute("""
SELECT 
    id, name, date, amount, state, payment_type, partner_id
FROM account_payment
LIMIT 5;
""")

for row in cur.fetchall():
    print(f"   ID: {row[0]}, Name: {row[1]}, Date: {row[2]}, Amount: €{row[3]}, State: {row[4]}, Type: {row[5]}")

# Check if payments are recorded differently (in account_move)
print("\n3. Checking for payment entries in account_move:")
cur.execute("""
SELECT 
    move_type,
    COUNT(*) as count
FROM account_move
WHERE move_type LIKE '%payment%' OR move_type = 'entry'
GROUP BY move_type
ORDER BY count DESC;
""")

payment_moves = cur.fetchall()
if payment_moves:
    for row in payment_moves:
        print(f"   {row[0]:20} {row[1]:5} records")
else:
    print("   No payment-type moves found")

# Check reconciliation - are invoices marked as paid through reconciliation?
print("\n4. Checking invoice reconciliation:")
cur.execute("""
SELECT 
    COUNT(DISTINCT am.id) as reconciled_invoices
FROM account_move am
JOIN account_move_line aml ON am.id = aml.move_id
WHERE am.move_type = 'out_invoice'
  AND aml.reconciled = true;
""")

reconciled = cur.fetchone()[0]
print(f"   Invoices with reconciled lines: {reconciled}")

# Check if payment_state = 'paid' but no payment records
print("\n5. Invoices marked as 'paid' in payment_state:")
cur.execute("""
SELECT 
    name, invoice_date, partner_id, amount_total, payment_state
FROM account_move
WHERE move_type = 'out_invoice'
  AND payment_state = 'paid'
LIMIT 5;
""")

paid_invoices = cur.fetchall()
if paid_invoices:
    print(f"   Found {len(paid_invoices)} paid invoices (showing first 5):")
    for row in paid_invoices:
        print(f"   {row[0]:20} {row[1]}  €{row[3]:,.2f}  State: {row[4]}")
else:
    print("   No invoices with payment_state = 'paid'")

# Summary
print("\n" + "="*80)
print("ANALYSIS")
print("="*80)

cur.execute("""
SELECT 
    COUNT(*) as total_invoices,
    SUM(CASE WHEN payment_state = 'paid' THEN 1 ELSE 0 END) as paid_count,
    SUM(CASE WHEN payment_state = 'not_paid' THEN 1 ELSE 0 END) as unpaid_count,
    SUM(CASE WHEN payment_state = 'in_payment' THEN 1 ELSE 0 END) as in_payment_count,
    SUM(CASE WHEN payment_state = 'partial' THEN 1 ELSE 0 END) as partial_count,
    SUM(amount_total) as total_invoiced,
    SUM(amount_residual) as total_unpaid
FROM account_move
WHERE move_type = 'out_invoice';
""")

stats = cur.fetchone()
print(f"\nTotal invoices: {stats[0]}")
print(f"Paid: {stats[1]} ({stats[1]/stats[0]*100:.1f}%)")
print(f"Unpaid: {stats[2]} ({stats[2]/stats[0]*100:.1f}%)")
print(f"In payment: {stats[3]}")
print(f"Partial: {stats[4]}")
print(f"\nTotal invoiced: €{stats[5]:,.2f}")
print(f"Total unpaid (residual): €{stats[6]:,.2f}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)

if stats[1] == 0:
    print("\n⚠️  ALL INVOICES ARE UNPAID")
    print("\nPossible reasons:")
    print("1. This is a test/demo database with no real payments")
    print("2. Payments are recorded in a different system")
    print("3. Business operates on credit/invoicing without immediate payment")
    print("4. Payment data was not included in this backup")
    print("\nRecommendation:")
    print("- Import invoices as 'posted' (validated) but 'unpaid'")
    print("- Payments can be recorded manually in new system as they occur")
    print("- Or import payment data separately if available")
else:
    print(f"\n{stats[1]} invoices are marked as paid")
    print(f"But only 1 payment record exists in account_payment table")
    print("\nThis suggests:")
    print("- Payments may be recorded differently (bank reconciliation)")
    print("- Or payment records were not exported in this backup")

cur.close()
conn.close()
