# 🚀 Quick Start Guide - AgriWaste2Fuel

## ⚡ 5-Minute Setup

### Prerequisites Check
- [x] Node.js installed? `node --version`
- [x] Python installed? `python --version`
- [x] Git available? `git --version`

### 🔥 Fast Track Setup

#### Backend (2 minutes)
```bash
# 1. Navigate and setup
cd Backend
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add Firebase config
# Place your firebase-service-account.json in Backend folder

# 4. Start server
python -m uvicorn app.main:app --reload --port 8000
```

#### Frontend (2 minutes)
```bash
# 1. Navigate and install
cd Frontend
npm install

# 2. Configure Firebase
# Edit src/config/firebase.js with your config

# 3. Start development server
npm start
```

### ✅ Verification
- Backend: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Test login/register functionality
- Upload sample image for analysis

### 🆘 Emergency Troubleshooting
```bash
# Kill port conflicts
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Reset everything
rm -rf node_modules
npm cache clean --force
npm install
```

## 📋 Project Checklist

### Setup Phase
- [ ] Backend server running on port 8000
- [ ] Frontend running on port 3000
- [ ] Firebase authentication working
- [ ] ML models loaded successfully

### Testing Phase
- [ ] User registration works
- [ ] Image upload and analysis works
- [ ] Text input analysis works
- [ ] Dashboard displays data
- [ ] Certificate generation works
- [ ] Multi-language switching works

### Deployment Ready
- [ ] Production build created (`npm run build`)
- [ ] Environment variables configured
- [ ] Error handling tested
- [ ] Performance optimized

---

## 🎯 Core Features Status

| Feature | Status | Test Command |
|---------|--------|--------------|
| User Auth | ✅ Ready | Register → Login |
| Image Analysis | ✅ Ready | Upload image → Get results |
| Text Analysis | ✅ Ready | Enter waste type → Analyze |
| Recommendations | ✅ Ready | Complete analysis → View suggestions |
| Carbon Calculations | ✅ Ready | Check CO₂ savings in results |
| Certificate Generation | ✅ Ready | Download PDF from results |
| Dashboard | ✅ Ready | View user statistics |
| Multi-language | ✅ Ready | Switch languages in navbar |

## 🔧 Development Commands

### Backend
```bash
# Start development server
uvicorn app.main:app --reload

# Install new package
pip install package-name
pip freeze > requirements.txt

# Run tests
python -m pytest

# Check API documentation
# Visit: http://localhost:8000/docs
```

### Frontend
```bash
# Start development
npm start

# Build for production
npm run build

# Install new package
npm install package-name

# Run tests
npm test

# Check bundle size
npm run build
npx serve -s build
```

---

**Ready to transform agricultural waste into sustainable fuel! 🌾→⚡**
