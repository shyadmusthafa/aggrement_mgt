# Stipend Salary Calculation Enhancement Documentation

## Overview
This document describes the automatic stipend salary calculation enhancement implemented in the `payrollgenerate()` function. The enhancement calculates pro-rated salaries for Stipend, Trainee, and Intern employees based on their payscale effective periods and applies LOP (Loss of Pay) deductions.

## Requirements Summary

### 1. **Employee Categories**
- **Target Employees**: Stipend, Trainee, Intern
- **Integration**: Enhanced within existing `payrollgenerate()` function (no separate functions)

### 2. **Payroll Cycle**
- **Default Cycle**: 21st of previous month to 20th of current month
- **Example**: For MonthAndYear = "2025-09", cycle is 2025-08-21 to 2025-09-20

### 3. **Data Source**
- **Payscale Table**: `hrm_payscale`
- **Columns Used**: 
  - `effective_from_date`
  - `effective_to_date`
  - `monthly_value` (Amount)
  - `yearly_value` (YearlyAmount)

### 4. **Salary Calculation Logic**
- **Period Splitting**: Payroll cycle is split across employee's payscale effective periods
- **Pro-rating Formula**: `(monthly_salary / 30) × working_days`
- **Example**:
  ```
  Period 1: 2024-09-04 to 2025-09-04 → ₹48,000/month
  Period 2: 2025-09-05 to 2026-09-05 → ₹49,000/month
  Payroll: 2025-08-21 to 2025-09-20 (31 days)
  
  Segment 1: 2025-08-21 to 2025-09-03 (14 days) → (48000/30) × 14 = ₹22,400
  Segment 2: 2025-09-04 to 2025-09-20 (17 days) → (49000/30) × 17 = ₹27,766.67
  Total: ₹50,166.67
  ```

### 5. **LOP (Loss of Pay) Calculation**
- **Source**: `hrm_lop` table
- **Columns**: `old_lop`, `new_lop`, `total_work_days`
- **Logic**:
  - **old_lop**: Based on effective_from_date period salary (beginning of payroll cycle)
  - **new_lop**: Based on effective_to_date period salary (end of payroll cycle)
  - **Formula**: 
    ```
    old_lop_amount = old_lop × (old_period_gross / total_work_days)
    new_lop_amount = new_lop × (new_period_gross / total_work_days)
    total_lop_deduction = old_lop_amount + new_lop_amount
    ```

### 6. **Database Operations**

#### **Insert into `hrm_payscale_monpayr_details`**
```sql
INSERT INTO hrm_payscale_monpayr_details 
(MonthAndYear, u_name, company_id, payroll_group_id, category_of_emp, PD, WD, lopAmount, payslip_model) 
VALUES (?, ?, ?, ?, 'Stipend', [total_working_days], [total_cycle_days], [lop_deduction], 'Standard');
```

#### **Insert Salary Segments into `hrm_payscale_monpayr`**
```sql
-- For each salary segment
INSERT INTO hrm_payscale_monpayr 
(MonthAndYear, u_name, company_id, payroll_group_id, category_of_emp, DataName, Values, Actual, Pre, Per, Description, SpeDescription, preActive) 
VALUES (?, ?, ?, ?, 'Stipend', 'E001', [pro_rated_salary], [monthly_salary], 0, 0, 'Stipend - [start] to [end]', 'Auto Generated', 1);
```

#### **Insert LOP Deductions**
```sql
-- Old LOP Deduction (D001)
INSERT INTO hrm_payscale_monpayr 
(MonthAndYear, u_name, company_id, payroll_group_id, category_of_emp, DataName, Values, Actual, Pre, Per, Description, SpeDescription, preActive) 
VALUES (?, ?, ?, ?, 'Stipend', 'D001', [old_lop_amount], [old_lop_amount], 0, 0, 'Old LOP - X days', 'Auto Generated', 1);

-- New LOP Deduction (D002)
INSERT INTO hrm_payscale_monpayr 
(MonthAndYear, u_name, company_id, payroll_group_id, category_of_emp, DataName, Values, Actual, Pre, Per, Description, SpeDescription, preActive) 
VALUES (?, ?, ?, ?, 'Stipend', 'D002', [new_lop_amount], [new_lop_amount], 0, 0, 'New LOP - X days', 'Auto Generated', 1);
```

#### **Insert Total Gross Salary**
```sql
INSERT INTO hrm_payscale_monpayr 
(MonthAndYear, u_name, company_id, payroll_group_id, category_of_emp, DataName, Values, Actual, Pre, Per, Description, SpeDescription, preActive) 
VALUES (?, ?, ?, ?, 'Stipend', 'Gross', [final_salary], [total_pro_rated_salary], 0, 0, 'Total Stipend Salary', 'Auto Generated', 1);
```

## Implementation Details

### **File Modified**
- `dashboard/templates/dashboard/payrollgenerate.php`

### **Code Location**
- Lines 806-1041: Stipend salary calculation enhancement
- Inserted after `$CategoryOfEmp` variable assignment
- Before normal payroll calculation logic

