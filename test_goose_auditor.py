#!/usr/bin/env python3
"""
Test script for Goose Payroll Auditor
"""

import sys
sys.path.append('.')

from goose_payroll_auditor import audit, differences, report, batch, latest, history

print("🧪 Testing Goose Payroll Auditor\n")

# Test 1: Check if files exist
import os
csv_files = [f for f in os.listdir('.') if f.startswith('payroll_') and f.endswith('.csv')]
print(f"Found {len(csv_files)} payroll CSV files")

if len(csv_files) >= 2:
    # Test 2: Quick audit
    print("\n📊 Test 1: Quick Audit")
    result = audit(csv_files[0], csv_files[1])
    print(result)
    
    # Test 3: Get differences
    print("\n📋 Test 2: Get Differences")
    diffs = differences(limit=3)
    print(diffs)
    
    # Test 4: Generate report
    print("\n📄 Test 3: Generate Report")
    report_result = report('test_audit_report.html', 'html')
    print(report_result)
    
    # Test 5: History
    print("\n📜 Test 4: Audit History")
    hist = history()
    print(hist)
    
    print("\n✅ All tests completed!")
else:
    print("⚠️  Not enough CSV files to test. Need at least 2 payroll files.")
    print("\nYou can generate test data with:")
    print("  python3 generate_sample_data.py")
