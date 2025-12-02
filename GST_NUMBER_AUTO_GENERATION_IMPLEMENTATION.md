# GST Number Auto-Generation Implementation

## Overview
This document describes the implementation of automatic GST number generation by concatenating State Code + PAN Number + Last 4 Characters when GST Status is set to YES.

## Changes Made

### 1. Form Field Updates (`dashboard/forms.py`)
- **GST Number Field**: Made read-only (disabled) with `readonly: 'readonly'`
- **Placeholder**: Changed to "GST number will be auto-generated"
- **Removed**: Pattern validation and title since field is now auto-generated

### 2. Template Updates (`dashboard/templates/dashboard/cfa_agreement_form.html`)
- **Help Text**: Added explanation below GST number field
- **JavaScript Logic**: Implemented auto-concatenation functionality

### 3. CSS Styling (`dashboard/static/dashboard/css/standard-ui.css`)
- **Read-only Styling**: Enhanced appearance for disabled fields
- **Success State**: Special styling when GST number is auto-generated

## Auto-Generation Logic

### When GST Status = YES:
1. **State Code** (2 digits) + **PAN Number** (10 characters) + **Last 4 Characters** (4 characters)
2. **Total Length**: 16 characters
3. **Format Example**: `22ABCDE1234F1234`

### Field Dependencies:
- **State Code**: Must be 2 digits (00-99)
- **PAN Number**: Must be 10 characters (ABCDE1234F format)
- **Last 4 Characters**: Must be 4 alphanumeric characters

### Auto-Update Triggers:
- **Real-time**: Updates as user types in any of the three fields
- **Field Change**: Updates when any field value changes
- **GST Status Change**: Clears GST number when status changes from YES

## User Experience Features

### Visual Feedback:
- **Default State**: Gray background, disabled appearance
- **Auto-generated State**: Green border, success styling
- **Help Text**: Clear explanation of how GST number is generated

### Validation:
- **Real-time**: GST number updates as fields are filled
- **Automatic**: No manual input required
- **Consistent**: Always follows the same concatenation pattern

### Field Behavior:
- **State Code**: Only accepts 2 digits
- **PAN Number**: Auto-converts to uppercase, PAN format validation
- **Last 4 Characters**: Letters and numbers only, no special characters

## Technical Implementation

### JavaScript Functions:
```javascript
// Main function to update GST number
function updateGSTNumber() {
    // Concatenates State Code + PAN Number + Last 4 Characters
    // Applies success styling when complete
    // Clears field when incomplete
}

// Event listeners on all three input fields
// Calls updateGSTNumber() on every input change
```

### CSS Classes:
- `.gst-auto-generated`: Success state styling
- `input[readonly]`: Default disabled field styling

### Form Validation:
- **Backend**: GST number field is required but auto-populated
- **Frontend**: Real-time validation and auto-generation

## Usage Instructions

1. **Select GST Status**: Choose "YES" from dropdown
2. **Enter State Code**: Type 2-digit state code (e.g., 22)
3. **Enter PAN Number**: Type PAN in format ABCDE1234F
4. **Enter Last 4 Characters**: Type 4 alphanumeric characters
5. **GST Number**: Automatically populated and styled

## Benefits

1. **Data Consistency**: Ensures GST number format is always correct
2. **User Experience**: No manual GST number entry required
3. **Validation**: Built-in format validation through field constraints
4. **Visual Feedback**: Clear indication when GST number is complete
5. **Error Prevention**: Eliminates manual entry errors

## Notes

- GST number field is completely read-only when auto-generation is active
- Field is automatically cleared when GST Status changes from YES to NO
- All three component fields must have values for GST number to be generated
- The implementation maintains backward compatibility with existing data
