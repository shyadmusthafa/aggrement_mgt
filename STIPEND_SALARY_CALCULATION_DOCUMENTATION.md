# Automatic Stipend Salary Calculation Implementation

## Overview
This implementation provides automatic stipend salary calculation for employees based on their CTC (Cost to Company) periods and payroll cycles. The system automatically splits payroll cycles across different CTC effective periods and calculates pro-rated salaries.

## Key Features

### 1. CTC Period Splitting
- Automatically identifies CTC periods from `mas_ctc` table
- Splits payroll cycles across multiple CTC effective periods
- Handles overlapping and consecutive CTC periods

### 2. Pro-rata Salary Calculation
- Calculates salary based on working days within each CTC period
- Supports different monthly salaries for different periods
- Example: 48000/month for first year, 49000/month for second year

### 3. LOP (Loss of Pay) Integration
- Integrates with `hrm_lop` table
- Uses `old_lop` and `new_lop` columns for deduction calculations
- Applies LOP deductions to final salary

### 4. Database Integration
- Inserts calculated data into `hrm_payscale_monpayr` table
- Inserts employee details into `hrm_payscale_monpayr_details` table
- Maintains audit trail with auto-generated descriptions

## Implementation Details

### Enhanced `payrollgenerate()` Function
The stipend salary calculation has been integrated directly into the existing `payrollgenerate()` function. The logic is executed inline when processing each employee during payroll generation.

**Integration Point**: The stipend calculation runs automatically for employees with `category_of_emp` set to:
- 'Stipend'
- 'Trainee' 
- 'Intern'

**Process Flow**:
1. **Employee Detection**: Checks if employee is eligible for stipend calculation
2. **Payroll Cycle Calculation**: Calculates cycle dates (21st of previous month to 20th of current month)
3. **CTC Period Retrieval**: Gets CTC periods from `mas_ctc` table
4. **Salary Segmentation**: Splits payroll cycle across CTC periods
5. **Pro-rata Calculation**: Calculates salary based on working days
6. **LOP Application**: Applies Loss of Pay deductions
7. **Database Insertion**: Inserts results into payroll tables

## Example Usage

### Scenario
- Employee: EMP001
- CTC Period 1: 2024-09-04 to 2025-09-04 (Monthly: 48000, Yearly: 576000)
- CTC Period 2: 2025-09-05 to 2026-09-05 (Monthly: 49000, Yearly: 588000)
- Payroll Cycle: 2025-08-21 to 2025-09-20 (31 days)

### Calculation Process

1. **CTC Period Splitting**:
   - Segment 1: 2025-08-21 to 2025-09-03 (14 days) → 48000/month
   - Segment 2: 2025-09-04 to 2025-09-20 (17 days) → 49000/month

2. **Pro-rata Calculation**:
   - Segment 1: (48000/30) × 14 = 22400
   - Segment 2: (49000/30) × 17 = 27766.67
   - Total Pro-rated: 50166.67

3. **LOP Application**:
   - If LOP = 2 days: (48000/30) × 2 = 3200 deduction
   - Final Salary: 50166.67 - 3200 = 46966.67

### Database Records Created

#### hrm_payscale_monpayr_details
```sql
INSERT INTO hrm_payscale_monpayr_details 
(MonthAndYear, u_name, company_id, payroll_group_id, category_of_emp, PD, WD, lopAmount, payslip_model) 
VALUES ('2025-09', 'EMP001', 1, 1, 'Stipend', 29, 31, 3200, 'Standard');
```

#### hrm_payscale_monpayr
```sql
-- Segment 1
INSERT INTO hrm_payscale_monpayr 
(MonthAndYear, u_name, company_id, payroll_group_id, category_of_emp, DataName, Values, Actual, Pre, Per, Description, SpeDescription, preActive) 
VALUES ('2025-09', 'EMP001', 1, 1, 'Stipend', 'E001', 22400, 48000, 0, 0, 'Stipend Salary - 2025-08-21 to 2025-09-03', 'Auto Generated', 1);

-- Segment 2
INSERT INTO hrm_payscale_monpayr 
(MonthAndYear, u_name, company_id, payroll_group_id, category_of_emp, DataName, Values, Actual, Pre, Per, Description, SpeDescription, preActive) 
VALUES ('2025-09', 'EMP001', 1, 1, 'Stipend', 'E001', 27766.67, 49000, 0, 0, 'Stipend Salary - 2025-09-04 to 2025-09-20', 'Auto Generated', 1);

-- Total Gross
INSERT INTO hrm_payscale_monpayr 
(MonthAndYear, u_name, company_id, payroll_group_id, category_of_emp, DataName, Values, Actual, Pre, Per, Description, SpeDescription, preActive) 
VALUES ('2025-09', 'EMP001', 1, 1, 'Stipend', 'Gross', 46966.67, 50166.67, 0, 0, 'Total Stipend Salary', 'Auto Generated', 1);
```

