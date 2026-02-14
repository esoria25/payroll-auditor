#!/bin/bash
# Quick Deployment Script for Payroll Auditor

echo "🚀 Payroll Auditor - Quick Deployment"
echo "======================================"
echo ""
echo "Choose deployment option:"
echo "1. Local Python (current setup)"
echo "2. Docker container"
echo "3. Web API (Flask)"
echo "4. Standalone executable"
echo "5. AWS Lambda"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "✅ Already set up! You can use it now."
        echo "Test with: python3 universal_payroll_auditor.py file1.csv file2.csv"
        ;;
    2)
        echo "🐳 Creating Docker deployment..."
        cat > Dockerfile << 'EOF'
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py .
ENTRYPOINT ["python", "universal_payroll_auditor.py"]
EOF
        echo "✅ Dockerfile created!"
        echo "Build with: docker build -t payroll-auditor ."
        echo "Run with: docker run -v $(pwd):/data payroll-auditor /data/file1.csv /data/file2.csv"
        ;;
    3)
        echo "🌐 Creating web API..."
        cat > api_server.py << 'EOF'
from flask import Flask, request, jsonify
from universal_payroll_auditor import UniversalPayrollAuditor
import tempfile
import os

app = Flask(__name__)

@app.route('/audit', methods=['POST'])
def audit():
    files = request.files
    file1 = files['file1']
    file2 = files['file2']
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path1 = os.path.join(tmpdir, file1.filename)
        path2 = os.path.join(tmpdir, file2.filename)
        file1.save(path1)
        file2.save(path2)
        
        auditor = UniversalPayrollAuditor()
        result = auditor.audit(path1, path2)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
        echo "✅ API server created!"
        echo "Install Flask: pip install flask"
        echo "Run with: python api_server.py"
        echo "Access at: http://localhost:5000/audit"
        ;;
    4)
        echo "📦 Creating standalone executable..."
        pip install pyinstaller
        pyinstaller --onefile --name payroll-auditor universal_payroll_auditor.py
        echo "✅ Executable created in dist/ folder!"
        echo "Distribute the file in dist/payroll-auditor"
        ;;
    5)
        echo "☁️ Creating AWS Lambda deployment..."
        mkdir -p lambda_package
        pip install -t lambda_package pandas numpy
        cp universal_payroll_auditor.py lambda_package/
        cat > lambda_package/lambda_function.py << 'EOF'
import json
from universal_payroll_auditor import UniversalPayrollAuditor

def lambda_handler(event, context):
    auditor = UniversalPayrollAuditor()
    result = auditor.audit(event['file1'], event['file2'])
    return {
        'statusCode': 200,
        'body': json.dumps(result, default=str)
    }
EOF
        cd lambda_package && zip -r ../lambda_deployment.zip . && cd ..
        echo "✅ Lambda package created: lambda_deployment.zip"
        echo "Upload to AWS Lambda console or use AWS CLI"
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac
