# GST Status Fields Implementation for CFA Agreement Form

## Overview
This document describes the implementation of GST status fields with conditional logic in the CFA Agreement form, based on the SPO page requirements.

## New Fields Added

### 1. GST Status (Required)
- **Field Type**: Dropdown
- **Choices**: YES / NO
- **Validation**: Required field
- **Purpose**: Determines which additional fields are displayed

### 2. State Code (Conditional - shown when GST Status = YES)
- **Field Type**: Text Input
- **Format**: 2-digit number only
- **Max Length**: 2 characters
- **Validation**: Only allows digits 0-9
- **Pattern**: `[0-9]{2}` (00-99)

### 3. PAN Number (Conditional - shown when GST Status = YES)
- **Field Type**: Text Input
- **Format**: Standard PAN format (ABCDE1234F)
- **Max Length**: 10 characters
- **Validation**: PAN format validation
- **Pattern**: `[A-Z]{5}[0-9]{4}[A-Z]{1}`

### 4. Entity Code (Conditional - shown when GST Status = YES)
- **Field Type**: Text Input
- **Format**: 4 characters, letters or numbers only
- **Max Length**: 4 characters
- **Validation**: No special characters allowed
- **Pattern**: `[A-Za-z0-9]{4}`

### 5. Declaration/RCM (Conditional - shown when GST Status = NO)
- **Field Type**: Dropdown
- **Choices**: Declaration / RCM
- **Purpose**: Determines if declaration status field is shown

### 6. Declaration Status (Conditional - shown when Declaration/RCM = Declaration)
- **Field Type**: Dropdown
- **Choices**: Collected / Pending
- **Purpose**: Shows declaration status when Declaration is selected

## Conditional Logic Implementation

### When GST Status = YES:
1. Show State Code field
2. Show PAN Number field
3. Show Entity Code field
4. Hide Declaration/RCM and Declaration Status fields
5. Clear values in hidden fields

### When GST Status = NO:
1. Show Declaration/RCM field
2. Hide State Code, PAN Number, and Entity Code fields
3. Clear values in hidden fields

### When Declaration/RCM = Declaration:
1. Show Declaration Status field
2. Hide Declaration Status field when RCM is selected

### When Declaration/RCM = RCM:
1. Hide Declaration Status field
2. Clear Declaration Status value

## Technical Implementation

### Backend Changes
1. **Model Updates**: Added new fields to CFAAgreement model
2. **Form Updates**: Added form fields with proper validation
3. **Migration**: Created and applied database migration

### Frontend Changes
1. **Template Updates**: Added new form fields with conditional display
2. **JavaScript Logic**: Implemented conditional field visibility
3. **Field Validation**: Added real-time validation for new fields

### Validation Rules
1. **State Code**: Only 2 digits (00-99)
2. **PAN Number**: Standard PAN format (ABCDE1234F)
3. **Entity Code**: 4 characters, letters/numbers only, no special characters

## Files Modified

### 1. `dashboard/models.py`
- Added new GST status fields to CFAAgreement model

### 2. `dashboard/forms.py`
- Added form field definitions
- Added field choices and validation
- Updated form initialization

### 3. `dashboard/templates/dashboard/cfa_agreement_form.html`
- Added new form fields to template
- Implemented conditional field display
- Added JavaScript for field logic

### 4. `dashboard/migrations/0048_add_gst_status_fields.py`
- Database migration for new fields

## Usage Instructions

1. **Select GST Status**: Choose YES or NO from dropdown
2. **If YES Selected**:
   - Enter 2-digit state code (e.g., 01, 25, 99)
   - Enter PAN number in format ABCDE1234F
   - Enter 4-character entity code (letters/numbers only)
3. **If NO Selected**:
   - Choose Declaration or RCM
   - If Declaration selected, choose Collected or Pending status
   - If RCM selected, no additional fields required

## Testing

The implementation has been tested with:
- Form field validation
- Conditional field display
- Data persistence
- Migration application

## Future Enhancements

1. **State Code Validation**: Could add validation against actual state codes
2. **PAN Number Verification**: Could integrate with PAN verification service
3. **Entity Code Validation**: Could add business logic validation
4. **Audit Trail**: Could add logging for field value changes

## Notes

- All new fields are optional (null=True, blank=True)
- Conditional fields are automatically cleared when parent field changes
- Validation is performed both on frontend and backend
- The implementation follows the same pattern as the SPO page
