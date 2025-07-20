# TrueFoundry Deployment Guide - Team 3A
# AgriWaste2Fuel - Annam.ai Internship Program 2025

## 🎯 TrueFoundry Overview

TrueFoundry is an enterprise MLOps platform that provides:
- ✅ Kubernetes-based auto-scaling
- ✅ Built-in ML model serving
- ✅ One-click deployments
- ✅ Database integration
- ✅ Monitoring & logging
- ✅ CI/CD pipelines
- ✅ GPU support for ML models

## 🏗️ Architecture for Team 3A

### Recommended Deployment Strategy:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   ML Service    │
│   (Vercel)      │◄──►│  (TrueFoundry)  │◄──►│  (TrueFoundry)  │
│                 │    │                 │    │                 │
│ - React App     │    │ - FastAPI       │    │ - ML Models     │
│ - Static Site   │    │ - Authentication│    │ - Image Proc    │
│ - CDN Cached    │    │ - Database      │    │ - GPU Support   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   PostgreSQL    │    │   File Storage  │
                       │  (TrueFoundry)  │    │  (TrueFoundry)  │
                       └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Deployment Steps

### Step 1: TrueFoundry CLI Setup
```bash
# Install TrueFoundry CLI
pip install truefoundry

# Login with Annam.ai credentials
tfy login

# Set workspace
tfy workspace set annam-ai-workspace
```

### Step 2: Project Creation
```bash
# Create Team 3A project
tfy project create agriwaste2fuel-team3a \
    --description "AI-powered agricultural waste to fuel conversion - Team 3A"
```

### Step 3: Database Deployment
```bash
# Deploy PostgreSQL database
tfy database deploy postgres \
    --name agriwaste-postgres \
    --version 14 \
    --storage 10Gi \
    --project agriwaste2fuel-team3a
```

### Step 4: Backend API Deployment
```bash
# Deploy FastAPI backend
tfy service deploy \
    --name api-service \
    --project agriwaste2fuel-team3a \
    --dockerfile Backend/Dockerfile \
    --context Backend/ \
    --port 8000 \
    --replicas 2 \
    --autoscale-min 1 \
    --autoscale-max 5 \
    --cpu-request 500m \
    --memory-request 512Mi \
    --cpu-limit 1000m \
    --memory-limit 1Gi
```

### Step 5: ML Model Deployment
```bash
# Deploy ML service with GPU support
tfy model deploy \
    --name ml-service \
    --project agriwaste2fuel-team3a \
    --dockerfile ML_Models/Dockerfile \
    --context ML_Models/ \
    --port 5000 \
    --replicas 1 \
    --gpu-request 1 \
    --cpu-request 1000m \
    --memory-request 2Gi
```

## 🔧 Configuration Files

### 1. Backend Dockerfile (Already created)
Location: `Backend/Dockerfile`
- Multi-stage build for optimization
- ML dependencies included
- Health checks configured
- Production-ready

### 2. ML Service Dockerfile
```dockerfile
# ML_Models/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for ML
RUN apt-get update && apt-get install -y \
    gcc g++ libpq-dev libgl1-mesa-glx \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    wget curl && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model files
COPY . .

# Create model directory
RUN mkdir -p /models

# Download pre-trained models (if needed)
# RUN wget -O /models/waste-classifier.pth "https://model-url"

ENV PYTHONPATH=/app
ENV PORT=5000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

EXPOSE $PORT

CMD ["python", "-m", "uvicorn", "ml_service.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

### 3. Frontend Production Dockerfile
```dockerfile
# Frontend/Dockerfile.prod
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

## 🔐 Environment Variables & Secrets

### Backend Environment Variables:
```env
# Production environment
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:pass@agriwaste-postgres:5432/agriwaste2fuel
FIREBASE_CONFIG=<firebase-config-json>
REDIS_URL=redis://redis:6379
AWS_ACCESS_KEY_ID=<aws-key>
AWS_SECRET_ACCESS_KEY=<aws-secret>
S3_BUCKET=agriwaste2fuel-images
SENTRY_DSN=<sentry-dsn>
```

### Setting Secrets in TrueFoundry:
```bash
# Database credentials
tfy secret create database-secrets \
    --project agriwaste2fuel-team3a \
    --from-literal DATABASE_URL="postgresql://user:pass@host:5432/db"

# Firebase configuration
tfy secret create firebase-secrets \
    --project agriwaste2fuel-team3a \
    --from-file FIREBASE_CONFIG=Backend/firebase-config.json

# AWS credentials
tfy secret create aws-secrets \
    --project agriwaste2fuel-team3a \
    --from-literal AWS_ACCESS_KEY_ID="your-key" \
    --from-literal AWS_SECRET_ACCESS_KEY="your-secret"
```

## 🌐 Domain & Ingress Configuration

### Setting up Custom Domains:
```bash
# API domain
tfy ingress create \
    --name api-ingress \
    --project agriwaste2fuel-team3a \
    --host api.agriwaste2fuel-team3a.annam.ai \
    --service api-service \
    --port 8000 \
    --enable-ssl

# ML service domain  
tfy ingress create \
    --name ml-ingress \
    --project agriwaste2fuel-team3a \
    --host ml.agriwaste2fuel-team3a.annam.ai \
    --service ml-service \
    --port 5000 \
    --enable-ssl
```

