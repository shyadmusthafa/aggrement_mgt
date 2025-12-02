# SPO Code Validation Implementation

## Overview
This document describes the implementation of SPO code validation based on Sale Organization selection in the CFA Agreement form. The validation ensures that SPO codes follow the correct format based on the selected organization.

## Validation Rules

### Chettinad Organization
- **Format**: 1 letter + 3 numbers
- **Examples**: A012, B123, C456, D789
- **Pattern**: `^[A-Za-z]\d{3}$`
- **Max Length**: 4 characters

### Anjani Organization
- **Format**: 2 letters + 2 numbers
- **Examples**: AB12, CD34, EF56, GH78
- **Pattern**: `^[A-Za-z]{2}\d{2}$`
- **Max Length**: 4 characters

## Implementation Details

### 1. Backend Validation (Django Forms)

#### File: `dashboard/forms.py`
- Added `clean_spo_code()` method to validate SPO code format
- Added `clean()` method to ensure both fields are provided together
- Added regex import for pattern matching
- Added unique IDs to form fields for JavaScript targeting

#### Key Methods:
```python
def clean_spo_code(self):
    spo_code = self.cleaned_data.get('spo_code')
    sale_organization = self.cleaned_data.get('sale_organization')
    
    if not spo_code:
        return spo_code
        
    if not sale_organization:
        raise forms.ValidationError("Please select a Sale Organization first.")
    
    # Remove any spaces and convert to uppercase
    spo_code = spo_code.strip().upper()
    
    if sale_organization == 'Chettinad':
        # Format: 1 letter + 3 numbers (A012)
        if not re.match(r'^[A-Z][0-9]{3}$', spo_code):
            raise forms.ValidationError(
                "For Chettinad, SPO code must be 1 letter followed by 3 numbers (e.g., A012, B123, C456)"
            )
    elif sale_organization == 'Anjani':
        # Format: 2 letters + 2 numbers (AB12)
        if not re.match(r'^[A-Z]{2}[0-9]{2}$', spo_code):
            raise forms.ValidationError(
                "For Anjani, SPO code must be 2 letters followed by 2 numbers (e.g., AB12, CD34, EF56)"
            )
    
    return spo_code
```

### 2. Frontend Validation (JavaScript)

#### File: `dashboard/templates/dashboard/cfa_agreement_form.html`
- Real-time validation on SPO code input
- Validation when sale organization changes
- Dynamic help text updates
- Visual feedback with CSS classes

#### Key Functions:
```javascript
function validateSPOCode(spoCode, saleOrganization) {
    if (!spoCode || !saleOrganization) return true;
    
    if (saleOrganization === 'Chettinad') {
        const pattern = /^[A-Za-z]\d{3}$/;
        return pattern.test(spoCode) && spoCode.length <= 4;
    } else if (saleOrganization === 'Anjani') {
        const pattern = /^[A-Za-z]{2}\d{2}$/;
        return pattern.test(spoCode) && spoCode.length <= 4;
    }
    return true;
}
```

### 3. CSS Styling

#### File: `dashboard/static/dashboard/css/standard-ui.css`
- Added validation-specific CSS classes
- Success and error state styling
- Smooth transitions and visual feedback

#### Key Classes:
```css
.spo-code-validation.success {
    border-color: #28a745 !important;
    background-color: #f8fff9 !important;
    box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.25) !important;
}

.spo-code-validation.error {
    border-color: #dc3545 !important;
    background-color: #fff8f8 !important;
    box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.25) !important;
}
```

## User Experience Features

### 1. Dynamic Help Text
- Help text changes based on selected organization
- Shows specific format requirements for each organization
- Color-coded for better visibility

### 2. Real-time Validation
- Validation occurs as user types
- Immediate feedback on format compliance
- Prevents form submission with invalid data

### 3. Visual Feedback
- Green border and background for valid codes
- Red border and background for invalid codes
- Smooth transitions between states

### 4. Smart Field Management
- SPO code field is cleared when organization is deselected
- Validation styling is reset appropriately
- Prevents orphaned SPO codes

## Form Submission Validation

The form submission handler includes comprehensive validation:
- File size validation
- SPO code format validation
- Required field validation
- Cross-field dependency validation

## Testing

A test HTML file (`test_spo_validation.html`) has been created to demonstrate the validation functionality outside of the Django application.

## Usage Instructions

1. **Select Sale Organization**: Choose either "Chettinad" or "Anjani"
2. **Enter SPO Code**: Follow the format shown in the help text
3. **Real-time Feedback**: See immediate validation results
4. **Form Submission**: Form will only submit if all validations pass

## Error Messages

### Common Error Scenarios:
- **No Sale Organization**: "Please select a Sale Organization first."
- **Invalid Chettinad Format**: "For Chettinad, SPO code must be 1 letter followed by 3 numbers (e.g., A012, B123, C456)"
- **Invalid Anjani Format**: "For Anjani, SPO code must be 2 letters followed by 2 numbers (e.g., AB12, CD34, EF56)"
- **Missing SPO Code**: "SPO code is required when Sale Organization is selected."

## Technical Notes

- Uses Django's built-in form validation
- JavaScript validation for immediate user feedback
- CSS classes for consistent styling
- Responsive design considerations
- Accessibility features maintained

## Future Enhancements

Potential improvements could include:
- Auto-formatting of SPO codes as user types
- Suggestion of next available codes
- Integration with existing SPO code database
- Bulk validation for multiple entries
