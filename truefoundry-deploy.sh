# TrueFoundry Deployment Script for Team 3A
# AgriWaste2Fuel - Annam.ai Internship Program 2025

# Prerequisites:
# 1. TrueFoundry CLI installed
# 2. Access to Annam.ai TrueFoundry workspace
# 3. Docker installed locally

# Installation Commands:
echo "🚀 TrueFoundry Deployment for AgriWaste2Fuel - Team 3A"
echo "=================================================="

# Step 1: Install TrueFoundry CLI
echo "📦 Installing TrueFoundry CLI..."
pip install truefoundry

# Step 2: Login to TrueFoundry
echo "🔐 Login to TrueFoundry workspace..."
tfy login

# Step 3: Set workspace
echo "🏢 Setting Annam.ai workspace..."
tfy workspace set annam-ai-workspace

# Step 4: Create project
echo "📁 Creating Team 3A project..."
tfy project create agriwaste2fuel-team3a --description "AI-powered agricultural waste to fuel conversion - Team 3A"

# Step 5: Deploy Database
echo "🗄️ Deploying PostgreSQL database..."
tfy database deploy postgres \
    --name agriwaste-postgres \
    --version 14 \
    --storage 10Gi \
    --project agriwaste2fuel-team3a

# Step 6: Deploy Backend API
echo "🔧 Deploying Backend API service..."
tfy service deploy \
    --name api-service \
    --project agriwaste2fuel-team3a \
    --dockerfile Backend/Dockerfile \
    --context Backend/ \
    --port 8000 \
    --replicas 2 \
    --cpu-request 500m \
    --memory-request 512Mi \
    --cpu-limit 1000m \
    --memory-limit 1Gi \
    --env ENVIRONMENT=production \
    --env DATABASE_URL=postgresql://user:pass@agriwaste-postgres:5432/agriwaste2fuel

# Step 7: Deploy ML Service
echo "🤖 Deploying ML model service..."
tfy model deploy \
    --name ml-service \
    --project agriwaste2fuel-team3a \
    --dockerfile ML_Models/Dockerfile \
    --context ML_Models/ \
    --port 5000 \
    --replicas 1 \
    --cpu-request 1000m \
    --memory-request 2Gi \
    --gpu-request 1 \
    --env MODEL_PATH=/models/waste-classifier

# Step 8: Deploy Frontend (Optional - can use Vercel instead)
echo "🌐 Deploying Frontend service..."
tfy service deploy \
    --name frontend-service \
    --project agriwaste2fuel-team3a \
    --dockerfile Frontend/Dockerfile.prod \
    --context Frontend/ \
    --port 3000 \
    --replicas 2 \
    --cpu-request 250m \
    --memory-request 256Mi \
    --env REACT_APP_API_URL=https://api-service-agriwaste2fuel-team3a.truefoundry.app \
    --env NODE_ENV=production

# Step 9: Set up secrets
echo "🔒 Setting up secrets..."
tfy secret create database-secrets \
    --project agriwaste2fuel-team3a \
    --from-literal DATABASE_URL="postgresql://user:pass@host:5432/db"

tfy secret create firebase-secrets \
    --project agriwaste2fuel-team3a \
    --from-file FIREBASE_CONFIG=Backend/agriwaste2fuel-737b5-firebase-adminsdk-fbsvc-a475a837f4.json

# Step 10: Set up ingress and domains
echo "🌍 Setting up ingress and domains..."
tfy ingress create \
    --name agriwaste-ingress \
    --project agriwaste2fuel-team3a \
    --host api.agriwaste2fuel-team3a.annam.ai \
    --service api-service \
    --port 8000

tfy ingress create \
    --name ml-ingress \
    --project agriwaste2fuel-team3a \
    --host ml.agriwaste2fuel-team3a.annam.ai \
    --service ml-service \
    --port 5000

# Step 11: Enable monitoring
echo "📊 Enabling monitoring and logging..."
tfy monitoring enable \
    --project agriwaste2fuel-team3a \
    --prometheus \
    --grafana \
    --alerts

# Step 12: Set up CI/CD
echo "🔄 Setting up CI/CD pipeline..."
tfy pipeline create \
    --name agriwaste-pipeline \
    --project agriwaste2fuel-team3a \
    --repo https://github.com/annam-ai-iitropar/team_3A \
    --branch main \
    --auto-deploy

echo "✅ Deployment completed successfully!"
echo "🔗 API URL: https://api.agriwaste2fuel-team3a.annam.ai"
echo "🔗 ML Service: https://ml.agriwaste2fuel-team3a.annam.ai"
echo "🔗 Frontend: https://app.agriwaste2fuel-team3a.annam.ai"
echo "📊 Monitoring: https://grafana.agriwaste2fuel-team3a.annam.ai"

# Check deployment status
echo "📋 Checking deployment status..."
tfy service list --project agriwaste2fuel-team3a
tfy service logs api-service --project agriwaste2fuel-team3a --tail 50