## Integration Points

### Employee Eligibility
The system automatically identifies stipend employees based on `category_of_emp`:
- 'Stipend'
- 'Trainee' 
- 'Intern'

### Payroll Generation Integration
The stipend calculation is integrated into the main `payrollgenerate()` function and runs automatically for eligible employees during payroll processing.

### Error Handling
- Validates CTC data availability
- Handles missing LOP records gracefully
- Logs errors for debugging
- Continues processing other employees if one fails

## Database Tables Used

### Input Tables
- `mas_ctc`: Contains CTC periods and salary information
- `hrm_lop`: Contains LOP (Loss of Pay) data with old_lop and new_lop columns
- `hrm_payroll_cycle_config`: Optional configuration for payroll cycle dates

### Output Tables
- `hrm_payscale_monpayr`: Main payroll data table
- `hrm_payscale_monpayr_details`: Employee payroll details

## Configuration

### Payroll Cycle Configuration
Create `hrm_payroll_cycle_config` table for custom payroll cycles:
```sql
CREATE TABLE hrm_payroll_cycle_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payroll_group_id INT,
    MonthAndYear VARCHAR(7),
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### CTC Table Structure
Ensure `mas_ctc` table has required columns:
- `emp_code`: Employee code
- `effective_from_date`: CTC effective start date
- `effective_to_date`: CTC effective end date
- `monthly_salary`: Monthly salary amount
- `yearly_salary`: Yearly salary amount
- `company_id`: Company ID
- `payroll_group_id`: Payroll group ID

### LOP Table Structure
Ensure `hrm_lop` table has required columns:
- `emp_code`: Employee code
- `MonthAndYear`: Month and year
- `old_lop`: Old LOP days
- `new_lop`: New LOP days
- `total_work_days`: Total working days
- `company_id`: Company ID
- `payroll_group_id`: Payroll group ID

## Testing

### Test Cases
1. **Single CTC Period**: Employee with one CTC period covering entire payroll cycle
2. **Multiple CTC Periods**: Employee with multiple CTC periods (as in example)
3. **Partial CTC Coverage**: CTC period that doesn't cover entire payroll cycle
4. **LOP Application**: Employee with LOP deductions
5. **No CTC Data**: Employee without CTC data (should return error)

### Test Data
```sql
-- CTC Test Data
INSERT INTO mas_ctc (emp_code, effective_from_date, effective_to_date, monthly_salary, yearly_salary, company_id, payroll_group_id) 
VALUES ('EMP001', '2024-09-04', '2025-09-04', 48000, 576000, 1, 1);

INSERT INTO mas_ctc (emp_code, effective_from_date, effective_to_date, monthly_salary, yearly_salary, company_id, payroll_group_id) 
VALUES ('EMP001', '2025-09-05', '2026-09-05', 49000, 588000, 1, 1);

-- LOP Test Data
INSERT INTO hrm_lop (emp_code, MonthAndYear, old_lop, new_lop, total_work_days, company_id, payroll_group_id) 
VALUES ('EMP001', '2025-09', 1, 1, 31, 1, 1);
```

## Maintenance

### Monitoring
- Check error logs for calculation failures
- Monitor database performance during payroll processing
- Validate calculation accuracy with sample data

### Updates
- Modify CTC periods in `mas_ctc` table
- Update LOP data in `hrm_lop` table
- Adjust payroll cycle dates in configuration

## Troubleshooting

### Common Issues
1. **No CTC Found**: Ensure CTC data exists for employee and payroll period
2. **Calculation Errors**: Check date formats and CTC period overlaps
3. **Database Errors**: Verify table structures and permissions
4. **Performance Issues**: Consider indexing on frequently queried columns

### Debug Information
The system logs detailed information for troubleshooting:
- Employee codes processed
- CTC periods found
- Calculation results
- Database insertion results
- Error messages with context
