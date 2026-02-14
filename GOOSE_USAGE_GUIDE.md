# Goose Payroll Auditor - Usage Guide

## 🚀 Quick Start in Goose

### 1. Import the Extension

```python
import sys
sys.path.append('/Users/esoria/Downloads')  # Adjust to your path
from goose_payroll_auditor import audit, differences, report, batch, latest, history
```

### 2. Basic Commands

#### Compare Two Files
```python
# Simple comparison
result = audit('payroll_jan.csv', 'payroll_feb.csv')
print(result)
```

Output:
```
============================================================
📊 PAYROLL AUDIT SUMMARY
============================================================

📁 Files Compared:
   • payroll_jan.csv (150 rows)
   • payroll_feb.csv (150 rows)

📈 Results:
   • Total Rows: 150
   • Matched: 142 ✓
   • Differences: 8
   • Match Rate: 94.67%

⚠️  WARNING - Moderate differences found

🔍 Field Differences:
   • overtime: 5 differences
     Avg: 2.50
   • federal_tax: 3 differences
     Avg: 15.30

============================================================
```

#### View Detailed Differences
```python
# Show differences from last audit
diffs = differences(limit=5)
print(diffs)
```

#### Generate HTML Report
```python
# Create beautiful HTML report
report('audit_report.html', format='html')
# Opens in browser automatically
```

#### Batch Audit Multiple Files
```python
# Audit all CSV files in a directory
results = batch('/Users/esoria/Downloads', pattern='payroll_*.csv')
print(results)
```

#### Compare Latest Files
```python
# Automatically compare the 2 most recent files
result = latest('/Users/esoria/Downloads', pattern='payroll_*.csv')
print(result)
```

#### View Audit History
```python
# See all audits performed in this session
hist = history()
print(hist)
```

## 🎯 Common Workflows

### Workflow 1: Daily Payroll Check
```python
from goose_payroll_auditor import latest, report

# Compare today's payroll with yesterday's
result = latest('/data/payroll', pattern='payroll_*.csv')
print(result)

# If differences found, generate report
report('/reports/daily_audit.html')
```

### Workflow 2: Month-End Audit
```python
from goose_payroll_auditor import batch, report

# Audit all payroll files for the month
results = batch('/data/payroll/2024-02', pattern='*.csv')
print(results)

# Generate comprehensive report
report('/reports/february_audit.html')
```

### Workflow 3: System Migration Validation
```python
from goose_payroll_auditor import audit, differences, report

# Compare old system export vs new system
result = audit('old_system_export.csv', 'new_system_export.xlsx')
print(result)

# Get detailed differences
diffs = differences(limit=20)
print(diffs)

# Generate report for stakeholders
report('migration_validation.html')
```

### Workflow 4: Automated Monitoring
```python
from goose_payroll_auditor import latest, report
import schedule
import time

def daily_check():
    result = latest('/data/payroll')
    
    # Extract match rate
    if 'Match Rate: ' in result:
        match_rate = float(result.split('Match Rate: ')[1].split('%')[0])
        
        if match_rate < 95:
            # Generate alert report
            report('/alerts/payroll_alert.html')
            print(f"⚠️  ALERT: Low match rate {match_rate}%")
    
    print(result)

# Run every day at 9 AM
schedule.every().day.at("09:00").do(daily_check)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 🔧 Advanced Usage

### Custom Configuration
```python
from goose_payroll_auditor import GoosePayrollAuditor

# Create auditor with custom settings
auditor = GoosePayrollAuditor()
auditor.auditor.config = {
    'numeric_tolerance': 0.001,  # Stricter comparison
    'field_mappings': {
        'bonus': ['bonus', 'bonus_pay', 'incentive']
    }
}

result = auditor.quick_audit('file1.csv', 'file2.csv')
print(result)
```

### Programmatic Access
```python
from goose_payroll_auditor import init_auditor

auditor = init_auditor()

# Get raw results
result = auditor.auditor.audit('file1.csv', 'file2.csv')

# Access specific data
summary = result['summary']
print(f"Match rate: {summary['match_rate']}")
print(f"Differences: {summary['rows_with_differences']}")

# Get field statistics
for field, stats in summary['field_statistics'].items():
    print(f"{field}: {stats['count']} differences")
```

## 📱 Integration with Goose Desktop

### In Goose Chat:
```
You: Compare the two latest payroll files in my Downloads folder

Goose: *runs the command*
from goose_payroll_auditor import latest
result = latest('/Users/esoria/Downloads', 'payroll_*.csv')
print(result)

[Shows formatted results]
```

### As a Goose Tool:
You can ask Goose to:
- "Audit these two payroll files"
- "Show me the differences in detail"
- "Generate an HTML report"
- "Check all payroll files from last week"
- "Compare today's payroll with yesterday's"

## 🎨 Output Examples

### Success (High Match Rate)
```
✅ EXCELLENT - High match rate!
Match Rate: 98.50%
Differences: 3
```

### Warning (Moderate Differences)
```
⚠️  WARNING - Moderate differences found
Match Rate: 87.20%
Differences: 19
```

### Alert (Significant Issues)
```
❌ ALERT - Significant differences detected!
Match Rate: 72.10%
Differences: 42
```

## 🐛 Troubleshooting

### Import Error
```python
# Make sure the path is correct
import sys
sys.path.append('/Users/esoria/Downloads')

# Verify files exist
import os
print(os.path.exists('/Users/esoria/Downloads/goose_payroll_auditor.py'))
```

### No Pandas
```bash
pip3 install --user pandas numpy openpyxl
```

### File Not Found
```python
# Use absolute paths
audit('/Users/esoria/Downloads/file1.csv', '/Users/esoria/Downloads/file2.csv')
```

## 💡 Tips

1. **Use absolute paths** for reliability
2. **Check history()** to see previous audits
3. **Generate HTML reports** for sharing with non-technical users
4. **Use batch()** for end-of-period audits
5. **Use latest()** for quick daily checks
6. **Keep audit reports** for compliance tracking

## 🔗 Related Commands

- `audit(file1, file2)` - Compare two files
- `differences(limit)` - Show detailed differences
- `report(path, format)` - Generate report
- `batch(directory, pattern)` - Batch audit
- `latest(directory, pattern)` - Compare latest files
- `history()` - Show audit history

---

**Need help?** Check the INTEGRATION_EXAMPLES.md for more advanced patterns!
