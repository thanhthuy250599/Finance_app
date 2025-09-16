# 🚀 Hướng dẫn Deploy Finance App

## 📋 Chuẩn bị Production

### 1. Environment Setup
```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Tạo file .env
echo "SECRET_KEY=your-secret-key-here" > .env
echo "GEMINI_API_KEY=your-gemini-api-key" >> .env
echo "DEBUG=False" >> .env
```

### 3. Data Directory
```bash
# Tạo thư mục data
mkdir -p data
mkdir -p data/user_data
mkdir -p config

# Set permissions
chmod 755 data
chmod 755 data/user_data
chmod 755 config
```

## 🐳 Docker Deployment

### 1. Build Image
```bash
docker build -t finance-app:latest .
```

### 2. Run Container
```bash
# Development
docker run -p 8000:8000 -v $(pwd)/data:/app/data finance-app:latest

# Production
docker run -d \
  --name finance-app \
  -p 80:8000 \
  -v /opt/finance-app/data:/app/data \
  -e SECRET_KEY=your-secret-key \
  finance-app:latest
```

### 3. Docker Compose
```yaml
version: '3.8'
services:
  finance-app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - SECRET_KEY=your-secret-key
      - DEBUG=False
    restart: unless-stopped
```

## ☁️ Cloud Deployment

### 1. Heroku
```bash
# Cài đặt Heroku CLI
# Tạo Procfile
echo "web: uvicorn finance_app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 2. Railway
```bash
# Cài đặt Railway CLI
npm install -g @railway/cli

# Login và deploy
railway login
railway init
railway up
```

### 3. DigitalOcean App Platform
```yaml
# .do/app.yaml
name: finance-app
services:
- name: web
  source_dir: /
  github:
    repo: your-username/finance-app
    branch: main
  run_command: uvicorn finance_app.main:app --host 0.0.0.0 --port 8080
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: SECRET_KEY
    value: your-secret-key
```

### 4. AWS EC2
```bash
# Cài đặt dependencies
sudo apt update
sudo apt install python3-pip nginx

# Clone và setup
git clone your-repo
cd finance-app
pip3 install -r requirements.txt

# Setup systemd service
sudo nano /etc/systemd/system/finance-app.service
```

```ini
[Unit]
Description=Finance App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/finance-app
Environment=PATH=/home/ubuntu/finance-app/venv/bin
ExecStart=/home/ubuntu/finance-app/venv/bin/uvicorn finance_app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl enable finance-app
sudo systemctl start finance-app

# Setup Nginx
sudo nano /etc/nginx/sites-available/finance-app
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/finance-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 Security Setup

### 1. SSL Certificate
```bash
# Sử dụng Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 2. Firewall
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 3. Environment Variables
```bash
# Tạo file .env production
cat > .env << EOF
SECRET_KEY=your-super-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=sqlite:///data/app.db
EOF
```

## 📊 Monitoring & Logging

### 1. Logging Setup
```python
# Thêm vào main.py
import logging
from logging.handlers import RotatingFileHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/app.log', maxBytes=10000000, backupCount=5),
        logging.StreamHandler()
    ]
)
```

### 2. Health Check
```python
# Thêm endpoint health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
```

### 3. Monitoring với Prometheus
```bash
pip install prometheus-fastapi-instrumentator
```

```python
# Thêm vào main.py
from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)
```

## 🔄 CI/CD Pipeline

### 1. GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Deploy to server
      run: |
        # Add your deployment commands here
        echo "Deploying to production..."
```

### 2. Docker Hub
```bash
# Build và push image
docker build -t your-username/finance-app:latest .
docker push your-username/finance-app:latest
```

## 📈 Performance Optimization

### 1. Gunicorn
```bash
pip install gunicorn
```

```bash
# Chạy với Gunicorn
gunicorn finance_app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 2. Redis Cache
```bash
pip install redis
```

```python
# Thêm Redis caching
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
```

### 3. Database Migration
```bash
# Nếu chuyển sang PostgreSQL
pip install psycopg2-binary alembic
alembic init alembic
```

## 🚨 Backup & Recovery

### 1. Data Backup
```bash
# Tạo script backup
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "backup_$DATE.tar.gz" data/
aws s3 cp "backup_$DATE.tar.gz" s3://your-backup-bucket/
EOF

chmod +x backup.sh
```

### 2. Automated Backup
```bash
# Crontab
0 2 * * * /path/to/backup.sh
```

## 📞 Troubleshooting

### Common Issues

1. **Port already in use**
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

2. **Permission denied**
```bash
sudo chown -R $USER:$USER data/
chmod -R 755 data/
```

3. **Module not found**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

4. **Memory issues**
```bash
# Tăng swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## ✅ Checklist Deploy

- [ ] Environment variables configured
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Monitoring setup
- [ ] Backup strategy implemented
- [ ] Health checks working
- [ ] Performance optimized
- [ ] Security hardened
- [ ] Documentation updated
- [ ] Team trained

---

**🎉 Ứng dụng đã sẵn sàng production!**



