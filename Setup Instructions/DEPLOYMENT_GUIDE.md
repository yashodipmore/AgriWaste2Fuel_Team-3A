# 🚀 Deployment Guide - AgriWaste2Fuel

## 🌐 Production Deployment Options

### 🎯 Recommended Stack
- **Frontend:** Vercel or Netlify
- **Backend:** Railway, Heroku, or DigitalOcean
- **Database:** PostgreSQL or MongoDB Atlas
- **File Storage:** Firebase Storage or AWS S3
- **CDN:** Cloudflare

## 🔧 Backend Deployment

### Option 1: Railway (Recommended)

#### Step 1: Prepare for Deployment
```bash
# Create production requirements
pip freeze > requirements.txt

# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Create runtime.txt (optional)
echo "python-3.9.16" > runtime.txt
```

#### Step 2: Deploy to Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

#### Step 3: Configure Environment Variables
In Railway dashboard, add:
```env
ENVIRONMENT=production
FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json
DATABASE_URL=postgresql://user:pass@host:port/db
```

### Option 2: Heroku

#### Step 1: Setup Heroku
```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create agriwaste2fuel-api
```

#### Step 2: Configure Files
```bash
# Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# requirements.txt (ensure it's updated)
pip freeze > requirements.txt
```

#### Step 3: Deploy
```bash
# Add files to git
git add .
git commit -m "Deploy to Heroku"

# Deploy
git push heroku main

# Set environment variables
heroku config:set ENVIRONMENT=production
heroku config:set FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json
```

### Option 3: DigitalOcean App Platform

#### Step 1: Create App Spec
Create `.do/app.yaml`:
```yaml
name: agriwaste2fuel-api
services:
- environment_slug: python
  github:
    branch: main
    deploy_on_push: true
    repo: your-username/agriwaste2fuel
  http_port: 8000
  instance_count: 1
  instance_size_slug: basic-xxs
  name: api
  run_command: uvicorn app.main:app --host 0.0.0.0 --port 8000
  source_dir: Backend
  envs:
  - key: ENVIRONMENT
    value: production
```

#### Step 2: Deploy
```bash
# Install doctl
# Follow: https://docs.digitalocean.com/reference/doctl/how-to/install/

# Deploy
doctl apps create --spec .do/app.yaml
```

## 🎨 Frontend Deployment

### Option 1: Vercel (Recommended)

#### Step 1: Prepare Build
```bash
cd Frontend

# Install dependencies
npm install

# Create production build
npm run build

# Test build locally
npx serve -s build
```

#### Step 2: Deploy to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

#### Step 3: Configure Environment Variables
In Vercel dashboard, add:
```env
REACT_APP_API_URL=https://your-backend-url.railway.app
REACT_APP_FIREBASE_API_KEY=your-firebase-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=123456789
REACT_APP_FIREBASE_APP_ID=your-app-id
```

### Option 2: Netlify

#### Step 1: Build and Deploy
```bash
# Build
npm run build

# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod --dir=build
```

#### Step 2: Configure Settings
Create `netlify.toml`:
```toml
[build]
  command = "npm run build"
  publish = "build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  REACT_APP_API_URL = "https://your-backend-url.railway.app"
```

### Option 3: GitHub Pages

#### Step 1: Setup GitHub Pages
```bash
# Install gh-pages
npm install --save-dev gh-pages

# Add to package.json scripts
"predeploy": "npm run build",
"deploy": "gh-pages -d build"

# Add homepage to package.json
"homepage": "https://username.github.io/agriwaste2fuel"
```

#### Step 2: Deploy
```bash
npm run deploy
```

## 🗄 Database Setup

### PostgreSQL (Production)

#### Step 1: Database Provider
Choose one:
- **Railway PostgreSQL** (integrated)
- **Supabase** (PostgreSQL with extras)
- **ElephantSQL** (PostgreSQL as a service)
- **DigitalOcean Managed Database**

#### Step 2: Update Backend for Database
Create `Backend/app/core/database.py`:
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### Step 3: Create Database Models
Create `Backend/app/models/database_models.py`:
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from .database import Base

class UserAnalysis(Base):
    __tablename__ = "user_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    waste_type = Column(String)
    quantity = Column(Float)
    co2_saved = Column(Float)
    carbon_credits = Column(Float)
    processing_method = Column(String)
    created_at = Column(DateTime)
