# Setting Up Subscriptions in Odoo - Step by Step

## ✅ Current Status

**Subscriptions module:** Installed ✅  
**Products created:** 4 service products ✅  
**Configured for subscriptions:** 0 ❌

---

## 📋 Your Products

You have 4 service products:
1. **Booking Fees** - €50.00
2. **DUA VAT Valuation 10%** - €1.00
3. **DUA VAT Valuation 21%** - €1.00
4. **DUA VAT Valuation 4%** - €1.00

**None are configured for recurring billing yet.**

---

## 🎯 Next Steps to Create Subscriptions

### Step 1: Create Subscription Templates (Billing Frequencies)

Before configuring products, you need to create subscription templates that define billing frequencies.

**How to create templates:**

1. Go to **Subscriptions** → **Configuration** → **Subscription Templates**
2. Click **Create**
3. Create templates for different billing frequencies:

**Example templates to create:**

**Monthly Subscription:**
- Name: "Monthly Billing"
- Recurring Rule Type: Monthly
- Recurring Interval: 1
- Duration: Undefined (ongoing)

**Quarterly Subscription:**
- Name: "Quarterly Billing"
- Recurring Rule Type: Monthly
- Recurring Interval: 3
- Duration: Undefined

**Yearly Subscription:**
- Name: "Yearly Billing"
- Recurring Rule Type: Yearly
- Recurring Interval: 1
- Duration: Undefined

---

### Step 2: Configure Products for Subscriptions

Now configure which products should be recurring:

**For each product that should be recurring:**

1. Go to **Products** → **Products**
2. Open the product (e.g., "Booking Fees")
3. Edit the product
4. Enable **"Subscription Product"** checkbox
5. In the **Subscription Pricing** tab:
   - Click **Add a line**
   - Select subscription template (e.g., "Monthly Billing")
   - Set the price for that frequency
   - Add more lines for different frequencies if needed
6. Save

**Example configuration for "Booking Fees":**
- ✅ Subscription Product: Enabled
- Subscription Pricing:
  - Monthly Billing: €50.00/month
  - Yearly Billing: €500.00/year (discount for annual)

---

### Step 3: Create a Subscription for a Customer

Once products are configured:

1. Go to **Subscriptions** → **Subscriptions**
2. Click **Create**
3. Fill in:
   - **Customer:** Select the customer
   - **Subscription Template:** Select billing frequency (Monthly, Yearly, etc.)
   - **Start Date:** When subscription begins
   - **Next Invoice Date:** When first invoice should be generated
4. In **Subscription Lines** tab:
   - Click **Add a line**
   - Select your subscription product
   - Set quantity (usually 1)
   - Price will auto-fill from product
5. Click **Confirm**

**The subscription is now active!**

---

## 🔄 How Subscriptions Work

### Automatic Invoice Generation

Once a subscription is confirmed:
- Odoo automatically generates invoices based on the schedule
- Invoices are created on the "Next Invoice Date"
- After each invoice, the "Next Invoice Date" advances
- Customers receive invoices automatically

### Example Timeline

**Monthly subscription starting March 1:**
- March 1: Subscription created, first invoice generated
- April 1: Second invoice auto-generated
- May 1: Third invoice auto-generated
- And so on...

---

## 📊 Subscription Management

### View Active Subscriptions

**Subscriptions** → **Subscriptions**
- Filter by status (In Progress, Closed, etc.)
- See all customer subscriptions
- Track recurring revenue

### Subscription Actions

**Pause subscription:**
- Open subscription → Click "Close" → Select "Paused"

**Resume subscription:**
- Open paused subscription → Click "Set to In Progress"

**Cancel subscription:**
- Open subscription → Click "Close" → Select "Cancelled"

**Modify subscription:**
- Open subscription → Edit lines, prices, or frequency
- Changes apply to next invoice

---

## 💡 Recommended Setup for Your Business

Based on your products, here's what I recommend:

### Option 1: Training/Course Subscriptions

If you offer recurring training or courses:

**Create subscription product:**
- Name: "Monthly Training Program"
- Price: €50/month (or appropriate amount)
- Configure as subscription product
- Add to subscription templates

**Use case:**
- Customers subscribe for ongoing training
- Automatic monthly invoicing
- Easy to manage recurring students

### Option 2: Service Subscriptions

If you offer recurring services:

**Create subscription products for:**
- Monthly consulting: €X/month
- Quarterly reviews: €Y/quarter
- Annual support: €Z/year

### Option 3: Mixed Approach

- Some products recurring (ongoing services)
- Some products one-time (booking fees)
- Use subscriptions only for recurring items

---

## 🎯 Quick Start: Create Your First Subscription

**5-Minute Setup:**

1. **Create Monthly Template:**
   - Subscriptions → Configuration → Templates → Create
   - Name: "Monthly"
   - Type: Monthly, Interval: 1
   - Save

2. **Configure "Booking Fees" as Subscription:**
   - Products → Booking Fees → Edit
   - Enable "Subscription Product"
   - Add pricing: Monthly template, €50
   - Save

3. **Create Test Subscription:**
   - Subscriptions → Create
   - Select a customer
   - Template: Monthly
   - Add line: Booking Fees, Qty: 1
   - Confirm

4. **Check Result:**
   - Invoice should be generated automatically
   - Next invoice date set to next month
   - Subscription status: In Progress

---

## 📋 Checklist for Your Friend

Tell your friend to do this:

### Phase 1: Setup (10 minutes)
- [ ] Create subscription templates (Monthly, Quarterly, Yearly)
- [ ] Decide which products should be recurring
- [ ] Configure those products as subscription products
- [ ] Set pricing for each billing frequency

### Phase 2: Test (5 minutes)
- [ ] Create a test subscription for one customer
- [ ] Verify invoice is generated
- [ ] Check next invoice date is correct
- [ ] Confirm subscription shows as "In Progress"

### Phase 3: Production
- [ ] Create subscriptions for all recurring customers
- [ ] Set correct start dates and billing frequencies
- [ ] Verify all subscriptions are active
- [ ] Monitor automatic invoice generation

---

## 🔧 Can We Help from API?

**Yes!** Once templates and products are configured, I can create a script to:
- Bulk create subscriptions for multiple customers
- Import subscription data from CSV
- Automate subscription setup

**But first:** Your friend needs to:
1. Create at least one subscription template
2. Configure at least one product as subscription product

Then I can help automate the rest!

---

## ❓ Common Questions

**Q: Can I have different prices for different customers?**
A: Yes! When creating the subscription, you can override the price per line.

**Q: What if a customer wants to pause their subscription?**
A: Open the subscription and click "Close" → Select "Paused". Resume later with "Set to In Progress".

**Q: Can I change billing frequency mid-subscription?**
A: Yes, but it's better to close the old subscription and create a new one with the new frequency.

**Q: How do I handle failed payments?**
A: Odoo tracks unpaid invoices. You can set up payment reminders and follow-up actions.

**Q: Can customers manage their own subscriptions?**
A: Yes! Enable customer portal access. Customers can view and manage their subscriptions.

---

## 📞 Next Steps

**Tell your friend:**

1. **Go to Subscriptions → Configuration → Subscription Templates**
2. **Create at least one template** (e.g., "Monthly Billing")
3. **Go to Products → Select a product**
4. **Enable "Subscription Product" and add pricing**
5. **Then we can help create subscriptions in bulk if needed**

**Once they've done steps 1-4, let me know and I can:**
- Create a script to bulk-create subscriptions
- Import subscription data from CSV
- Automate the subscription setup process

---

**The key is: Templates first, then configure products, then create subscriptions!**
