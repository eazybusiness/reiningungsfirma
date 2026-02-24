# Migration Procedure - 3-Step Approach

## Overview
This document outlines the exact procedure for migrating from Odoo Community to Odoo Online Enterprise Standard, including data migration, module configuration, and user onboarding.

---

## STEP 1: DATA MIGRATION & VALIDATION (4-5 hours)

### Phase 1.1: Pre-Migration Preparation (1 hour)
**Actions**:
1. **Full backup of Odoo Community database**
   - Export complete PostgreSQL backup
   - Document current module versions
   - Screenshot current invoice sequences and numbering

2. **Data audit in Community**
   - Count total clients, invoices, products
   - Identify data quality issues (duplicates, missing fields)
   - Document custom fields or modifications

3. **Prepare Odoo Online instance**
   - Client creates Odoo Online Enterprise Standard account
   - Grant temporary admin access (5-7 days)
   - Install Spanish localization module

**Deliverables**:
- Complete Community backup file
- Data inventory spreadsheet
- Clean Odoo Online instance ready for import

---

### Phase 1.2: Data Export from Community (1 hour)
**Actions**:
1. **Export Clients (Contacts)**
   - Navigate to Contacts → Export
   - Fields to include:
     - Name, VAT/NIF, Address, Email, Phone
     - Payment terms, Customer/Supplier flags
     - Tags, Categories
   - Export as CSV (UTF-8 encoding)

2. **Export Products/Services**
   - Navigate to Products → Export
   - Fields: Name, Internal Reference, Sale Price, Cost, Taxes
   - Export as CSV

3. **Export Invoices**
   - Navigate to Invoicing → Customer Invoices → Export
   - **Critical fields**:
     - Invoice Number, Date, Due Date
     - Customer (by ID or VAT)
     - Invoice Lines (Product, Quantity, Price, Tax)
     - Payment Status, Payment Terms
     - Total Amount, Tax Amount
   - Export as CSV (one file for headers, one for lines)

4. **Export Invoice Payments**
   - Navigate to Accounting → Payments → Export
   - Link to invoice numbers
   - Export as CSV

**Deliverables**:
- `clients.csv`
- `products.csv`
- `invoices_header.csv`
- `invoices_lines.csv`
- `payments.csv`

---

### Phase 1.3: Data Import to Odoo Online (2 hours)
**Actions**:
1. **Import Clients first** (foundation data)
   - Odoo Online → Contacts → Import
   - Map CSV columns to Odoo fields
   - Enable "Create if doesn't exist" for related fields
   - Import in batches of 100 records
   - **Validation**: Check total count matches Community

2. **Import Products/Services**
   - Sales → Products → Import
   - Map fields, set default taxes
   - **Validation**: Verify pricing and tax configuration

3. **Import Invoices (most critical)**
   - **Method A: CSV Import** (for simple invoices)
     - Accounting → Customers → Invoices → Import
     - Map invoice headers first
     - Then import invoice lines (linked by invoice number)
   
   - **Method B: API Script** (if CSV fails or complex data)
     - Use Odoo XML-RPC API
     - Python script to create invoices programmatically
     - Preserves relationships and validation

   - **Critical**: Preserve original invoice numbers and dates
   - Set invoices to "Posted" status (not draft)
   - Link to correct customers via VAT/NIF matching

4. **Import Payments**
   - Link payments to invoices
   - Reconcile paid invoices

**Validation Checkpoints**:
✅ Client count: Community = Online  
✅ Invoice count: Community = Online  
✅ Invoice totals: Sum matches between systems  
✅ Invoice sequences: 2024, 2025, 2026 numbering preserved  
✅ Payment status: Paid invoices show as paid  
✅ Tax calculations: Amounts match original invoices  

**Deliverables**:
- All data imported to Odoo Online
- Validation report (counts, totals, discrepancies)
- List of any issues requiring manual correction

---

### Phase 1.4: VeriFactu Compliance Setup (30 minutes)
**Actions**:
1. **Configure Spanish fiscal data**
   - Settings → Companies → Edit company
   - Set VAT/NIF correctly
   - Configure fiscal position (Spain)

2. **VeriFactu module activation**
   - Apps → Search "VeriFactu" → Install
   - Configure digital certificate (if required by client)
   - Set invoice hash chain parameters

3. **Test VeriFactu on new invoice**
   - Create test invoice (2026 date)
   - Verify hash generation
   - Check compliance indicators

**Note**: Historical invoices (2024-2025) are migrated as-is. VeriFactu applies to new invoices from go-live date forward.

