# Universal Payroll Auditor - Integration Examples

## 1. As a Python Module

```python
from universal_payroll_auditor import UniversalPayrollAuditor

# Simple usage
auditor = UniversalPayrollAuditor()
results = auditor.audit('file1.csv', 'file2.csv')
print(f"Match rate: {results['summary']['match_rate']:.2f}%")

# With custom configuration
config = {
    'numeric_tolerance': 0.001,
    'field_mappings': {
        'custom_field': ['custom', 'my_field']
    }
}
auditor = UniversalPayrollAuditor(config)
results = auditor.compare_files('file1.csv', 'file2.csv', verbose=False)

# Get specific data
summary = auditor.get_summary()
differences = auditor.get_differences(limit=50)
```

## 2. As a CLI Tool

```bash
# Basic comparison
python3 universal_payroll_auditor.py file1.csv file2.csv

# Generate HTML report
python3 universal_payroll_auditor.py file1.csv file2.csv -o report.html -f html

# Custom tolerance
python3 universal_payroll_auditor.py file1.csv file2.csv -t 0.001 -f json
```

## 3. Integration with Goose

```python
# In your Goose extension or script
import sys
sys.path.append('/path/to/auditor')
from universal_payroll_auditor import UniversalPayrollAuditor

def audit_payroll_files(file1: str, file2: str) -> dict:
    """Goose-compatible function"""
    auditor = UniversalPayrollAuditor()
    return auditor.audit(file1, file2)

# Usage in Goose
result = audit_payroll_files('payroll_jan.csv', 'payroll_feb.csv')
print(f"Found {result['summary']['rows_with_differences']} differences")
```

## 4. As a REST API (Flask)

```python
from flask import Flask, request, jsonify
from universal_payroll_auditor import UniversalPayrollAuditor
import tempfile
import os

app = Flask(__name__)

@app.route('/audit', methods=['POST'])
def audit_files():
    # Get uploaded files
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    # Save temporarily
    with tempfile.TemporaryDirectory() as tmpdir:
        path1 = os.path.join(tmpdir, file1.filename)
        path2 = os.path.join(tmpdir, file2.filename)
        file1.save(path1)
        file2.save(path2)
        
        # Audit
        auditor = UniversalPayrollAuditor()
        results = auditor.audit(path1, path2)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
```

## 5. Batch Processing Script

```python
from universal_payroll_auditor import UniversalPayrollAuditor
from pathlib import Path
import json

def batch_audit(directory: str, pattern: str = "*.csv"):
    """Audit all matching files in directory"""
    auditor = UniversalPayrollAuditor()
    results = []
    
    files = sorted(Path(directory).glob(pattern))
    
    for i in range(len(files) - 1):
        file1 = str(files[i])
        file2 = str(files[i + 1])
        
        print(f"Comparing {files[i].name} vs {files[i+1].name}")
        result = auditor.audit(file1, file2)
        
        results.append({
            'file1': files[i].name,
            'file2': files[i+1].name,
            'match_rate': result['summary']['match_rate'],
            'differences': result['summary']['rows_with_differences']
        })
    
    return results

# Usage
results = batch_audit('./payroll_data/')
print(json.dumps(results, indent=2))
```

## 6. Integration with Data Pipeline

```python
# Apache Airflow DAG example
from airflow import DAG
from airflow.operators.python import PythonOperator
from universal_payroll_auditor import UniversalPayrollAuditor
from datetime import datetime

def audit_task(**context):
    auditor = UniversalPayrollAuditor()
    result = auditor.audit(
        '/data/payroll_current.csv',
        '/data/payroll_previous.csv'
    )
    
    # Push to XCom
    context['task_instance'].xcom_push(
        key='audit_result',
        value=result['summary']
    )
    
    # Alert if match rate is low
    if result['summary']['match_rate'] < 95:
        raise ValueError(f"Low match rate: {result['summary']['match_rate']:.2f}%")

with DAG('payroll_audit', start_date=datetime(2024, 1, 1)) as dag:
    audit = PythonOperator(
        task_id='audit_payroll',
        python_callable=audit_task
    )
```

## 7. As a Jupyter Notebook Widget

```python
from universal_payroll_auditor import UniversalPayrollAuditor
import ipywidgets as widgets
from IPython.display import display, HTML

def create_audit_widget():
    file1_input = widgets.Text(description='File 1:')
    file2_input = widgets.Text(description='File 2:')
    button = widgets.Button(description='Audit')
    output = widgets.Output()
    
    def on_button_click(b):
        with output:
            output.clear_output()
            auditor = UniversalPayrollAuditor()
            result = auditor.audit(file1_input.value, file2_input.value)
            
            html = auditor.generate_report(format='html')
            display(HTML(html))
    
    button.on_click(on_button_click)
    display(file1_input, file2_input, button, output)

create_audit_widget()
```

## 8. Scheduled Monitoring Script

```python
#!/usr/bin/env python3
"""
Scheduled payroll audit monitor
Run with: python3 monitor.py
"""

from universal_payroll_auditor import UniversalPayrollAuditor
import schedule
import time
from datetime import datetime

def daily_audit():
    """Run daily audit"""
    print(f"\n[{datetime.now()}] Running daily payroll audit...")
    
    auditor = UniversalPayrollAuditor()
    result = auditor.audit(
        '/data/payroll_today.csv',
        '/data/payroll_yesterday.csv'
    )
    
    # Save report
    report_name = f"audit_{datetime.now().strftime('%Y%m%d')}.html"
    auditor.generate_report(report_name, format='html')
    
    # Send alert if issues found
    if result['summary']['match_rate'] < 98:
        send_alert(result)
    
    print(f"✓ Audit complete. Match rate: {result['summary']['match_rate']:.2f}%")

def send_alert(result):
    """Send alert for low match rate"""
    # Implement email/Slack notification
    pass

# Schedule daily at 9 AM
schedule.every().day.at("09:00").do(daily_audit)

print("Payroll audit monitor started...")
while True:
    schedule.run_pending()
    time.sleep(60)
```

## Key Features for Integration:

1. **No dependencies on specific frameworks** - Pure Python with pandas
2. **Configurable** - Pass config dict for custom behavior
3. **Multiple output formats** - JSON, HTML, text
4. **API-style methods** - `audit()`, `get_summary()`, `get_differences()`
5. **Error handling** - Returns structured error messages
6. **Verbose control** - Silent mode for automated systems
7. **Extensible** - Easy to add custom field mappings

## Installation for Integration:

```bash
# Copy to your project
cp universal_payroll_auditor.py /your/project/

# Or install as package
pip install -e .

# Or add to requirements.txt
echo "pandas>=2.0.0" >> requirements.txt
echo "numpy>=1.24.0" >> requirements.txt
```
