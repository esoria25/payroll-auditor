# 🚀 Payroll Auditor - Quick Reference

**Repository:** https://github.com/esoria25/payroll-auditor

---

## 📥 Setup (One Time)

```bash
git clone https://github.com/esoria25/payroll-auditor.git
cd payroll-auditor
pip install -r requirements.txt
```

---

## 🌐 Web Interface (Easiest)

```bash
python3 api_server.py
```
Open: **http://localhost:8080**

Drag & drop two files → Click "Compare Files"

---

## 💻 Command Line

```bash
# Basic comparison
python3 universal_payroll_auditor.py file1.csv file2.xlsx

# Save HTML report
python3 universal_payroll_auditor.py file1.csv file2.xlsx --output report.html

# JSON output
python3 universal_payroll_auditor.py file1.csv file2.xlsx --format json
```

---

## 📋 Supported Files

✅ CSV  ✅ Excel (.xlsx, .xls)  ✅ PDF

---

## 🔍 What's Compared

✅ Employee info  ✅ Hours (regular, OT, PTO, sick)
✅ Pay amounts  ✅ Taxes (Federal, SS, Medicare, State, Local)
✅ Tips  ✅ Deductions

---

## 🐳 Docker (Alternative)

```bash
docker-compose up
```
Open: **http://localhost:5000**

---

## 📞 Help

Issues: https://github.com/esoria25/payroll-auditor/issues