**Deliverables**:
- VeriFactu module configured
- Test invoice with valid hash
- Compliance documentation

---

## STEP 2: MODULE CONFIGURATION (8-10 hours)

### Phase 2.1: CRM Configuration (3-4 hours)

#### 2.1.1: Sales Pipeline Setup (1.5 hours)
**Actions**:
1. **Create custom pipeline stages**
   - CRM → Configuration → Stages
   - Create stages:
     - Lead (initial contact)
     - Qualification (needs assessment)
     - Proposal (quote sent)
     - Negotiation (discussing terms)
     - Won (closed deal)
     - Renewal (existing customer renewal)
   - Configure stage probabilities (0%, 25%, 50%, 75%, 100%, 90%)
   - Set automated actions per stage

2. **Configure sales teams**
   - Create team for VA
   - Set team leader (Admin)
   - Configure team targets/quotas (if needed)

3. **Customize opportunity form**
   - Add custom fields (if required):
     - Renewal date
     - Subscription type
     - Contract value
   - Configure required fields

**Deliverables**:
- Custom CRM pipeline with 6 stages
- Sales team configured
- Opportunity form customized

---

#### 2.1.2: Outlook 365 Integration (1.5-2 hours)
**Actions**:
1. **Azure AD App Registration** (client may need to do this)
   - Go to Azure Portal → App Registrations
   - Create new app: "Odoo CRM Integration"
   - Configure redirect URI: `https://[odoo-instance].odoo.com/microsoft_outlook/confirm`
   - Generate Client ID and Client Secret
   - Set API permissions:
     - Mail.Read
     - Mail.Send
     - Calendars.ReadWrite
     - Contacts.Read

2. **Odoo Outlook Connector Setup**
   - Settings → Integrations → Microsoft Outlook
   - Enter Client ID and Client Secret
   - Authorize connection
   - Test email sync

3. **Configure email sync for users**
   - Settings → Users → Admin/VA
   - Connect Outlook account
   - Configure sync settings:
     - Sync emails to CRM (create leads from emails)
     - Sync calendar (meetings → CRM activities)
     - Email templates for proposals

4. **Test integration**
   - Send test email from Outlook → Should appear in CRM
   - Create CRM activity → Should sync to Outlook calendar
   - Send email from CRM → Should send via Outlook

**Potential Issues**:
- OAuth authentication errors (Azure permissions)
- Email sync delays (check sync frequency)
- Duplicate contacts (configure merge rules)

**Deliverables**:
- Outlook 365 fully integrated
- Email sync working for Admin + VA
- Calendar sync functional
- Email templates configured

---

#### 2.1.3: CRM Automation (30 minutes)
**Actions**:
1. **Automated actions**
   - Lead assignment rules (round-robin to VA)
   - Email notifications on stage changes
   - Activity reminders (follow-up tasks)

2. **Email templates**
   - Proposal email template
   - Renewal reminder template
   - Welcome email for new clients

**Deliverables**:
- 3+ automated actions configured
- 3+ email templates ready

---

### Phase 2.2: Subscriptions Module Configuration (3-4 hours)

#### 2.2.1: Subscription Products Setup (1 hour)
**Actions**:
1. **Create subscription products**
   - Sales → Products → Create
   - Product type: Service
   - Enable "Recurring" checkbox
   - Configure:
     - Recurring period: Monthly
     - Recurring price
     - Taxes (IVA 21% for Spain)

2. **Create subscription templates**
   - Subscriptions → Configuration → Subscription Templates
   - Define:
     - Billing period (monthly)
     - Invoice generation timing (1st of month)
     - Payment terms (immediate, 15 days, 30 days)
     - Auto-renewal settings

3. **Configure subscription stages**
   - Draft → In Progress → To Renew → Closed
   - Set automated transitions

**Deliverables**:
- 3-5 subscription products configured
- Subscription templates ready
- Stages configured

---

#### 2.2.2: Recurring Invoice Automation (1.5 hours)
**Actions**:
1. **Configure invoice generation**
   - Subscriptions → Configuration → Settings
   - Set automatic invoice generation:
     - Frequency: Monthly
     - Generation date: 1st of month
     - Invoice date: Same as generation
     - Due date: Based on payment terms

2. **Set up automated workflows**
   - Create automated action: "Generate Monthly Invoices"
   - Trigger: Scheduled (daily check)
   - Action: Create invoices for active subscriptions
   - Send invoice email automatically

3. **Configure payment follow-up**
   - Accounting → Configuration → Follow-up Levels
   - Set reminder emails:
     - 7 days before due date
     - On due date
     - 7 days overdue
     - 15 days overdue

