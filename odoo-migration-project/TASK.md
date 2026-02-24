# Tasks - Odoo Migration Project Analysis

## Active Tasks
- [ ] Test pricelist rules import with one of the provided methods - 2025-02-24
- [ ] Validate product Internal References match Product IDs - 2025-02-24
- [ ] Configure bank accounts (IBAN/SEPA) - 2025-02-24
- [ ] Create test subscription and validate pricing - 2025-02-24

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
