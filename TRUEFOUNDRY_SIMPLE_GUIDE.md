# TrueFoundry Simple Setup Guide - Team 3A
# बिल्कुल आसान तरीके से! 🚀

## 🎯 TrueFoundry क्या है?
**Simple words में:**
- ये एक website है जहाँ आप अपना backend deploy कर सकते हैं
- Railway की तरह, but बहुत ज्यादा powerful
- Annam.ai company इसे use करती है
- Free में भी काम करता है basic features के लिए

## 📱 Step 1: Account Setup (बिल्कुल आसान!)

### 1.1 TrueFoundry Website पर जाएं:
```
🌐 Website: https://www.truefoundry.com
```

### 1.2 Sign Up करें:
1. **"Get Started"** button पर click करें
2. **Email** और **Password** डालें
3. **"Create Account"** पर click करें
4. **Email verification** करें (inbox check करें)

### 1.3 Annam.ai Workspace Join करें:
```
📧 Annam.ai team से invite link मांगें
या
🔗 Workspace URL: annam-ai.truefoundry.com
```

## 💻 Step 2: Local Setup (अपने Computer पर)

### 2.1 Python Check करें:
```powershell
# PowerShell में type करें
python --version

# अगर error आए तो Python install करें from python.org
```

### 2.2 TrueFoundry CLI Install करें:
```powershell
# यह command run करें
pip install truefoundry

# Success message आना चाहिए
```

### 2.3 Login करें:
```powershell
# यह command run करें
tfy login

# Browser में website खुलेगी
# अपने account से login करें
# "Success" message आएगा terminal में
```

## 🏗️ Step 3: Project बनाएं (GUI में!)

### 3.1 TrueFoundry Dashboard:
1. **Browser** में `https://app.truefoundry.com` जाएं
2. **Login** करें अपने account से
3. **"Create New Project"** पर click करें

### 3.2 Project Details:
```
📝 Project Name: agriwaste2fuel-team3a
📝 Description: Team 3A - AgriWaste2Fuel Backend
📝 Team: Annam.ai Internship
```

### 3.3 Project Create करें:
- **"Create Project"** button पर click करें
- Project dashboard दिखेगी

## 🗄️ Step 4: Database Setup (One Click!)

### 4.1 Database Add करें:
1. Project dashboard में **"Add Service"** पर click करें
2. **"Database"** option select करें
3. **"PostgreSQL"** choose करें

### 4.2 Database Configuration:
```
📝 Database Name: agriwaste-postgres
📝 Version: 14 (latest)
📝 Storage: 5GB (free tier)
📝 Password: apna strong password
```

### 4.3 Deploy Database:
- **"Deploy Database"** पर click करें
- 2-3 minutes wait करें
- Green checkmark आएगा ✅

## 🚀 Step 5: Backend Deploy (Drag & Drop!)

### 5.1 Backend Service Add करें:
1. **"Add Service"** पर click करें again
2. **"Web Service"** select करें
3. **"From GitHub"** option choose करें

### 5.2 GitHub Connect करें:
```
📝 Repository: https://github.com/annam-ai-iitropar/team_3A
📝 Branch: main
📝 Folder Path: /Backend
📝 Dockerfile: Backend/Dockerfile
```

### 5.3 Service Configuration:
```
📝 Service Name: api-service
📝 Port: 8000
📝 Memory: 512MB
📝 CPU: 0.5 cores
📝 Replicas: 1
```

### 5.4 Environment Variables Add करें:
```
🔧 DATABASE_URL: (database connection से copy करें)
🔧 ENVIRONMENT: production
🔧 PORT: 8000
```

### 5.5 Deploy करें:
- **"Deploy Service"** पर click करें
- Build logs दिखेंगे
- 5-10 minutes wait करें
- Success message आएगा! 🎉

## 🌐 Step 6: Domain Setup (Automatic!)

### 6.1 Custom Domain:
- Service deploy होने के बाद automatic URL मिलेगा:
```
🔗 Your Backend URL: 
https://api-service-agriwaste2fuel-team3a.truefoundry.app
```

### 6.2 Test करें:
```
🧪 Browser में जाकर test करें:
https://your-url/docs

FastAPI documentation page दिखना चाहिए!
```

## 📊 Step 7: Monitoring Setup (Built-in!)

### 7.1 Dashboard Check करें:
1. Project dashboard में **"Monitoring"** tab पर click करें
2. CPU, Memory usage graphs दिखेंगे
3. Logs भी देख सकते हैं

### 7.2 Alerts Setup:
```
⚠️ CPU > 80% पर alert
⚠️ Memory > 85% पर alert
⚠️ Service down पर email notification
```

## 🔧 Step 8: Frontend Connect करें

### 8.1 Frontend Environment Variables Update करें:
```javascript
// Frontend/.env.production
REACT_APP_API_URL=https://your-truefoundry-backend-url
```

### 8.2 Frontend Deploy (Vercel recommended):
```bash
# Vercel पर deploy करें (easier than TrueFoundry for frontend)
npm run build
vercel --prod
```

## ✅ Step 9: Testing Checklist

### 9.1 Backend Test:
- [ ] API docs accessible (`/docs` endpoint)
- [ ] Database connection working
- [ ] Image upload working
- [ ] Authentication working

### 9.2 Frontend Test:
- [ ] API calls working
- [ ] Image upload from frontend
- [ ] User registration/login
- [ ] Certificate generation

## 🆘 Troubleshooting (Common Problems)

### Problem 1: CLI Login नहीं हो रहा
```powershell
# Solution:
tfy logout
tfy login --api-key YOUR_API_KEY

# API key: Account settings > API Keys से copy करें
```

### Problem 2: Build fail हो रहा है
```
❌ Dockerfile में error है
✅ Backend/Dockerfile check करें
✅ requirements.txt में सभी dependencies हैं
```

### Problem 3: Database connect नहीं हो रहा
```
❌ Connection string wrong है
✅ Database dashboard से correct URL copy करें
✅ Environment variables में properly set करें
```

### Problem 4: Service slow है
```
❌ Resources कम हैं
✅ Memory 512MB → 1GB बढ़ाएं
✅ CPU 0.5 → 1 core बढ़ाएं
```

## 🎯 Quick Commands Summary

### सबसे Important Commands:
```powershell
# Install
pip install truefoundry

# Login
tfy login

# Project list
tfy project list

# Service status
tfy service list

# Logs देखें
tfy logs api-service --follow

# Service restart
tfy service restart api-service
```

## 📞 Help & Support

### अगर कुछ समझ नहीं आए:
1. **TrueFoundry Docs**: https://docs.truefoundry.com
2. **Team 3A Group**: WhatsApp/Discord में पूछें
3. **Annam.ai Mentors**: Direct contact करें
4. **Community**: TrueFoundry Slack channel

### Emergency Contacts:
```
📱 TrueFoundry Support: support@truefoundry.com
📱 Annam.ai Team: (आपके mentor का contact)
```

---

## 🎉 Success होने पर आपके पास होगा:

✅ **Working Backend API** on TrueFoundry
✅ **PostgreSQL Database** connected  
✅ **Monitoring Dashboard** for health check
✅ **Custom Domain** for API access
✅ **Auto-scaling** if traffic बढ़े
✅ **Professional Deployment** for portfolio

**बस इतना करना है! Railway से भी आसान है! 😊🚀**

---

**Team 3A, तुम्हारा backend enterprise-ready हो जाएगा! 💪**
