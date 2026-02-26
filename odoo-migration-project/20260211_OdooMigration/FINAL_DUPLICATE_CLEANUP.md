# Final Duplicate Customer Cleanup Report

## 🚨 Problem Identified

Your friend was correct - there were **92 duplicate customer records** in Odoo, not just 6.

### Root Cause

The customer import script created duplicates because:
1. **5 customers already existed** in Odoo (IDs 408-504)
2. **Import script ran** and created 98 new customers (IDs 505-605)
3. **Result:** 92 customers had duplicate records with same VAT

### Why Previous Cleanup Missed Them

The first cleanup only removed 6 duplicates because it only searched for:
- Active customers (`customer_rank > 0`)

But the duplicates were:
- **Lower IDs (408-504):** `customer_rank = 0` (not marked as customers)
- **Higher IDs (505-605):** `customer_rank = 1` (marked as customers)

So the first cleanup didn't find the non-customer duplicates.

---

## 📊 Example: COMERGROUP

**URL:** `exartia.odoo.com/odoo/customers/531/res.partner/428`

**Explanation:**
- **531** = Current record being viewed (customer_rank = 1) ✅
- **428** = Duplicate record with same VAT (customer_rank = 0) ❌

**Both had VAT:** B60085867

**Odoo warning:** "Posibles duplicados: COMERGROUP SL (NIF)"

---

## ✅ Resolution

**Deleted 92 duplicate records:**

### Strategy:
- **Kept:** Records with `customer_rank > 0` (actual customers with pricelists)
- **Deleted:** Records with `customer_rank = 0` (duplicates without customer data)

### Sample deletions:
- ID 428: COMERGROUP, S.L. (kept ID 531)
- ID 408: Acordia Legal, S.L.P. (kept ID 507)
- ID 409: ADV-Glegal, S.L.P. (kept ID 508)
- ID 442: Evidentia Digital, S.L.U. (kept ID 545)
- ... and 88 more

---

## 📈 Before & After

| Metric | Before | After |
|--------|--------|-------|
| Total partners | 205 | 113 |
| Active customers | 97 | 97 |
| Duplicate VATs | 92 | 0 ✅ |
| Customer records kept | 97 | 97 |
| Non-customer duplicates deleted | 0 | 92 |

---

## ✅ Verification

All duplicates removed with **0 errors**.

Your friend should now:
1. Refresh the customer list in Odoo
2. Open any customer record
3. **No more duplicate warnings** should appear
4. All customer data (pricelists, bank accounts) preserved

---

## 🔍 Why This Happened

### Timeline:
1. **Initial state:** 5 customers existed in Odoo (IDs 408-504) without `customer_rank`
2. **Import ran:** Created 98 customers (IDs 505-605) with `customer_rank = 1`
3. **Result:** 92 overlapping VATs (5 existing + 92 from import = 97 unique)

### Import Script Issue:
The `import_customers.py` script didn't check:
```python
# Missing check:
existing = search_by_vat(vat)
if existing:
    update(existing)  # Should update
else:
    create(new)  # Should create
```

Instead it just created all records, causing duplicates.

---

## 📝 Current Status

**Database is now clean:**
- ✅ 97 unique customers
- ✅ All have pricelists assigned
- ✅ All have bank accounts (86 customers)
- ✅ No duplicate VAT warnings
- ✅ Ready for subscription workflow testing

---

## 🎯 Next Steps for Your Friend

1. **Verify in UI:**
   - Go to Clientes (Customers)
   - Open COMERGROUP, S.L.
   - **Should see NO duplicate warning**
   - Verify pricelist is assigned
   - Check bank account is visible

2. **Test subscription creation:**
   - Now that duplicates are gone
   - Create test subscription
   - Verify pricing from pricelist

3. **Report any remaining issues:**
   - All duplicates should be resolved
   - If any warnings persist, let us know

---

## 🔧 Prevention for Future Imports

To prevent this in future:
1. Always check for existing records by VAT before creating
2. Use "upsert" logic (update if exists, insert if not)
3. Test import on small dataset first
4. Verify no duplicates after import

---

## ✅ Summary

**Problem:** 92 duplicate customers with same VAT  
**Cause:** Import script didn't check for existing records  
**Solution:** Deleted all non-customer duplicates (customer_rank = 0)  
**Result:** 97 unique customers, 0 duplicates, all data preserved  

Your friend can now proceed with subscription workflow testing without duplicate warnings.