```

#### Step 4: Replace In-Memory Storage
Update `Backend/app/services/analysis_storage.py`:
```python
from sqlalchemy.orm import Session
from ..models.database_models import UserAnalysis
from ..core.database import get_db

class DatabaseStorage:
    def save_analysis_result(self, user_id: str, analysis_data: dict, db: Session):
        analysis = UserAnalysis(
            user_id=user_id,
            waste_type=analysis_data['waste_type'],
            quantity=analysis_data['quantity'],
            co2_saved=analysis_data['co2_saved'],
            carbon_credits=analysis_data['carbon_credits'],
            processing_method=analysis_data['processing_method']
        )
        db.add(analysis)
        db.commit()
        return analysis
```

## 🔒 Security Configuration

### Environment Variables
```bash
# Backend .env (production)
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:port/db
FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json
SECRET_KEY=your-super-secret-key-here
ALLOWED_ORIGINS=https://your-frontend-domain.com
CORS_ORIGINS=["https://your-frontend-domain.com"]
```

### CORS Configuration
Update `Backend/app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Production CORS
if os.getenv("ENVIRONMENT") == "production":
    origins = [
        "https://your-frontend-domain.com",
        "https://your-frontend-domain.vercel.app"
    ]
else:
    origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Firebase Security
```javascript
// Frontend: src/config/firebase.js (production)
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID
};
```

## 📊 Monitoring & Analytics

### Backend Monitoring
```python
# Add to main.py
import time
import logging
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logging.info(
        f"{request.method} {request.url} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    return response
```

### Performance Monitoring
Consider adding:
- **Sentry** for error tracking
- **LogRocket** for frontend monitoring
- **DataDog** for infrastructure monitoring
- **Google Analytics** for user analytics

## 🚀 CI/CD Pipeline

### GitHub Actions
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        cd Backend
        pip install -r requirements.txt
    - name: Run tests
      run: |
        cd Backend
        python -m pytest

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Railway
      run: |
        npm install -g @railway/cli
        railway deploy --service backend
      env:
        RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'
    - name: Install and Build
      run: |
        cd Frontend
        npm install
        npm run build
    - name: Deploy to Vercel
      run: npx vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

## 🔧 Performance Optimization

### Backend Optimization
```python
# Add caching
from functools import lru_cache
import redis

# Redis cache (optional)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@lru_cache(maxsize=100)
def cached_ml_prediction(waste_type: str, quantity: float):
    return ml_model.predict(waste_type, quantity)

# Database connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True
)
```

### Frontend Optimization
```javascript
// Code splitting
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Analysis = lazy(() => import('./pages/Analysis'));

// Image optimization
const optimizeImage = (file) => {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  // Resize and compress logic
};
```

## 📱 Mobile Optimization

### PWA Configuration
Update `Frontend/public/manifest.json`:
```json
{
  "short_name": "AgriWaste2Fuel",
  "name": "AgriWaste to Fuel Converter",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}
```

## 🔍 Testing in Production

### Health Check Endpoints
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "database": "connected" if database_healthy() else "disconnected"
    }
```

### Smoke Tests
```bash
# Test production endpoints
curl https://your-api-domain.com/health
curl -X POST https://your-api-domain.com/api/predict/text \
  -H "Content-Type: application/json" \
  -d '{"waste_type": "Rice Straw", "quantity": "10", "unit": "tons"}'
```

## 📚 Documentation Deployment

Deploy documentation using:
- **GitBook** for comprehensive docs
- **Docusaurus** for developer docs
- **Notion** for internal documentation

## 🚨 Backup & Recovery

### Database Backups
```bash
# Automated daily backups
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Upload to cloud storage
aws s3 cp backup_$(date +%Y%m%d).sql s3://your-backup-bucket/
```

### Code Backups
- Use Git for version control
- Mirror repositories on multiple platforms
- Tag releases for rollback capability

---

**🎉 Your AgriWaste2Fuel application is now production-ready!**

### Quick Deployment Checklist
- [ ] Backend deployed and running
- [ ] Frontend deployed and accessible
- [ ] Database connected and configured
- [ ] Environment variables set
- [ ] CORS configured properly
- [ ] HTTPS enabled
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Backup system in place

**🌱 Ready to transform agricultural waste into sustainable fuel at scale!**
