# 🔥 Railway Deployment - Step by Step

## 🎯 **Railway Backend Deployment (Detailed)**

### **What is Railway?**
- Free cloud platform for deploying apps
- 500 hours/month free (16+ hours daily)
- Automatic database included
- No credit card required

---

### **Step 1: Prepare Backend Files**

#### 1.1 Open Terminal in Backend Folder
```bash
# Navigate to your project
cd c:\Users\morey\OneDrive\Desktop\AgriWaste2Fuel\Backend
```

#### 1.2 Create Procfile
```bash
# Create Procfile (tells Railway how to run your app)
echo "web: uvicorn app.main:app --host 0.0.0.0 --port $PORT" > Procfile
```

#### 1.3 Update Requirements
```bash
# Make sure all dependencies are listed
pip freeze > requirements.txt
```

#### 1.4 Check Firebase File
```bash
# Make sure this file exists in Backend folder
ls firebase-service-account.json
```

---

### **Step 2: Railway Account Setup**

#### 2.1 Go to Railway Website
1. Open browser: **https://railway.app**
2. Click **"Login"** (top right)
3. Click **"Continue with GitHub"**
4. Login with your GitHub account
5. Allow Railway access to your repositories

#### 2.2 Create New Project
1. Click **"New Project"** (big purple button)
2. Click **"Deploy from GitHub repo"**
3. Find **"AgriWaste2Fuel"** repository
4. Click **"Deploy Now"**

#### 2.3 Configure Root Directory
1. Railway will start deploying
2. Click **"Settings"** tab
3. Scroll to **"Service Settings"**
4. Set **"Root Directory"** to: `Backend`
5. Click **"Update"**

---

### **Step 3: Add Database**

#### 3.1 Add PostgreSQL
1. In your Railway project dashboard
2. Click **"+ New"** (top right)
3. Click **"Database"**
4. Click **"Add PostgreSQL"**
5. Database automatically created!

#### 3.2 Check Database Connection
1. Click on **PostgreSQL** service
2. Go to **"Connect"** tab
3. Copy **"Postgres Connection URL"**
4. This is automatically added as **DATABASE_URL** variable

---

### **Step 4: Environment Variables**

#### 4.1 Add Environment Variables
1. Click on your **Backend service** (not database)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**

#### 4.2 Add These Variables:
```env
# Variable 1
Name: ENVIRONMENT
Value: production

# Variable 2  
Name: FIREBASE_SERVICE_ACCOUNT_PATH
Value: firebase-service-account.json
```

#### 4.3 Save Variables
1. Click **"Add"** for each variable
2. Railway will automatically redeploy

---

### **Step 5: Check Deployment**

#### 5.1 Monitor Deployment
1. Go to **"Deployments"** tab
2. Click on latest deployment
3. Watch **"Deploy Logs"**
4. Wait for **"Success"** message

#### 5.2 Get Your Backend URL
1. After successful deployment
2. Go to **"Settings"** tab
3. Scroll to **"Domains"**
4. Copy the **Railway domain** (like: `backend-production-1234.up.railway.app`)

#### 5.3 Test Backend
```bash
# Test your deployed backend
curl https://your-backend-url.up.railway.app/health

# Should return: {"status": "healthy", ...}
```

---

### **Step 6: Common Railway Issues & Solutions**

#### Issue 1: Build Failed
**Cause:** Missing requirements.txt or wrong Python version
**Solution:**
```bash
# In Backend folder
pip freeze > requirements.txt
echo "python-3.9.16" > runtime.txt
git add . && git commit -m "Fix requirements" && git push
```

#### Issue 2: App Crashed
**Cause:** Wrong Procfile or missing environment variables
**Solution:**
1. Check Procfile content: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
2. Verify all environment variables are added

#### Issue 3: Database Connection Error
**Cause:** DATABASE_URL not automatically set
**Solution:**
1. Go to PostgreSQL service → Variables tab
2. Copy DATABASE_URL value
3. Add it manually to Backend service variables

#### Issue 4: Import Errors
**Cause:** Missing dependencies
**Solution:**
```bash
# Add missing packages to requirements.txt
pip install package-name
pip freeze > requirements.txt
```

---

### **Step 7: Verify Everything Works**

#### 7.1 Test API Endpoints
```bash
# Health check
curl https://your-backend-url.up.railway.app/health

# API documentation
# Visit: https://your-backend-url.up.railway.app/docs
```

#### 7.2 Check Logs
1. Railway dashboard → Backend service
2. Go to **"Observability"** tab
3. Check **"Logs"** for any errors

---

## 🎯 **Railway Dashboard Navigation**

### **Main Dashboard**
- **Services:** Your backend + database
- **+ New:** Add more services
- **Settings:** Project-level settings

### **Backend Service Dashboard**
- **Deployments:** See deployment history and logs
- **Variables:** Environment variables
- **Settings:** Service configuration
- **Observability:** Logs and metrics
- **Connect:** Domain and connection info

### **PostgreSQL Service Dashboard**
- **Connect:** Database connection details
- **Data:** Browse database (coming soon)
- **Backups:** Automatic backups

---

## 🚨 **Troubleshooting Commands**

### **Local Testing Before Deploy**
```bash
# Test locally first
cd Backend
python -m uvicorn app.main:app --reload

# Visit: http://localhost:8000/docs
```

### **Check Railway Deployment**
```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Login
railway login

# Check deployment status
railway status

# View logs
railway logs
```

### **Force Redeploy**
1. Railway dashboard → Backend service
2. Go to **"Deployments"** tab
3. Click **"Deploy Latest Commit"**

---

## ✅ **Success Indicators**

### **Deployment Successful When:**
- ✅ Build logs show "Success"
- ✅ Health endpoint returns 200 OK
- ✅ API docs page loads
- ✅ No error logs in Observability

### **Your Backend is Ready When:**
- ✅ Railway URL works: `https://your-app.up.railway.app/health`
- ✅ API docs accessible: `https://your-app.up.railway.app/docs`
- ✅ Database connected (no connection errors in logs)

---

**🎉 Railway deployment complete! Ab tumhara backend live hai!** 

**Next:** Vercel pe frontend deploy karna hai! 🚀
