#!/bin/bash

echo "🎬 Creating Demo for Payroll Auditor"
echo "===================================="
echo ""

# Generate sample data
echo "📊 Generating sample payroll data..."
python3 generate_sample_data.py

echo ""
echo "🔍 Running comparison..."
python3 universal_payroll_auditor.py sample_original.csv sample_modified.csv --output demo_report.html

echo ""
echo "✅ Demo created!"
echo ""
echo "📋 Files created:"
echo "  • sample_original.csv - Original payroll data"
echo "  • sample_modified.csv - Modified payroll data"
echo "  • demo_report.html - Comparison report"
echo ""
echo "🌐 Open demo_report.html in your browser to see the results!"
echo ""
echo "📸 To create screenshots for GitHub:"
echo "  1. Run: python3 api_server.py"
echo "  2. Open: http://localhost:8080"
echo "  3. Take screenshots (Cmd+Shift+4 on Mac)"
echo "  4. Save to: docs/images/"