### Expected URLs:
- **API:** `https://api.agriwaste2fuel-team3a.annam.ai`
- **ML Service:** `https://ml.agriwaste2fuel-team3a.annam.ai`
- **Frontend:** Deploy on Vercel for better performance

## 📊 Monitoring & Logging

### Enable Monitoring:
```bash
# Enable comprehensive monitoring
tfy monitoring enable \
    --project agriwaste2fuel-team3a \
    --prometheus \
    --grafana \
    --alertmanager

# Set up alerts
tfy alert create \
    --name high-cpu \
    --project agriwaste2fuel-team3a \
    --condition "cpu_usage > 80%" \
    --action scale_up

tfy alert create \
    --name high-memory \
    --project agriwaste2fuel-team3a \
    --condition "memory_usage > 85%" \
    --action alert_team
```

### Logging Configuration:
```python
# Backend logging setup
import structlog
import logging

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

## 🔄 CI/CD Pipeline

### GitHub Actions Integration:
```bash
# Set up CI/CD pipeline
tfy pipeline create \
    --name agriwaste-pipeline \
    --project agriwaste2fuel-team3a \
    --repo https://github.com/annam-ai-iitropar/team_3A \
    --branch main \
    --auto-deploy \
    --dockerfile Backend/Dockerfile \
    --context Backend/
```

### Pipeline Configuration:
```yaml
# .github/workflows/truefoundry-deploy.yml
name: Deploy to TrueFoundry

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup TrueFoundry CLI
        run: |
          pip install truefoundry
          echo "${{ secrets.TFY_API_KEY }}" | tfy login --api-key
          
      - name: Deploy Backend
        run: |
          tfy service deploy \
            --name api-service \
            --project agriwaste2fuel-team3a \
            --dockerfile Backend/Dockerfile \
            --context Backend/ \
            --wait
            
      - name: Deploy ML Service
        run: |
          tfy model deploy \
            --name ml-service \
            --project agriwaste2fuel-team3a \
            --dockerfile ML_Models/Dockerfile \
            --context ML_Models/ \
            --wait
```

## 💰 Cost Optimization

### Resource Limits:
```yaml
# Optimized resource configuration
resources:
  api-service:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "1Gi" 
      cpu: "1000m"
    replicas: 2
    autoscaling:
      min: 1
      max: 5
      
  ml-service:
    requests:
      memory: "2Gi"
      cpu: "1000m"
      gpu: 1
    limits:
      memory: "4Gi"
      cpu: "2000m"
      gpu: 1
    replicas: 1
    autoscaling:
      min: 0  # Scale to zero when not in use
      max: 3
```

## 🚀 Deployment Commands Summary

### Quick Deploy (Run in PowerShell):
```powershell
# Navigate to project directory
cd "c:\Users\morey\OneDrive\Desktop\AgriWaste2Fuel"

# Run deployment script
.\truefoundry-deploy.ps1
```

### Manual Step-by-Step:
```bash
# 1. Install and login
pip install truefoundry
tfy login

# 2. Create project
tfy project create agriwaste2fuel-team3a

# 3. Deploy database
tfy database deploy postgres --name agriwaste-postgres --project agriwaste2fuel-team3a

# 4. Deploy backend
tfy service deploy --name api-service --project agriwaste2fuel-team3a --dockerfile Backend/Dockerfile --context Backend/

# 5. Deploy ML service
tfy model deploy --name ml-service --project agriwaste2fuel-team3a --dockerfile ML_Models/Dockerfile --context ML_Models/

# 6. Set up domains
tfy ingress create --name api-ingress --host api.agriwaste2fuel-team3a.annam.ai --service api-service

# 7. Enable monitoring
tfy monitoring enable --project agriwaste2fuel-team3a
```

## ✅ Post-Deployment Checklist

- [ ] **Database connectivity** - Test API can connect to PostgreSQL
- [ ] **ML model loading** - Verify ML service loads models correctly  
- [ ] **API endpoints** - Test all FastAPI endpoints
- [ ] **File uploads** - Test image upload functionality
- [ ] **Authentication** - Verify Firebase auth integration
- [ ] **SSL certificates** - Ensure HTTPS is working
- [ ] **Monitoring** - Check Grafana dashboards
- [ ] **Logs** - Verify structured logging is working
- [ ] **Autoscaling** - Test under load
- [ ] **Backup** - Verify database backup schedule

## 🎯 Frontend Deployment (Recommended: Vercel)

Since TrueFoundry is best for backend/ML services, deploy frontend on Vercel:

```bash
# Frontend on Vercel
vercel --prod

# Update environment variables
REACT_APP_API_URL=https://api.agriwaste2fuel-team3a.annam.ai
REACT_APP_ML_URL=https://ml.agriwaste2fuel-team3a.annam.ai
```

## 📞 Support & Troubleshooting

### TrueFoundry Support:
- Documentation: https://docs.truefoundry.com
- Slack: Annam.ai workspace channel
- Email: support@truefoundry.com

### Common Issues:
1. **Build failures** - Check Dockerfile syntax
2. **Memory limits** - Increase resource limits
3. **Database connection** - Verify connection string
4. **SSL issues** - Check domain DNS settings

---

**Team 3A is ready for enterprise-grade deployment on TrueFoundry! 🚀**
