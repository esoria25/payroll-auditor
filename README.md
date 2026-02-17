# 🔍 Payroll Auditor

**A powerful, universal tool for comparing and auditing payroll data across CSV, Excel, and PDF files.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

---

## ✨ Features

- 🔄 **Multi-Format Support**: Compare CSV, Excel (.xlsx, .xls), and PDF files
- 🎯 **Payroll-Specific**: Tracks pay dates, hours, tips, taxes, and more
- 🌐 **Web Interface**: Beautiful drag-and-drop UI for easy comparisons
- 🐳 **Docker Ready**: One-command deployment with Docker Compose
- 📊 **Detailed Reports**: HTML, JSON, and text output formats
- 🦆 **Goose Integration**: Works seamlessly with Goose Desktop
- ⚡ **Batch Processing**: Compare multiple file pairs automatically
- 🔧 **CLI & API**: Use via command line, REST API, or Python module

---

## 🚀 Quick Start

### Option 1: Web Interface (Easiest!)

```bash
git clone https://github.com/esoria25/payroll-auditor.git
cd payroll-auditor
pip install -r requirements.txt
python3 api_server.py
```

Open **http://localhost:8080** and start auditing!

![Web Interface Demo](docs/images/web-interface.png)

### Option 2: Docker (No Setup Required!)

```bash
git clone https://github.com/esoria25/payroll-auditor.git
cd payroll-auditor
docker-compose up
```

Access at **http://localhost:5000**

### Option 3: Command Line

```bash
python3 universal_payroll_auditor.py file1.csv file2.xlsx --output report.html
```

---

## 📋 Supported Payroll Fields

The auditor automatically detects and compares:

| Category | Fields |
|----------|--------|
| **Employee Info** | Name, Employee ID |
| **Time** | Pay Date, Pay Period |
| **Hours** | Regular Hours, Overtime, PTO, Sick Hours |
| **Earnings** | Gross Pay, Net Pay, Tips (Cash/Paycheck) |
| **Taxes** | Federal Income Tax, Social Security, Medicare, State Tax, Local Tax, PFML |

---

## 📸 Screenshots

### Web Interface
![Upload Files](docs/images/upload.png)
*Drag and drop your payroll files*

### Comparison Results
![Results View](docs/images/results.png)
*Detailed side-by-side comparison with highlights*

### Summary Statistics
![Summary Stats](docs/images/summary.png)
*Quick overview of differences found*

---

## 🎯 Use Cases

- ✅ **Payroll Verification**: Compare payroll reports from different systems
- ✅ **Audit Compliance**: Verify tax calculations and deductions
- ✅ **Data Migration**: Ensure accuracy when switching payroll providers
- ✅ **Quality Assurance**: Catch errors before processing payments
- ✅ **Historical Analysis**: Compare payroll data across time periods

---

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[Integration Examples](INTEGRATION_EXAMPLES.md)** - Use in Python, API, or Goose
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Deploy to cloud, Docker, or local
- **[Goose Usage](GOOSE_USAGE_GUIDE.md)** - Integrate with Goose Desktop
- **[GitHub Usage](GITHUB_USAGE_GUIDE.md)** - How to use from GitHub

---

## 🛠️ Installation

### Requirements
- Python 3.8+
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Or Install as Package

```bash
pip install git+https://github.com/esoria25/payroll-auditor.git
```

---

## 💻 Usage Examples

### 1. Web Interface

```bash
python3 api_server.py
```

### 2. Command Line

```bash
# Basic comparison
python3 universal_payroll_auditor.py file1.csv file2.xlsx

# Save HTML report
python3 universal_payroll_auditor.py file1.csv file2.xlsx --output report.html

# JSON output
python3 universal_payroll_auditor.py file1.csv file2.xlsx --format json
```

### 3. Python Module

```python
from universal_payroll_auditor import UniversalPayrollAuditor

auditor = UniversalPayrollAuditor()
result = auditor.audit('payroll_jan.csv', 'payroll_feb.csv')

print(f"Differences found: {result['summary']['total_differences']}")
print(f"Match rate: {result['summary']['match_percentage']:.1f}%")
```

### 4. Batch Processing

```bash
python3 batch_audit.py
```

### 5. REST API

```bash
# Start API server
python3 api_server.py

# Use with curl
curl -X POST http://localhost:8080/api/audit \
  -F "file1=@payroll1.csv" \
  -F "file2=@payroll2.xlsx"
```

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Using Dockerfile

```bash
docker build -t payroll-auditor .
docker run -p 8080:5000 payroll-auditor
```

---

## 🧪 Testing

### Generate Sample Data

```bash
python3 generate_sample_data.py
```

### Run Test Audit

```bash
python3 universal_payroll_auditor.py sample_original.csv sample_modified.csv
```

---

## 📊 Example Output

```
╔══════════════════════════════════════════════════════════════════╗
║                    PAYROLL AUDIT REPORT                          ║
╚══════════════════════════════════════════════════════════════════╝

📊 SUMMARY STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Rows Compared:        150
Matching Rows:              142 (94.7%)
Different Rows:             8 (5.3%)
Missing in File 1:          0
Missing in File 2:          0

⚠️  DIFFERENCES FOUND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Row 5 - Employee: John Doe
  • Regular Hours: 40.0 → 42.0 (Δ +2.0)
  • Gross Pay: $800.00 → $840.00 (Δ +$40.00)

Row 12 - Employee: Jane Smith
  • Overtime Hours: 5.0 → 7.5 (Δ +2.5)
  • Federal Tax: $120.50 → $135.75 (Δ +$15.25)
```

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute:
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with Python, Flask, Pandas, and OpenPyXL
- Designed for Block's payroll auditing needs
- Integrated with Goose Desktop

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/esoria25/payroll-auditor/issues)
- **Documentation**: Check the `docs/` folder
- **Quick Help**: See [HOW_TO_USE.txt](HOW_TO_USE.txt)

---

## ⭐ Star This Repo!

If you find this tool useful, please give it a star! ⭐

---

**Made with ❤️ for better payroll auditing**

