#!/bin/bash
# Deployment script for Payroll Auditor API

set -e

echo "🚀 Deploying Payroll Auditor API with Docker"
echo "=============================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

echo "✅ Docker and docker-compose are installed"
echo ""

# Build the Docker image
echo "📦 Building Docker image..."
docker-compose build

echo ""
echo "✅ Docker image built successfully"
echo ""

# Start the containers
echo "🚀 Starting containers..."
docker-compose up -d

echo ""
echo "✅ Containers started successfully"
echo ""

# Wait for service to be healthy
echo "⏳ Waiting for service to be healthy..."
sleep 5

# Check health
if curl -f http://localhost:5000/health &> /dev/null; then
    echo "✅ Service is healthy!"
else
    echo "⚠️  Service may not be ready yet. Check logs with: docker-compose logs"
fi

echo ""
echo "=============================================="
echo "🎉 Deployment Complete!"
echo "=============================================="
echo ""
echo "📍 Web Interface: http://localhost:5000"
echo "📍 API Endpoint:  http://localhost:5000/api/audit"
echo "📍 Health Check:  http://localhost:5000/health"
echo "📍 API Docs:      http://localhost:5000/api/docs"
echo ""
echo "📋 Useful commands:"
echo "  View logs:     docker-compose logs -f"
echo "  Stop service:  docker-compose down"
echo "  Restart:       docker-compose restart"
echo "  Rebuild:       docker-compose up -d --build"
echo ""
echo "🧪 Test the API:"
echo "  curl http://localhost:5000/health"
echo "  curl -X POST http://localhost:5000/api/audit \\"
echo "    -F 'file1=@your_file1.csv' \\"
echo "    -F 'file2=@your_file2.csv'"
echo ""