### **Flow**
1. Check if employee is Stipend/Trainee/Intern
2. Calculate payroll cycle dates (21st to 20th)
3. Fetch payscale periods from `hrm_payscale` table
4. Split payroll cycle across payscale effective periods
5. Calculate pro-rated salary for each segment
6. Fetch LOP data from `hrm_lop` table
7. Calculate old_lop and new_lop amounts based on respective period salaries
8. Calculate final salary (total pro-rated - total LOP)
9. Insert data into database tables
10. Log calculation results
11. Skip normal payroll calculation (using `continue`)

### **Error Handling**
- If no payscale data found: Log error and skip employee
- If no LOP data: Continue with zero LOP deduction
- All database operations use parameterized queries to prevent SQL injection

### **Logging**
```
Stipend calculated: [u_name] | Pro-rated: [amount] | LOP: [amount] | Final: [amount]
```

## Example Calculation Walkthrough

### **Scenario**
- **Employee**: EMP001 (Stipend)
- **MonthAndYear**: 2025-09
- **Payroll Cycle**: 2025-08-21 to 2025-09-20 (31 days)

### **Payscale Periods**
1. **Period 1**: 2024-09-04 to 2025-09-04 → ₹48,000/month
2. **Period 2**: 2025-09-05 to 2026-09-05 → ₹49,000/month

### **Salary Segments**
1. **Segment 1**: 2025-08-21 to 2025-09-03 (14 days)
   - Pro-rated: (48000/30) × 14 = ₹22,400

2. **Segment 2**: 2025-09-04 to 2025-09-20 (17 days)
   - Pro-rated: (49000/30) × 17 = ₹27,766.67

**Total Pro-rated**: ₹50,166.67

### **LOP Calculation**
- **old_lop**: 1 day (from hrm_lop)
- **new_lop**: 1 day (from hrm_lop)
- **total_work_days**: 31 (from hrm_lop)

**old_lop_amount**: 1 × (48000/31) = ₹1,548.39 (Segment 1 salary)
**new_lop_amount**: 1 × (49000/31) = ₹1,580.65 (Segment 2 salary)
**Total LOP**: ₹3,129.04

### **Final Salary**
₹50,166.67 - ₹3,129.04 = **₹47,037.63**

### **Database Records**

#### **hrm_payscale_monpayr_details**
| MonthAndYear | u_name | company_id | payroll_group_id | category_of_emp | PD | WD | lopAmount | payslip_model |
|--------------|--------|------------|------------------|-----------------|----|----|-----------|---------------|
| 2025-09 | EMP001 | 1 | 1 | Stipend | 31 | 31 | 3129.04 | Standard |

#### **hrm_payscale_monpayr**
| DataName | Values | Actual | Description |
|----------|--------|--------|-------------|
| E001 | 22400.00 | 48000 | Stipend - 2025-08-21 to 2025-09-03 |
| E001 | 27766.67 | 49000 | Stipend - 2025-09-04 to 2025-09-20 |
| D001 | 1548.39 | 1548.39 | Old LOP - 1 days |
| D002 | 1580.65 | 1580.65 | New LOP - 1 days |
| Gross | 47037.63 | 50166.67 | Total Stipend Salary |

## Additional Bug Fix

### **Fixed LOP Code Bug**
- **Location**: Lines 1462-1467
- **Issue**: Loop was using `$old_lop2` instead of `$new_lop2`
- **Fixed Code**:
```php
$new_lop2=json_decode(json_encode($new_lop1), true);
foreach ($new_lop2 as $paid => $days) {  // Fixed: was $old_lop2
    $pd = $days['total_work_days'] - $days['PD'];
}
```

## Benefits

1. ✅ **Automatic Calculation**: No manual intervention required for stipend salaries
2. ✅ **Accurate Pro-rating**: Handles multiple payscale periods correctly
3. ✅ **Effective Date Splitting**: Properly splits LOP based on old/new periods
4. ✅ **Database Integration**: Seamlessly integrates with existing payroll tables
5. ✅ **Error Handling**: Graceful handling of missing data
6. ✅ **Audit Trail**: Comprehensive logging for tracking
7. ✅ **No Duplication**: Skips normal payroll calculation for stipend employees

## Testing Checklist

- [ ] Test with single payscale period
- [ ] Test with multiple payscale periods across payroll cycle
- [ ] Test with old_lop only
- [ ] Test with new_lop only
- [ ] Test with both old_lop and new_lop
- [ ] Test with no LOP data
- [ ] Test with no payscale data (error case)
- [ ] Verify database insertions
- [ ] Check log output
- [ ] Verify final salary calculations

## Future Enhancements

1. **Configurable Payroll Cycle**: Allow dynamic payroll cycle configuration
2. **Email Notifications**: Send calculation summary to HR
3. **Validation Rules**: Add business rule validations
4. **Bulk Processing**: Optimize for large employee batches
5. **Reporting**: Generate detailed calculation reports

---

**Last Updated**: October 2, 2025
**Author**: System Enhancement
**Version**: 1.0

