# TrueFoundry Deployment Script for Team 3A - Windows PowerShell
# AgriWaste2Fuel - Annam.ai Internship Program 2025

Write-Host "🚀 TrueFoundry Deployment for AgriWaste2Fuel - Team 3A" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Step 1: Install TrueFoundry CLI
Write-Host "📦 Installing TrueFoundry CLI..." -ForegroundColor Yellow
pip install truefoundry

# Step 2: Login to TrueFoundry
Write-Host "🔐 Login to TrueFoundry workspace..." -ForegroundColor Yellow
Write-Host "Please login with your Annam.ai credentials:" -ForegroundColor Cyan
tfy login

# Step 3: Set workspace
Write-Host "🏢 Setting Annam.ai workspace..." -ForegroundColor Yellow
tfy workspace set annam-ai-workspace

# Step 4: Create project
Write-Host "📁 Creating Team 3A project..." -ForegroundColor Yellow
tfy project create agriwaste2fuel-team3a --description "AI-powered agricultural waste to fuel conversion - Team 3A"

# Step 5: Deploy Database
Write-Host "🗄️ Deploying PostgreSQL database..." -ForegroundColor Yellow
tfy database deploy postgres `
    --name agriwaste-postgres `
    --version 14 `
    --storage 10Gi `
    --project agriwaste2fuel-team3a

# Step 6: Deploy Backend API
Write-Host "🔧 Deploying Backend API service..." -ForegroundColor Yellow
tfy service deploy `
    --name api-service `
    --project agriwaste2fuel-team3a `
    --dockerfile Backend/Dockerfile `
    --context Backend/ `
    --port 8000 `
    --replicas 2 `
    --cpu-request 500m `
    --memory-request 512Mi `
    --cpu-limit 1000m `
    --memory-limit 1Gi `
    --env ENVIRONMENT=production

# Step 7: Deploy ML Service
Write-Host "🤖 Deploying ML model service..." -ForegroundColor Yellow
tfy model deploy `
    --name ml-service `
    --project agriwaste2fuel-team3a `
    --dockerfile ML_Models/Dockerfile `
    --context ML_Models/ `
    --port 5000 `
    --replicas 1 `
    --cpu-request 1000m `
    --memory-request 2Gi `
    --gpu-request 1

# Step 8: Set up secrets
Write-Host "🔒 Setting up secrets..." -ForegroundColor Yellow
$dbUrl = Read-Host "Enter your PostgreSQL connection string"
tfy secret create database-secrets `
    --project agriwaste2fuel-team3a `
    --from-literal DATABASE_URL="$dbUrl"

tfy secret create firebase-secrets `
    --project agriwaste2fuel-team3a `
    --from-file FIREBASE_CONFIG=Backend/agriwaste2fuel-737b5-firebase-adminsdk-fbsvc-a475a837f4.json

# Step 9: Set up ingress and domains
Write-Host "🌍 Setting up ingress and domains..." -ForegroundColor Yellow
tfy ingress create `
    --name agriwaste-ingress `
    --project agriwaste2fuel-team3a `
    --host api.agriwaste2fuel-team3a.annam.ai `
    --service api-service `
    --port 8000

# Step 10: Enable monitoring
Write-Host "📊 Enabling monitoring and logging..." -ForegroundColor Yellow
tfy monitoring enable `
    --project agriwaste2fuel-team3a `
    --prometheus `
    --grafana `
    --alerts

Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host "🔗 API URL: https://api.agriwaste2fuel-team3a.annam.ai" -ForegroundColor Cyan
Write-Host "🔗 ML Service: https://ml.agriwaste2fuel-team3a.annam.ai" -ForegroundColor Cyan
Write-Host "📊 Monitoring: https://grafana.agriwaste2fuel-team3a.annam.ai" -ForegroundColor Cyan

# Check deployment status
Write-Host "📋 Checking deployment status..." -ForegroundColor Yellow
tfy service list --project agriwaste2fuel-team3a
tfy service logs api-service --project agriwaste2fuel-team3a --tail 50
