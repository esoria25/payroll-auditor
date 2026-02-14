# Quick Start Guide

## Installation (5 minutes)

1. **Install Python** (if not already installed)
   - Download from https://www.python.org/downloads/
   - Version 3.8 or higher required

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python payroll_auditor.py --help
   ```

## Test with Sample Data (2 minutes)

1. **Generate sample data**
   ```bash
   python generate_sample_data.py
   ```
   
   This creates:
   - `payroll_original.csv` (20 employees)
   - `payroll_corrected.csv` (same data with 8 modifications)
   - `payroll_original.xlsx` (Excel version)

2. **Run your first audit**
   ```bash
   python payroll_auditor.py payroll_original.csv payroll_corrected.csv
   ```

3. **Generate HTML report**
   ```bash
   python payroll_auditor.py payroll_original.csv payroll_corrected.csv -o report.html -f html
   ```
   
   Open `report.html` in your browser to see the results!

## Using with Your Own Data (5 minutes)

### Option 1: Command Line

```bash
# Compare two CSV files
python payroll_auditor.py your_file1.csv your_file2.csv

# Save report
python payroll_auditor.py your_file1.csv your_file2.csv -o audit_report.html -f html
```

### Option 2: Python Script

Create a file called `my_audit.py`:

```python
from payroll_auditor import PayrollAuditor

auditor = PayrollAuditor()
results = auditor.compare_files('january_payroll.csv', 'january_corrected.csv')
auditor.generate_report('january_audit.html', format='html')

print(f"Match rate: {results['summary']['match_rate']:.2f}%")
```

Run it:
```bash
python my_audit.py
```

## Batch Processing Multiple Files (10 minutes)

1. **Organize your files**
   ```
   payroll_data/
   ├── january_original.csv
   ├── january_corrected.csv
   ├── february_original.xlsx
   ├── february_corrected.xlsx
   └── march_original.csv
       march_corrected.csv
   ```

2. **Run batch audit**
   ```bash
   python batch_audit.py payroll_data/
   ```

3. **View results**
   - Individual HTML reports for each comparison
   - Summary table showing all match rates
   - Overall statistics

## Common Use Cases

### Case 1: Compare Old vs New Payroll System
```bash
python payroll_auditor.py old_system_export.csv new_system_export.xlsx -o migration_audit.html -f html
```

### Case 2: Verify Payroll Corrections
```bash
python payroll_auditor.py original_payroll.csv corrected_payroll.csv -o corrections_audit.txt
```

### Case 3: Monthly Payroll Validation
```python
from payroll_auditor import PayrollAuditor

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
auditor = PayrollAuditor()

for month in months:
    results = auditor.compare_files(
        f'{month}_draft.csv',
        f'{month}_final.csv'
    )
    auditor.generate_report(f'{month}_audit.html', format='html')
    
    if results['summary']['match_rate'] < 95:
        print(f"⚠ WARNING: {month} has low match rate: {results['summary']['match_rate']:.2f}%")
```

## Tips for Success

1. **Column Names**: Make sure your files have similar column names (e.g., "Employee Name" or "employee")

2. **Employee IDs**: Include an employee identifier for accurate matching

3. **Clean Data**: Remove extra spaces and special characters

4. **File Formats**: CSV is fastest, Excel is most common, PDF works but is slower

5. **Large Files**: For 10,000+ rows, consider splitting into batches

## Troubleshooting

**Problem**: "No common columns found"
- **Solution**: Check column names match between files. Add custom mappings if needed.

**Problem**: "PDF support disabled"
- **Solution**: Run `pip install pdfplumber`

**Problem**: "Excel support limited"
- **Solution**: Run `pip install openpyxl`

**Problem**: Too many differences shown
- **Solution**: The tool shows first 20 by default. Check the summary statistics for totals.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize field mappings for your specific column names
- Integrate into your payroll workflow
- Set up automated batch processing

## Getting Help

- Review the code comments in `payroll_auditor.py`
- Check the examples in `batch_audit.py`
- Modify the tool to fit your specific needs

Happy auditing! 🎯
