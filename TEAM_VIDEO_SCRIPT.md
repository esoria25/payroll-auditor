# 🎥 Team Training Video Script

**Duration:** 5 minutes
**Audience:** Team members who will use the auditor

---

## Scene 1: Introduction (0:00 - 0:30)

**Narration:**
> "Hi team! This quick tutorial shows you how to use our Payroll Auditor to compare and verify payroll files. Whether you're in HR, accounting, or operations, this tool will save you hours of manual work."

**Show:**
- GitHub repository page
- Tool features overview

---

## Scene 2: Setup (0:30 - 1:30)

**Narration:**
> "First, let's get set up. Open your terminal and run these three commands."

**Show terminal:**
```bash
git clone https://github.com/esoria25/payroll-auditor.git
cd payroll-auditor
pip install -r requirements.txt
```

**Narration:**
> "That's it! You're ready to go. You only need to do this once."

---

## Scene 3: Web Interface Demo (1:30 - 3:00)

**Narration:**
> "The easiest way to use the auditor is through the web interface. Just start the server..."

**Show terminal:**
```bash
python3 api_server.py
```

**Narration:**
> "...and open your browser to localhost:8080."

**Show browser:**
- Navigate to http://localhost:8080
- Drag first payroll file
- Drag second payroll file
- Click "Compare Files"

**Narration:**
> "In seconds, you get a detailed comparison showing exactly what changed. Green means matching, red shows differences."

**Show results:**
- Summary statistics
- Detailed differences table
- Highlight specific changes

---

## Scene 4: Command Line (3:00 - 4:00)

**Narration:**
> "For automation or batch processing, use the command line."

**Show terminal:**
```bash
python3 universal_payroll_auditor.py january.xlsx february.xlsx --output report.html
```

**Narration:**
> "This generates a professional HTML report you can share with stakeholders or archive for compliance."

**Show:**
- HTML report opening in browser
- Professional formatting

---

## Scene 5: Best Practices (4:00 - 4:45)

**Narration:**
> "A few tips: First, use consistent file naming. Second, never commit payroll data to Git. And third, share reports securely through your company's approved channels."

**Show text:**
- File naming: payroll_YYYY-MM-DD_system.xlsx
- Security: Don't commit sensitive data
- Sharing: Use secure channels

---

## Scene 6: Closing (4:45 - 5:00)

**Narration:**
> "That's it! You're ready to start auditing. Check the documentation for advanced features, and reach out if you have questions. Happy auditing!"

**Show:**
- GitHub repository link
- Documentation links
- Contact information