**Deliverables**:
- Automated monthly invoice generation
- Email automation for invoices
- Payment follow-up configured

---

#### 2.2.3: CRM → Subscription Integration (30 minutes)
**Actions**:
1. **Link CRM to Subscriptions**
   - When opportunity is "Won" → Create subscription automatically
   - Map opportunity fields to subscription:
     - Customer
     - Products/Services
     - Pricing
     - Start date

2. **Configure renewal workflow**
   - 30 days before subscription end → Create renewal opportunity in CRM
   - Assign to VA
   - Send renewal reminder email

**Deliverables**:
- CRM opportunities auto-create subscriptions
- Renewal workflow automated

---

#### 2.2.4: Testing Subscription Workflows (1 hour)
**Actions**:
1. **Create test subscription**
   - Add test customer
   - Create monthly subscription
   - Verify invoice generation

2. **Test full workflow**
   - CRM: Create opportunity → Mark as Won
   - Verify: Subscription created automatically
   - Wait/Force: Invoice generation
   - Check: Invoice sent via email
   - Verify: Payment follow-up emails

3. **Test renewal scenario**
   - Set subscription to expire in 30 days
   - Verify: Renewal opportunity created in CRM
   - Check: Reminder email sent

**Deliverables**:
- Complete workflow tested end-to-end
- Documentation of any issues
- Adjustments made based on testing

---

### Phase 2.3: Invoicing & VeriFactu Configuration (2-3 hours)

#### 2.3.1: Spanish Invoicing Setup (1 hour)
**Actions**:
1. **Configure Spanish taxes (IVA)**
   - Accounting → Configuration → Taxes
   - Create/verify tax rates:
     - IVA 21% (standard)
     - IVA 10% (reduced)
     - IVA 4% (super-reduced)
     - IVA 0% (exempt)
   - Set default tax on products

2. **Configure invoice sequences**
   - Accounting → Configuration → Journals → Sales
   - Set invoice sequence format: `FAC/2026/0001`
   - Ensure sequences continue from migrated data

3. **Configure payment terms**
   - Immediate payment
   - 15 days
   - 30 days
   - Custom terms (if needed)

4. **Invoice layout customization**
   - Settings → Companies → Document Layout
   - Add company logo
   - Configure invoice template (header, footer)
   - Add legal text (VeriFactu compliance notice)

**Deliverables**:
- Spanish tax configuration complete
- Invoice sequences properly configured
- Professional invoice template

---

#### 2.3.2: VeriFactu Advanced Configuration (1 hour)
**Actions**:
1. **Digital certificate setup** (if required)
   - Upload company digital certificate
   - Configure certificate password
   - Test certificate validity

2. **Configure VeriFactu parameters**
   - Invoice hash algorithm (SHA-256)
   - Chain validation rules
   - Signature format

3. **Test VeriFactu compliance**
   - Create test invoice
   - Verify hash generation
   - Check signature validity
   - Export VeriFactu XML report
   - Validate against tax authority requirements

**Deliverables**:
- VeriFactu fully configured and tested
- Sample compliant invoice
- Validation report

---

#### 2.3.3: Automated Invoice Workflows (1 hour)
**Actions**:
1. **CRM → Invoice automation**
   - When opportunity "Won" → Create invoice (or subscription)
   - Auto-send invoice via email
   - Track invoice status in CRM

2. **Subscription → Invoice automation**
   - Monthly invoice generation (already configured in 2.2.2)
   - Auto-send to customer
   - Update subscription status based on payment

3. **Payment reconciliation**
   - Configure bank feed (if applicable)
   - Set up automatic payment matching
   - Reconcile payments to invoices

4. **Configure invoice email template**
   - Professional email with invoice attached
   - Payment instructions
   - Company contact info

**Deliverables**:
- Complete invoice automation workflow
- Professional email templates
- Payment reconciliation configured

---

## STEP 3: USER ONBOARDING & HANDOVER (2-3 hours)

### Phase 3.1: User & Role Configuration (1 hour)

#### 3.1.1: Admin User Setup
**Actions**:
1. **Configure admin permissions**
   - Full access to all modules
   - API access enabled
   - Settings access

2. **Set up admin preferences**
   - Language: Spanish
   - Timezone: Europe/Madrid
   - Email notifications
   - Dashboard customization

