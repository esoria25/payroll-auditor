#!/usr/bin/env python3
"""
Excel Export Wrapper for Payroll Auditor
Converts audit results to Excel format
"""

import sys
import pandas as pd
from universal_payroll_auditor import UniversalPayrollAuditor
from datetime import datetime

def export_to_excel(file1, file2, output_file):
    """Run audit and export to Excel"""
    
    print("\n" + "="*80)
    print("PAYROLL AUDIT - EXCEL EXPORT")
    print("="*80)
    print(f"\nFile 1: {file1}")
    print(f"File 2: {file2}")
    print(f"Output: {output_file}")
    print()
    
    # Run the audit
    auditor = UniversalPayrollAuditor()
    result = auditor.audit(file1, file2)
    
    # Create Excel writer
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        
        # Sheet 1: Summary
        summary_data = {
            'Metric': [
                'Total Rows Compared',
                'Matching Rows',
                'Different Rows',
                'Match Percentage',
                'Total Differences',
                'Comparison Date',
                'File 1',
                'File 2'
            ],
            'Value': [
                result['summary']['total_rows'],
                result['summary']['matching_rows'],
                result['summary']['different_rows'],
                f"{result['summary']['match_percentage']:.2f}%",
                result['summary']['total_differences'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                file1,
                file2
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Sheet 2: Differences
        if result['differences']:
            diff_rows = []
            for diff in result['differences']:
                for field_diff in diff['fields']:
                    diff_rows.append({
                        'Row': diff['row'],
                        'Employee': diff.get('employee', 'N/A'),
                        'Field': field_diff['field'],
                        'File 1 Value': field_diff['file1'],
                        'File 2 Value': field_diff['file2'],
                        'Difference': field_diff.get('difference', 'Changed')
                    })
            
            if diff_rows:
                diff_df = pd.DataFrame(diff_rows)
                diff_df.to_excel(writer, sheet_name='Differences', index=False)
        
        # Sheet 3: Matching Rows
        if result['matching_rows']:
            matching_data = {
                'Row': [m['row'] for m in result['matching_rows']],
                'Employee': [m.get('employee', 'N/A') for m in result['matching_rows']],
                'Status': ['All fields match'] * len(result['matching_rows'])
            }
            matching_df = pd.DataFrame(matching_data)
            matching_df.to_excel(writer, sheet_name='Matching Rows', index=False)
    
    print(f"✅ Excel report created: {output_file}")
    print(f"   Sheets: Summary, Differences, Matching Rows")
    print("="*80)
    print()
    
    return output_file

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 export_to_excel.py file1 file2 [output.xlsx]")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else 'payroll_audit_report.xlsx'
    
    export_to_excel(file1, file2, output)

