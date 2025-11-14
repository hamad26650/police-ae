# Fraud Report Form - Complete Documentation 🔍

## Overview
A comprehensive fraud report form with conditional questions that dynamically appear based on user selections.

---

## Form Structure

### Section 1: Applicant Data (Always Required)
- Full Name
- National ID
- Phone Number
- Email
- Police Center
- Report Type

---

### Section 2: Fraud Details (When "Fraud" is selected)

#### Basic Information
1. **Detailed subject of the report** (required)
2. **Date and time of incident** (required)
3. **Location of incident** (required)
4. **Relationship with accused** (required)
5. **Type of agreement** (required)
   - Verbal
   - Written
   - Via social media

---

#### Financial Details
6. **Did the accused seize money?** (required)
   - Yes / No

**If "Yes":**
- **Total amount seized** (required)
- **Payment method** (required):
  - Bank transfer (shows: Bank name, Account/IBAN)
  - Wire transfer
  - Digital wallet
  - Receipt
  - Other (shows: text field for details)

**If "No":**
- **What item was seized?** (required)

---

#### Witnesses
7. **Are there witnesses?** (required)
   - Yes / No

**If "Yes":**
- **Witness details and contact numbers** (required)

---

#### Evidence
8. **Do you have proof?** (required)
   - Yes / No

**If "Yes":**
- **What evidence do you have?** (required)

---

#### Accused Party Information
9. **Party type** (required)
   - Person
   - Company
   - Unknown

**If "Person":**
- Name (required)
- Document type (optional)
- Nationality (optional)
- Phone (optional)
- Address (optional)

**If "Unknown":**
- Same fields as "Person" but not required
- At least name OR phone must be provided

**If "Company":**
- Company name (required)
- Phone (required)
- Address (required)

---

#### Additional Statements
10. **Any additional statements?** (optional)

---

## Smart Logic Implementation

### Conditional Display Rules

1. Report type = "الاحتيال" → Show all fraud questions
2. Money seized = "Yes" → Show amount + payment method fields
3. Money seized = "No" → Show seized item field
4. Payment method = "Bank transfer" → Show bank details
5. Payment method = "Other" → Show text field
6. Has witnesses = "Yes" → Show witness details field
7. Has evidence = "Yes" → Show evidence details field
8. Party type → Show relevant fields (person/company/unknown)

---

## Technical Implementation

### Files Modified

1. **`submit_report_form.html`**
   - Added all new form fields
   - Implemented conditional display logic in JavaScript
   - Added animations and visual enhancements

2. **`views.py`**
   - Updated `submit_report()` function
   - Extract all new fields from POST data
   - Build detailed text with all information
   - Store in `ServiceRequest.request_details`

---

## Data Storage Format

All information is stored in `request_details` field with structured formatting:

```
Report Type: Fraud

Subject: [details]

Date/Time: [datetime]
Location: [location]
Relationship: [relationship]
Agreement Type: [type]

Money Seized: Yes
Amount: [amount] AED
Payment Method: Bank Transfer
  - Bank Name: [name]
  - Account/IBAN: [number]

Witnesses: Yes
Witness Details: [details]

Evidence: Yes
Evidence Details: [details]

=== Accused Party Information ===
Party Type: Person
Name: [name]
Document Type: [type]
Nationality: [nationality]
Phone: [phone]
Address: [address]

=== Additional Statements ===
[statements]
```

---

## Features

✅ **Form Validation** - All required fields validated before submission
✅ **Responsive Design** - Works on all devices
✅ **Smooth Animations** - Professional UX with transitions
✅ **Icon-Enhanced** - Clear visual indicators for each field
✅ **Loading State** - Shows progress during submission
✅ **Smart Logic** - Fields appear/disappear based on selections

---

## Testing

Visit: `http://127.0.0.1:8000/submit-report/`

Test scenarios:
1. Select "الاحتيال" → All questions should appear
2. Money seized = "Yes" → Amount + payment fields appear
3. Money seized = "No" → Seized item field appears
4. Payment = "Bank transfer" → Bank details appear
5. Payment = "Other" → Text field appears
6. Try different party types (person/company/unknown)
7. Submit and verify success message

---

## Future Enhancements

To add other report types (slander, threat, etc.):
1. Create new section similar to `fraudQuestions`
2. Add required fields
3. Update JavaScript to show on selection
4. Update `views.py` to process data

---

**Status: ✅ Ready for Production**


