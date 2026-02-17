# 👥 Team Guide: Using the Payroll Auditor

**Repository:** https://github.com/esoria25/payroll-auditor

This guide shows your teammates how to use the Payroll Auditor to compare and audit payroll files.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Clone the Repository
```bash
git clone https://github.com/esoria25/payroll-auditor.git
cd payroll-auditor
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Start Comparing!
Choose your preferred method below.

---

## 🎯 Method 1: Web Interface (Easiest!)

### Start the Server:
```bash
python3 api_server.py
```

### Use It:
1. Open browser: **http://localhost:8080**
2. Drag & drop first payroll file
3. Drag & drop second payroll file
4. Click "Compare Files"
5. View detailed results!

**Perfect for:** Non-technical users, quick comparisons, visual results

---

## 💻 Method 2: Command Line

### Basic Comparison:
```bash
python3 universal_payroll_auditor.py file1.csv file2.xlsx
```

### Save Report:
```bash
python3 universal_payroll_auditor.py file1.csv file2.xlsx --output report.html
```

### JSON Output:
```bash
python3 universal_payroll_auditor.py file1.csv file2.xlsx --format json
```

**Perfect for:** Automation, scripting, batch processing

---

## 📦 Method 3: Batch Processing

For comparing multiple file pairs:

```bash
python3 batch_audit.py
```

Edit `batch_audit.py` to specify your file pairs.

**Perfect for:** Monthly audits, bulk comparisons

---

## 🐳 Method 4: Docker (No Python Setup!)

### If Docker is Installed:
```bash
docker-compose up
```

Access at: **http://localhost:5000**

**Perfect for:** Consistent environment, production deployment

---

## 📋 Supported File Formats

✅ **CSV** - Comma-separated values
✅ **Excel** - .xlsx, .xls files
✅ **PDF** - Scanned or digital payroll documents

---

## 🔍 What Gets Compared?

The auditor automatically detects and compares:

### Employee Information
- Employee Name
- Employee ID
- Pay Date
- Pay Period

### Hours Worked
- Regular Hours
- Overtime Hours
- PTO/Vacation Hours
- Sick Hours

### Earnings
- Gross Pay
- Net Pay
- Tips (Cash)
- Tips (Paycheck)

### Taxes & Deductions
- Federal Income Tax
- Social Security / FICA
- Medicare
- State Income Tax
- Local/City Tax
- PFML (Paid Family Medical Leave)

---

## 📊 Understanding Results

### Summary Statistics
```
Total Rows Compared:    150
Matching Rows:          142 (94.7%)
Different Rows:         8 (5.3%)
Missing in File 1:      0
Missing in File 2:      0
```

### Detailed Differences
```
Row 5 - Employee: John Doe
  • Regular Hours: 40.0 → 42.0 (Δ +2.0)
  • Gross Pay: $800.00 → $840.00 (Δ +$40.00)
```

### Color Coding (HTML Reports)
- 🟢 **Green** - Matching values
- 🔴 **Red** - Different values
- 🟡 **Yellow** - Missing data

---

## 🎯 Common Use Cases

### 1. Verify Payroll Between Systems
```bash
# Compare QuickBooks export vs ADP export
python3 universal_payroll_auditor.py quickbooks_payroll.xlsx adp_payroll.csv
```

### 2. Monthly Audit
```bash
# Compare this month vs last month
python3 universal_payroll_auditor.py payroll_jan.xlsx payroll_feb.xlsx
```

### 3. Pre-Processing Check
```bash
# Compare draft vs final before submitting
python3 universal_payroll_auditor.py payroll_draft.csv payroll_final.csv
```

### 4. Compliance Audit
```bash
# Generate audit report for compliance
python3 universal_payroll_auditor.py file1.csv file2.csv --output audit_report.html
```

---

## 🔧 Advanced Usage

### Python Integration
```python
from universal_payroll_auditor import UniversalPayrollAuditor

# Create auditor instance
auditor = UniversalPayrollAuditor()

# Compare files
result = auditor.audit('file1.csv', 'file2.xlsx')

# Get summary
print(f"Match Rate: {result['summary']['match_percentage']:.1f}%")
print(f"Differences: {result['summary']['total_differences']}")

# Get differences
for diff in result['differences']:
    print(f"Row {diff['row']}: {diff['field']} changed")
```

### Custom Field Mapping
```python
auditor = UniversalPayrollAuditor(config={
    'custom_mappings': {
        'emp_name': ['Employee', 'Name', 'Worker'],
        'gross': ['Gross Pay', 'Total Earnings']
    }
})
```

---

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution:** Use a different port
```bash
PORT=8080 python3 api_server.py
```

### Issue: "File not found"
**Solution:** Use full path or check current directory
```bash
python3 universal_payroll_auditor.py /full/path/to/file1.csv /full/path/to/file2.xlsx
```

### Issue: "Permission denied"
**Solution:** Check file permissions
```bash
chmod +r file1.csv file2.xlsx
```

---

## 📖 Documentation

- **README.md** - Full project overview
- **QUICKSTART.md** - 5-minute setup guide
- **INTEGRATION_EXAMPLES.md** - Code examples
- **DEPLOYMENT_GUIDE.md** - Production deployment
- **HOW_TO_USE.txt** - Step-by-step instructions

---

## 💡 Tips for Teams

### 1. Standardize File Naming
```
payroll_YYYY-MM-DD_system.xlsx
Example: payroll_2026-02-17_quickbooks.xlsx
```

### 2. Create Shared Scripts
Save common comparisons in a script:
```bash
#!/bin/bash
# monthly_audit.sh
python3 universal_payroll_auditor.py \
  /shared/payroll/current_month.xlsx \
  /shared/payroll/previous_month.xlsx \
  --output /shared/reports/monthly_audit.html
```

### 3. Automate with Cron
```bash
# Run audit every Monday at 9 AM
0 9 * * 1 /path/to/monthly_audit.sh
```

### 4. Share Reports
HTML reports can be:
- Emailed to stakeholders
- Uploaded to shared drive
- Archived for compliance

---

## 🔒 Security Best Practices

1. **Don't commit payroll data to Git**
   - Add to `.gitignore`: `*.csv`, `*.xlsx`, `*.xls`

2. **Use secure file sharing**
   - Share files via encrypted channels
   - Use company file servers

3. **Clean up after audits**
   ```bash
   rm *.csv *.xlsx *.html  # Remove local copies
   ```

4. **Restrict repository access**
   - Make repo private if needed
   - Use GitHub teams for access control

---

## 🤝 Contributing

Found a bug or want to add a feature?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See **CONTRIBUTING.md** for details.

---

## 📞 Getting Help

- **Issues:** https://github.com/esoria25/payroll-auditor/issues
- **Discussions:** GitHub Discussions tab
- **Email:** Contact repository owner

---

## ⚡ Quick Reference Card

```bash
# Clone
git clone https://github.com/esoria25/payroll-auditor.git

# Install
pip install -r requirements.txt

# Web Interface
python3 api_server.py
# → http://localhost:8080

# Command Line
python3 universal_payroll_auditor.py file1.csv file2.xlsx

# Save Report
python3 universal_payroll_auditor.py file1.csv file2.xlsx --output report.html

# Docker
docker-compose up
# → http://localhost:5000
```

---

**Happy Auditing! 🎉**

Repository: https://github.com/esoria25/payroll-auditor

