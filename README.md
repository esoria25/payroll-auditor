# 🔍 Payroll Auditor

A comprehensive tool for auditing and comparing payroll data files. Supports CSV, Excel, and PDF formats with detailed difference reporting.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

- 📊 **Multi-format Support**: CSV, Excel (.xlsx, .xls), and PDF files
- 🔍 **Smart Comparison**: Automatic field detection and normalization
- 📈 **Detailed Reports**: HTML, JSON, and text output formats
- 🌐 **Web Interface**: Beautiful drag-and-drop UI
- 🐳 **Docker Ready**: Containerized deployment
- 🦆 **Goose Integration**: Works with Goose automation
- 🚀 **API Endpoint**: REST API for programmatic access

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/payroll-auditor.git
cd payroll-auditor

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Command line
python universal_payroll_auditor.py file1.csv file2.csv

# Generate HTML report
python universal_payroll_auditor.py file1.csv file2.csv -o report.html -f html

# Start web interface
python api_server.py
# Open http://localhost:5000
```

### Python API

```python
from universal_payroll_auditor import UniversalPayrollAuditor

auditor = UniversalPayrollAuditor()
result = auditor.audit('payroll1.csv', 'payroll2.csv')

print(f"Match rate: {result['summary']['match_rate']:.2f}%")
```

## 📋 Supported Fields

Automatically detects and compares:
- Employee information
- Pay dates
- Hours (regular, overtime, PTO, sick)
- Tips (cash and paycheck)
- Taxes (Federal, Social Security, Medicare, State, Local, PFML)

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:5000
```

## 📖 Documentation

- [Quick Start Guide](QUICKSTART.md)
- [API Documentation](INTEGRATION_EXAMPLES.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [How to Use](HOW_TO_USE.txt)

## 🎯 Use Cases

- **Payroll Validation**: Compare old vs new payroll systems
- **Data Migration**: Verify data transfer accuracy
- **Monthly Audits**: Automated payroll checking
- **Compliance**: Track and document changes
- **Quality Assurance**: Catch errors before processing

## 🔧 Requirements

- Python 3.8+
- pandas >= 2.0.0
- numpy >= 1.24.0
- openpyxl >= 3.1.0 (for Excel support)
- flask >= 2.3.0 (for web interface)
- pdfplumber >= 0.9.0 (for PDF support)

## 📊 Example Output

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

✅ EXCELLENT - High match rate!

🔍 Field Differences:
   • overtime: 5 differences (Avg: 2.50)
   • federal_tax: 3 differences (Avg: 15.30)
============================================================
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and pandas
- Web interface powered by Flask
- Docker support for easy deployment

## 📧 Contact

Your Name - [@yourhandle](https://twitter.com/yourhandle)

Project Link: [https://github.com/YOUR_USERNAME/payroll-auditor](https://github.com/YOUR_USERNAME/payroll-auditor)

---

⭐ Star this repo if you find it helpful!
