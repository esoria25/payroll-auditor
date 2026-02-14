#!/bin/bash
# GitHub Repository Setup Script

echo "🚀 Setting up GitHub repository for Payroll Auditor"
echo "=================================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Initialize git repository
echo "📦 Initializing git repository..."
git init

# Add all files
echo "📝 Adding files..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Payroll Auditor v1.0.0

Features:
- Multi-format support (CSV, Excel, PDF)
- Web interface with REST API
- Docker deployment
- Goose integration
- Comprehensive documentation"

echo ""
echo "✅ Local repository initialized!"
echo ""
echo "📋 Next steps:"
echo "1. Create a new repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Name it: payroll-auditor"
echo ""
echo "3. Run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/payroll-auditor.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Your tool will be live on GitHub! 🎉"
