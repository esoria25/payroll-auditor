# 🎬 Demo Guide

## Quick Demo in 3 Steps

### Step 1: Generate Sample Data
```bash
python3 generate_sample_data.py
```

This creates:
- `sample_original.csv` - Original payroll data with 50 employees
- `sample_modified.csv` - Modified version with intentional changes

### Step 2: Run Comparison
```bash
python3 universal_payroll_auditor.py sample_original.csv sample_modified.csv --output demo_report.html
```

### Step 3: View Results
Open `demo_report.html` in your browser to see:
- Side-by-side comparison
- Highlighted differences
- Summary statistics
- Detailed change log

---

## Web Interface Demo

### Start the Server
```bash
python3 api_server.py
```

### Try It Out
1. Open http://localhost:8080
2. Drag and drop `sample_original.csv` and `sample_modified.csv`
3. Click "Compare Files"
4. View interactive results

---

## Video Demo Script

If you want to create a video demo:

### 1. Introduction (15 seconds)
- Show GitHub repository page
- Highlight star count and features

### 2. Installation (30 seconds)
```bash
git clone https://github.com/esoria25/payroll-auditor.git
cd payroll-auditor
pip install -r requirements.txt
```

### 3. Generate Sample Data (15 seconds)
```bash
python3 generate_sample_data.py
```

### 4. Web Interface Demo (60 seconds)
- Start server: `python3 api_server.py`
- Open browser to http://localhost:8080
- Upload two sample files
- Show comparison results
- Highlight key features:
  - Differences count
  - Side-by-side view
  - Summary statistics

### 5. Command Line Demo (30 seconds)
```bash
python3 universal_payroll_auditor.py sample_original.csv sample_modified.csv
```
- Show terminal output
- Open generated HTML report

### 6. Closing (15 seconds)
- Show GitHub repo again
- Call to action: "Star the repo!"
- Show documentation links

**Total Time: ~2.5 minutes**

---

## Screenshot Checklist

For the README, capture these screenshots:

- [ ] **web-interface.png**: Home page at http://localhost:8080
- [ ] **upload.png**: File upload area (drag-and-drop zone)
- [ ] **results.png**: Comparison results with differences
- [ ] **summary.png**: Summary statistics section
- [ ] **cli-output.png**: Terminal showing command line usage

Save all screenshots to `docs/images/` directory.

---

## Live Demo Data

The sample data includes realistic payroll scenarios:

- 50 employees
- Various pay rates ($15-$50/hour)
- Different hour types (regular, overtime, PTO, sick)
- Tax calculations (Federal, State, Social Security, Medicare)
- Intentional discrepancies for demonstration

### Types of Changes in Sample Data:
- Hours modified (±1-5 hours)
- Pay rates adjusted (±$2-$5)
- Tax amounts recalculated
- Tips added/removed
- Some employees added/removed

This demonstrates the tool's ability to catch various types of payroll errors.

