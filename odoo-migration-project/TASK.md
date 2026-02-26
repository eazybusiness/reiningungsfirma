# Tasks - Odoo Migration Project Analysis

## Active Tasks
- [ ] Friend to test subscription creation in UI - 2026-02-26
- [ ] Friend to validate pricelist pricing on subscription - 2026-02-26
- [ ] Friend to test invoice generation from subscription - 2026-02-26
- [ ] Friend to verify IBAN/SEPA data visibility in UI - 2026-02-26
- [ ] Friend to test full subscription → invoice → payment workflow - 2026-02-26

## Completed Tasks
- [x] Research Odoo Community → Online migration best practices - 2025-02-24
- [x] Analyze VeriFactu requirements for Spain - 2025-02-24
- [x] Create 3-step migration procedure - 2025-02-24
- [x] Break down time estimates per phase - 2025-02-24
- [x] Calculate total project hours and budget - 2025-02-24
- [x] Document approach and recommendations - 2025-02-24
- [x] Analyze pricelist rules CSV data structure - 2025-02-24
- [x] Identify pricelist import issue (field mapping problem) - 2025-02-24
- [x] Create CSV converter script for external IDs - 2025-02-24
- [x] Create API import script for pricelist rules - 2025-02-24
- [x] Document 3 import methods with step-by-step instructions - 2025-02-24
- [x] Diagnose root cause: products missing Internal Reference field - 2026-02-25
- [x] Create fix_product_internal_references.py script - 2026-02-25
- [x] Create verify_products.py validation script - 2026-02-25
- [x] Create import_pricelist_rules_fixed.py with proper matching - 2026-02-25
- [x] Create comprehensive execution guide - 2026-02-25
- [x] Fix CSV encoding issue in product import script - 2026-02-25
- [x] Create fix_products_by_id.py for direct ID mapping - 2026-02-25
- [x] Successfully set Internal References for 22 products - 2026-02-25
- [x] Fix parse_external_id function for pricelist vs product naming - 2026-02-25
- [x] Fix applied_on field issue in pricelist items - 2026-02-25
- [x] Successfully import 102 pricelist rules to Odoo Online - 2026-02-25
- [x] Diagnose missing customer data (0 customers in Odoo) - 2026-02-25
- [x] Fix product categories for 19 products - 2026-02-25
- [x] Create and run import_customers.py script - 2026-02-25
- [x] Successfully import 98 customers with pricelists and bank accounts - 2026-02-25
- [x] Create comprehensive debugging summary documentation - 2026-02-25
- [x] Identify and remove 6 duplicate customers - 2026-02-25
- [x] Identify and remove 10 duplicate pricelist items - 2026-02-25
- [x] Investigate LP_ADVLEGAL pricelist (no rules in source CSV) - 2026-02-25
- [x] Fix missing internal reference for "Booking Fees" product - 2026-02-26
- [x] Verify all completion criteria programmatically - 2026-02-26
- [x] Create completion criteria status report - 2026-02-26

## Discovered During Work
- VeriFactu is a Spanish tax compliance requirement (2025) requiring digital signatures and hash chains for invoices
- Odoo Community → Enterprise migration cannot use direct database migration (different structures)
- Client's 10-20 hour budget is tight but achievable for experienced specialist at upper limit (18-20 hours)
- Outlook 365 integration requires Azure AD app registration (may need client involvement)
- Project requires specialist expertise: migration experience, VeriFactu knowledge, Odoo Online familiarity
- Pricelist rules CSV uses human-readable names (LP_ACORDIA, SRV-MANT-RGPD) but Odoo needs database/external IDs
- 104 pricelist rules need to be imported across 70 pricelists
- Products use Product ID as Internal Reference (e.g., SRV-MANT-RGPD-LSSI)
- Date format in CSV is MM/DD/YYYY, Odoo needs YYYY-MM-DD
- **CRITICAL:** Products were imported WITHOUT Internal Reference field (default_code) - this is why pricelist rules failed
- Odoo Online interface is in Spanish: "Referencia interna" = Internal Reference, "Tarifas" = Pricelists
- Cannot import pricelist rules via UI when multiple pricelists selected - must use API or import per pricelist
- Backup option not readily available in Odoo Online standard - need to use manual data exports or Odoo.sh