#### 3.1.2: VA User Setup
**Actions**:
1. **Create VA user account**
   - Settings → Users → Create
   - Email: [VA email]
   - Access rights:
     - CRM: User (can create/edit leads, opportunities)
     - Subscriptions: User (can manage subscriptions)
     - Invoicing: User (view only, cannot edit posted invoices)
     - Contacts: User (can create/edit customers)

2. **Configure VA permissions**
   - Sales team assignment
   - Record rules (can only see own opportunities)
   - Email signature
   - Outlook integration

3. **Test VA access**
   - Login as VA
   - Verify can access CRM, Subscriptions
   - Verify cannot access Settings, Accounting (full)
   - Test creating opportunity → subscription → invoice flow

**Deliverables**:
- Admin user fully configured
- VA user created with correct permissions
- Access tested and validated

---

### Phase 3.2: API Access Configuration (30 minutes)
**Actions**:
1. **Generate API keys**
   - Settings → Users → Admin → API Keys
   - Create API key for automation scripts
   - Document API key securely

2. **Configure API permissions**
   - Set access scope (read/write for specific models)
   - Test API connection with simple script

3. **Provide API documentation**
   - Odoo API endpoint: `https://[instance].odoo.com/xmlrpc/2/`
   - Sample Python script for common operations:
     - Create invoice
     - Update subscription
     - Query customer data

**Deliverables**:
- API key generated and documented
- Sample API scripts provided
- API documentation for client

---

### Phase 3.3: Training & Documentation (1 hour)
**Actions**:
1. **Create user documentation**
   - **For Admin**:
     - How to manage users
     - How to configure new products
     - How to run reports
     - How to backup data
     - VeriFactu compliance checklist
   
   - **For VA**:
     - How to create leads in CRM
     - How to move opportunities through pipeline
     - How to create subscriptions
     - How to generate invoices
     - How to handle customer inquiries

2. **Screen sharing training session** (30 minutes)
   - Walk through CRM workflow
   - Demonstrate subscription creation
   - Show invoice generation
   - Answer questions

3. **Create quick reference guides**
   - CRM cheat sheet
   - Subscription management guide
   - Invoice troubleshooting

**Deliverables**:
- Complete user documentation (PDF)
- Training session completed
- Quick reference guides

---

### Phase 3.4: Final Validation & Go-Live (30 minutes)
**Actions**:
1. **Final data validation**
   - Re-check invoice counts and totals
   - Verify all customers migrated
   - Confirm VeriFactu compliance

2. **Go-live checklist**
   - [ ] All data migrated and validated
   - [ ] CRM pipeline configured and tested
   - [ ] Subscriptions generating invoices correctly
   - [ ] VeriFactu compliance verified
   - [ ] Outlook integration working
   - [ ] Users trained and comfortable
   - [ ] API access documented
   - [ ] Backup of Odoo Online created

3. **Post-migration support plan**
   - 7-day monitoring period
   - Quick response for critical issues
   - Optional: Ongoing support retainer

**Deliverables**:
- Go-live checklist completed
- Final validation report
- Post-migration support plan

---

## SUMMARY: 3-STEP MIGRATION PROCEDURE

### STEP 1: DATA MIGRATION (4-5 hours)
- Export data from Community (CSV)
- Import to Odoo Online (clients, products, invoices)
- Validate data integrity
- Configure VeriFactu basics

### STEP 2: MODULE CONFIGURATION (8-10 hours)
- CRM: Pipeline, Outlook integration, automation (3-4 hours)
- Subscriptions: Products, recurring invoices, workflows (3-4 hours)
- Invoicing: Spanish config, VeriFactu, automation (2-3 hours)

### STEP 3: USER ONBOARDING (2-3 hours)
- User roles and permissions (Admin + VA)
- API access setup
- Training and documentation
- Final validation and go-live

---

## TOTAL TIME ESTIMATE: 14-18 hours

**Breakdown**:
- Minimum (everything goes smoothly): 14 hours
- Realistic (normal troubleshooting): 16 hours
- Maximum (complex issues): 18 hours

**Buffer**: 2 hours for unexpected issues (within 10-20 hour range)

---

## RISK MITIGATION

### If Issues Arise
1. **Data import errors**: Use API method instead of CSV
2. **VeriFactu problems**: Consult Spanish Odoo community/documentation
3. **Outlook integration fails**: Use IMAP/SMTP as fallback
4. **Subscription workflow bugs**: Manual invoice generation as temporary solution

### Success Criteria
✅ All historical data migrated correctly  
✅ VeriFactu compliance verified  
✅ CRM pipeline operational  
✅ Subscriptions generating invoices automatically  
✅ Users trained and confident  
✅ Client satisfied with system
