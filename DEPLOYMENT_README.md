# 🚀 Payroll Auditor API - Docker Deployment

## Quick Start

### Prerequisites
- Docker installed
- docker-compose installed

### Deploy in 3 Steps

1. **Make deployment script executable:**
   ```bash
   chmod +x deploy.sh
   ```

2. **Run deployment:**
   ```bash
   ./deploy.sh
   ```

3. **Access the service:**
   - Web Interface: http://localhost:5000
   - API Endpoint: http://localhost:5000/api/audit

## Manual Deployment

### Build and Run

```bash
# Build the Docker image
docker-compose build

# Start the service
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Stop and Remove

```bash
# Stop the service
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Usage

### Web Interface

Open http://localhost:5000 in your browser and upload two files.

### API Usage

#### Health Check
```bash
curl http://localhost:5000/health
```

#### Audit Files
```bash
curl -X POST http://localhost:5000/api/audit \
  -F "file1=@payroll_jan.csv" \
  -F "file2=@payroll_feb.csv"
```

#### Python Example
```python
import requests

files = {
    'file1': open('payroll_jan.csv', 'rb'),
    'file2': open('payroll_feb.csv', 'rb')
}

response = requests.post('http://localhost:5000/api/audit', files=files)
result = response.json()

print(f"Match rate: {result['summary']['match_rate']:.2f}%")
```

#### JavaScript Example
```javascript
const formData = new FormData();
formData.append('file1', file1);
formData.append('file2', file2);

fetch('http://localhost:5000/api/audit', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## Configuration

### Environment Variables

Edit `docker-compose.yml` to add environment variables:

```yaml
environment:
  - FLASK_ENV=production
  - MAX_FILE_SIZE=16777216  # 16MB
  - LOG_LEVEL=INFO
```

### Port Configuration

Change the port in `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Access on port 8080
```

## Production Deployment

### With Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### With SSL (Let's Encrypt)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com
```

### Scale with Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml payroll-auditor

# Scale service
docker service scale payroll-auditor_api=3
```

## Monitoring

### View Logs
```bash
docker-compose logs -f
```

### Check Resource Usage
```bash
docker stats payroll-auditor
```

### Health Check
```bash
curl http://localhost:5000/health
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs

# Rebuild
docker-compose up -d --build
```

### Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - "5001:5000"
```

### Out of memory
```bash
# Increase memory limit in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 1G
```

## API Response Format

```json
{
  "metadata": {
    "file1": {"name": "file1.csv", "rows": 150, "columns": 15},
    "file2": {"name": "file2.csv", "rows": 150, "columns": 15}
  },
  "summary": {
    "total_rows_compared": 150,
    "rows_matched": 142,
    "rows_with_differences": 8,
    "match_rate": 94.67,
    "field_statistics": {...}
  },
  "data": {
    "differences": [...]
  },
  "api_metadata": {
    "timestamp": "2024-02-13T21:42:00",
    "api_version": "1.0.0"
  }
}
```

## Security Notes

- Files are processed in temporary directories and cleaned up automatically
- Maximum file size is 16MB (configurable)
- No files are stored permanently
- Use HTTPS in production
- Add authentication for production use

## Support

For issues or questions, check the logs:
```bash
docker-compose logs -f payroll-auditor-api
```
