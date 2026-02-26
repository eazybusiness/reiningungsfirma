#!/usr/bin/env python3
"""
Analyze the Odoo backup to count invoices and payments
"""

import re
import sys

backup_file = '../odoo_backup/dump.sql'

print("="*80)
print("ANALYZING ODOO BACKUP FOR INVOICES AND PAYMENTS")
print("="*80 + "\n")

# Count account_move records (invoices)
print("Counting invoices (account_move)...")
in_account_move = False
invoice_count = 0

with open(backup_file, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if 'COPY public.account_move' in line:
            in_account_move = True
            print(f"Found account_move table")
            continue
        
        if in_account_move:
            if line.strip() == '\\.':
                in_account_move = False
                break
            invoice_count += 1

print(f"✅ Total account_move records: {invoice_count}")

# Count account_move_line records (invoice lines)
print("\nCounting invoice lines (account_move_line)...")
in_account_move_line = False
line_count = 0

with open(backup_file, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if 'COPY public.account_move_line' in line:
            in_account_move_line = True
            print(f"Found account_move_line table")
            continue
        
        if in_account_move_line:
            if line.strip() == '\\.':
                in_account_move_line = False
                break
            line_count += 1

print(f"✅ Total account_move_line records: {line_count}")

# Count account_payment records
print("\nCounting payments (account_payment)...")
in_account_payment = False
payment_count = 0

with open(backup_file, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if 'COPY public.account_payment' in line:
            in_account_payment = True
            print(f"Found account_payment table")
            continue
        
        if in_account_payment:
            if line.strip() == '\\.':
                in_account_payment = False
                break
            payment_count += 1

print(f"✅ Total account_payment records: {payment_count}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Invoices (account_move): {invoice_count}")
print(f"Invoice lines (account_move_line): {line_count}")
print(f"Payments (account_payment): {payment_count}")
print()

if invoice_count > 0:
    print("✅ Backup contains invoice data - we can extract and import it!")
else:
    print("⚠️  No invoices found in backup")
