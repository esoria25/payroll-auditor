#!/usr/bin/env python3
"""
Generate sample payroll data for testing the auditor
"""

import pandas as pd
import random
from datetime import datetime, timedelta

def generate_sample_payroll(num_employees=20, filename='sample_payroll.csv'):
    """Generate sample payroll data"""
    
    # Sample employee names
    first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Robert', 'Lisa', 
                   'James', 'Mary', 'William', 'Patricia', 'Richard', 'Jennifer', 'Thomas']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                  'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson']
    
    employees = []
    
    for i in range(num_employees):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        # Generate payroll data
        regular_hours = round(random.uniform(35, 40), 2)
        overtime_hours = round(random.uniform(0, 10), 2)
        pto_hours = round(random.uniform(0, 8), 2) if random.random() > 0.7 else 0
        sick_hours = round(random.uniform(0, 8), 2) if random.random() > 0.9 else 0
        
        hourly_rate = round(random.uniform(15, 45), 2)
        gross_pay = (regular_hours * hourly_rate) + (overtime_hours * hourly_rate * 1.5)
        
        # Tips (for some employees)
        tips_cash = round(random.uniform(50, 200), 2) if random.random() > 0.6 else 0
        tips_paycheck = round(random.uniform(30, 150), 2) if random.random() > 0.7 else 0
        
        # Calculate taxes
        federal_tax = round(gross_pay * 0.12, 2)
        social_security = round(gross_pay * 0.062, 2)
        medicare = round(gross_pay * 0.0145, 2)
        state_tax = round(gross_pay * 0.05, 2)
        local_tax = round(gross_pay * 0.02, 2)
        pfml = round(gross_pay * 0.006, 2)
        
        employee = {
            'Employee Name': name,
            'Pay Date': '2024-01-15',
            'Regular Hours': regular_hours,
            'Overtime Hours': overtime_hours,
            'PTO Hours': pto_hours,
            'Sick Hours': sick_hours,
            'Hourly Rate': hourly_rate,
            'Gross Pay': round(gross_pay, 2),
            'Tips Cash': tips_cash,
            'Tips Paycheck': tips_paycheck,
            'Federal Income Tax': federal_tax,
            'Social Security': social_security,
            'Medicare': medicare,
            'State Tax': state_tax,
            'Local Tax': local_tax,
            'PFML': pfml,
            'Net Pay': round(gross_pay - federal_tax - social_security - medicare - 
                           state_tax - local_tax - pfml, 2)
        }
        
        employees.append(employee)
    
    df = pd.DataFrame(employees)
    df.to_csv(filename, index=False)
    print(f"✓ Generated {filename} with {num_employees} employees")
    return df


def generate_modified_version(original_file, output_file, num_changes=5):
    """Generate a modified version with some differences"""
    
    df = pd.read_csv(original_file)
    
    # Make random changes
    changes_made = []
    
    for _ in range(num_changes):
        row_idx = random.randint(0, len(df) - 1)
        
        # Pick a field to modify
        numeric_fields = ['Regular Hours', 'Overtime Hours', 'Federal Income Tax', 
                         'Social Security', 'Medicare', 'State Tax']
        field = random.choice(numeric_fields)
        
        old_value = df.at[row_idx, field]
        
        # Modify by 5-20%
        change_percent = random.uniform(0.05, 0.20)
        new_value = round(old_value * (1 + change_percent), 2)
        
        df.at[row_idx, field] = new_value
        
        changes_made.append({
            'employee': df.at[row_idx, 'Employee Name'],
            'field': field,
            'old': old_value,
            'new': new_value
        })
    
    df.to_csv(output_file, index=False)
    print(f"✓ Generated {output_file} with {num_changes} modifications")
    
    print("\nChanges made:")
    for change in changes_made:
        print(f"  {change['employee']}: {change['field']} changed from {change['old']} to {change['new']}")
    
    return df


if __name__ == '__main__':
    print("Generating sample payroll data...\n")
    
    # Generate original file
    generate_sample_payroll(20, 'payroll_original.csv')
    
    # Generate modified version
    generate_modified_version('payroll_original.csv', 'payroll_corrected.csv', num_changes=8)
    
    # Generate Excel version
    try:
        df = pd.read_csv('payroll_original.csv')
        df.to_excel('payroll_original.xlsx', index=False)
        print("\n✓ Generated payroll_original.xlsx")
    except Exception as e:
        print(f"\n⚠ Could not generate Excel file: {e}")
        print("  Install openpyxl: pip install openpyxl")
    
    print("\n" + "="*80)
    print("Sample data generated successfully!")
    print("="*80)
    print("\nTo test the auditor, run:")
    print("  python payroll_auditor.py payroll_original.csv payroll_corrected.csv")
    print("\nOr generate an HTML report:")
    print("  python payroll_auditor.py payroll_original.csv payroll_corrected.csv -o report.html -f html")
