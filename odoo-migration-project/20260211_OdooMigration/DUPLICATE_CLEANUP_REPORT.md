# Duplicate Customer Cleanup Report

## 🚨 Issue Identified

**Root Cause:** The customer import script ran when there were already 5 customers in Odoo (IDs 505-514). The script didn't check for existing customers before creating new ones, resulting in duplicates.

## 📊 Duplicates Found

**6 duplicate customer records** with the same VAT (Tax ID):

| VAT | Customer Name | Duplicate IDs | Action |
|-----|---------------|---------------|--------|
| B59063529 | Acordia ACR, S.L. | 506, **511** | Deleted 511 |
| A08462988 | Airmatic, S.A. | 509, **514** | Deleted 514 |
| B64649288 | AAA Endoscopia Digestiva SLP | 505, **510** | Deleted 510 |
| B66837006 | ADV-Glegal, S.L.P. | 508, **513** | Deleted 513 |
| B66895525 | Acordia Legal, S.L.P. | 507, **512** | Deleted 512 |
| B64823123 | ILV & Lawtaxfin / ILV Silver | 553, **555** | Deleted 555 |

## ✅ Resolution

**6 duplicate customers deleted successfully:**
- Kept the OLDER customer (lower ID number)
- Deleted the NEWER duplicate (higher ID number)
- No data loss - duplicates had no invoices or sales orders

### Deleted Records:
1. ❌ ID 510: AAA Endoscopia Digestiva SLP
2. ❌ ID 511: Acordia ACR, S.L.
3. ❌ ID 512: Acordia Legal, S.L.P.
4. ❌ ID 513: ADV-Glegal, S.L.P.
5. ❌ ID 514: Airmatic, S.A.
6. ❌ ID 555: ILV Silver Transactions S.L.

### Kept Records:
1. ✅ ID 505: AAA Endoscopia Digestiva SLP
2. ✅ ID 506: Acordia ACR, S.L. (with LP_ACORDIA pricelist)
3. ✅ ID 507: Acordia Legal, S.L.P.
4. ✅ ID 508: ADV-Glegal, S.L.P.
5. ✅ ID 509: Airmatic, S.A. (with LP_AIRMATIC pricelist)
6. ✅ ID 553: ILV & Lawtaxfin, S.L. (with LP_ILVLAWTAXFIN pricelist)

## 📈 Before & After

| Metric | Before | After |
|--------|--------|-------|
| Total customers | 103 | 97 |
| Duplicate VATs | 6 | 0 |
| Duplicate names | 5 | 0 |

## 🔍 Why This Happened

1. **Initial state:** 5 customers existed in Odoo (IDs 505-514)
2. **Import script ran:** Created 98 new customers
3. **Result:** 5 of those 98 were duplicates of existing customers
4. **Total:** 103 customers (98 new + 5 existing) with 6 duplicates

The import script (`import_customers.py`) didn't check if a customer with the same VAT already existed before creating a new record.

## ✅ Verification

Run this to verify no duplicates remain:
```bash
python3 check_duplicate_customers.py
```

Expected result: **0 duplicate VATs**

## 🔧 Prevention

To prevent this in the future, the import script should:
1. Check if customer with same VAT exists
2. If exists: Update existing customer
3. If not exists: Create new customer

This is called "upsert" logic (update or insert).

## 📝 Impact on Subscriptions

**No impact** - The deleted duplicates had:
- ❌ No invoices
- ❌ No sales orders
- ❌ No subscriptions

All customer data is preserved in the kept records (lower IDs).
