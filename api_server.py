#!/usr/bin/env python3
"""
Payroll Auditor Web API
Flask-based REST API for payroll file auditing
"""

from flask import Flask, request, jsonify, send_file, render_template_string
from werkzeug.utils import secure_filename
from universal_payroll_auditor import UniversalPayrollAuditor
import os
import tempfile
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HTML template for web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Payroll Auditor API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .upload-section {
            margin: 30px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 5px;
        }
        .file-input {
            margin: 10px 0;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #45a049;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #e3f2fd;
            border-radius: 5px;
            display: none;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .api-docs {
            margin-top: 30px;
            padding: 20px;
            background: #fff3cd;
            border-radius: 5px;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
        }
        .stat-box {
            display: inline-block;
            margin: 10px;
            padding: 15px;
            background: white;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #1976d2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Payroll Auditor API</h1>
        <p>Upload two payroll files to compare and audit differences</p>
        
        <div class="upload-section">
            <h2>Upload Files</h2>
            <form id="auditForm" enctype="multipart/form-data">
                <div class="file-input">
                    <label>📄 File 1 (Original):</label><br>
                    <input type="file" name="file1" accept=".csv,.xlsx,.xls,.pdf" required>
                </div>
                <div class="file-input">
                    <label>📄 File 2 (Comparison):</label><br>
                    <input type="file" name="file2" accept=".csv,.xlsx,.xls,.pdf" required>
                </div>
                <br>
                <button type="submit">🚀 Run Audit</button>
            </form>
        </div>
        
        <div class="loading" id="loading">
            <h3>⏳ Processing audit...</h3>
        </div>
        
        <div class="result" id="result">
            <h2>📊 Audit Results</h2>
            <div id="resultContent"></div>
        </div>
        
        <div class="api-docs">
            <h2>📚 API Documentation</h2>
            <h3>Endpoints:</h3>
            <ul>
                <li><code>GET /</code> - This web interface</li>
                <li><code>GET /health</code> - Health check</li>
                <li><code>POST /api/audit</code> - Audit two files (multipart/form-data)</li>
                <li><code>GET /api/docs</code> - API documentation</li>
            </ul>
            
            <h3>Example cURL:</h3>
            <code>
                curl -X POST http://localhost:5000/api/audit \\<br>
                &nbsp;&nbsp;-F "file1=@payroll1.csv" \\<br>
                &nbsp;&nbsp;-F "file2=@payroll2.csv"
            </code>
        </div>
    </div>
    
    <script>
        document.getElementById('auditForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const resultContent = document.getElementById('resultContent');
            
            loading.style.display = 'block';
            result.style.display = 'none';
            
            try {
                const response = await fetch('/api/audit', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    const summary = data.summary;
                    resultContent.innerHTML = `
                        <div class="stat-box">
                            <div class="stat-value">${summary.total_rows_compared}</div>
                            <div>Total Rows</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${summary.rows_matched}</div>
                            <div>Matched</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${summary.rows_with_differences}</div>
                            <div>Differences</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-value">${summary.match_rate.toFixed(2)}%</div>
                            <div>Match Rate</div>
                        </div>
                        <br><br>
                        <h3>Status: ${summary.match_rate >= 95 ? '✅ Excellent' : 
                                      summary.match_rate >= 85 ? '⚠️ Warning' : '❌ Alert'}</h3>
                        <pre>${JSON.stringify(data, null, 2)}</pre>
                    `;
                    result.style.display = 'block';
                } else {
                    resultContent.innerHTML = `<p style="color: red;">❌ Error: ${data.error}</p>`;
                    result.style.display = 'block';
                }
            } catch (error) {
                resultContent.innerHTML = `<p style="color: red;">❌ Error: ${error.message}</p>`;
                result.style.display = 'block';
            } finally {
                loading.style.display = 'none';
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'payroll-auditor-api',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/docs')
def api_docs():
    """API documentation"""
    return jsonify({
        'service': 'Payroll Auditor API',
        'version': '1.0.0',
        'endpoints': {
            'GET /': 'Web interface',
            'GET /health': 'Health check',
            'POST /api/audit': 'Audit two payroll files',
            'GET /api/docs': 'This documentation'
        },
        'usage': {
            'audit': {
                'method': 'POST',
                'endpoint': '/api/audit',
                'content_type': 'multipart/form-data',
                'parameters': {
                    'file1': 'First payroll file (CSV, Excel, or PDF)',
                    'file2': 'Second payroll file (CSV, Excel, or PDF)'
                },
                'example': 'curl -X POST http://localhost:5000/api/audit -F "file1=@file1.csv" -F "file2=@file2.csv"'
            }
        },
        'supported_formats': ['csv', 'xlsx', 'xls', 'pdf']
    })

@app.route('/api/audit', methods=['POST'])
def audit_files():
    """
    Audit two payroll files
    
    Expects multipart/form-data with:
    - file1: First payroll file
    - file2: Second payroll file
    
    Returns JSON with audit results
    """
    # Check if files are present
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'Both file1 and file2 are required'}), 400
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    # Check if files have names
    if file1.filename == '' or file2.filename == '':
        return jsonify({'error': 'Both files must have filenames'}), 400
    
    # Check file types
    if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
        return jsonify({
            'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    try:
        # Create temporary directory for this request
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save uploaded files
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            path1 = os.path.join(tmpdir, filename1)
            path2 = os.path.join(tmpdir, filename2)
            
            file1.save(path1)
            file2.save(path2)
            
            # Perform audit
            auditor = UniversalPayrollAuditor()
            result = auditor.audit(path1, path2)
            
            # Add metadata
            result['api_metadata'] = {
                'file1_name': filename1,
                'file2_name': filename2,
                'timestamp': datetime.now().isoformat(),
                'api_version': '1.0.0'
            }
            
            return jsonify(result), 200
            
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting Payroll Auditor API...")
    print("📍 Access web interface: http://localhost:5000")
    print("📍 API endpoint: http://localhost:5000/api/audit")
    print("📍 Health check: http://localhost:5000/health")
    print("📍 API docs: http://localhost:5000/api/docs")
    app.run(host='0.0.0.0', port=9000, debug=False)
