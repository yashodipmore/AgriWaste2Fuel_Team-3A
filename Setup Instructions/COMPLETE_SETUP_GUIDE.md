# 🌾 AgriWaste2Fuel - Complete Setup Guide

## 📋 Project Overview

AgriWaste2Fuel is a full-stack web application that helps farmers convert agricultural waste into sustainable fuel alternatives using AI-powered analysis. The project includes image-based waste classification, text-based analysis, carbon credit calculations, and sustainability certificates.

## 🛠 Technology Stack

### Frontend
- **React 18** - Modern React with hooks
- **React Router** - Navigation and routing
- **Tailwind CSS** - Utility-first CSS framework
- **React i18next** - Internationalization (English, Hindi, Marathi)
- **Firebase Auth** - User authentication
- **Axios** - HTTP client for API calls

### Backend
- **FastAPI** - Modern Python web framework
- **Firebase Admin SDK** - Authentication verification
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server
- **YOLOv8** - Image classification model
- **ReportLab** - PDF certificate generation

## 📁 Project Structure

```
AgriWaste2Fuel/
├── Frontend/                 # React Application
│   ├── public/              # Static assets
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts (Auth)
│   │   ├── services/       # API services
│   │   ├── utils/          # Utility functions
│   │   ├── i18n/           # Internationalization
│   │   └── config/         # Configuration files
│   ├── package.json
│   └── tailwind.config.js
│
├── Backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/   # API route handlers
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic
│   │   │   ├── ml/         # Machine Learning services
│   │   │   └── auth_service.py
│   │   ├── core/           # Core configuration
│   │   └── main.py         # FastAPI app entry point
│   ├── requirements.txt
│   └── models/             # ML model files
│
└── README.md               # This file
```

## 🚀 Quick Setup (Development)

### Prerequisites
- **Node.js** (v16 or higher)
- **Python** (v3.9 or higher)
- **Git**
- **Firebase Project** (for authentication)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AgriWaste2Fuel
```

### 2. Backend Setup

#### Step 1: Navigate to Backend Directory
```bash
cd Backend
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Firebase Configuration
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use existing one
3. Enable Authentication with Email/Password
4. Generate service account key:
   - Go to Project Settings → Service Accounts
   - Click "Generate new private key"
   - Save as `firebase-service-account.json` in `Backend/` directory

#### Step 5: Environment Variables
Create `.env` file in Backend directory:
```env
FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json
```

#### Step 6: Start Backend Server
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at: `http://localhost:8000`

### 3. Frontend Setup

#### Step 1: Navigate to Frontend Directory
```bash
cd ../Frontend
```

#### Step 2: Install Dependencies
```bash
npm install
```

#### Step 3: Firebase Configuration
1. In Firebase Console, go to Project Settings → General
2. Scroll down to "Your apps" and click "Add app" → Web
3. Register your app and copy the config object
4. Create `src/config/firebase.js`:

```javascript
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "your-app-id"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export default app;
```

#### Step 4: Start Frontend Server
```bash
npm start
```

Frontend will be available at: `http://localhost:3000`

## 🧪 Testing the Application

### 1. User Registration/Login
1. Open `http://localhost:3000`
2. Click "Register" to create a new account
3. Verify email and login

### 2. Image Analysis
1. Navigate to "Upload Image" or "Image Analysis"
2. Upload an agricultural waste image
3. Wait for AI analysis results
4. View recommendations and carbon calculations

### 3. Text Analysis
1. Navigate to "Manual Input" or "Text Analysis"
2. Enter waste type (e.g., "Rice Straw")
3. Specify quantity and location
4. Get instant analysis results

### 4. Dashboard
1. Complete some analyses
2. Visit Dashboard to see:
   - Total analyses performed
   - CO₂ saved
   - Carbon credits earned
   - Recent activity

### 5. Certificate Download
1. Complete an analysis
2. On results page, click "Download Certificate"
3. Get PDF sustainability certificate

## 🔧 Advanced Configuration

### ML Model Setup
1. Place YOLOv8 model file (`best.pt`) in `Backend/app/models/`
2. Model will be automatically loaded on server startup

### Custom Styling
- Modify `Frontend/tailwind.config.js` for custom theme
- Edit component styles in respective files

### API Documentation
- Backend API docs: `http://localhost:8000/docs`
- Interactive testing: `http://localhost:8000/redoc`

## 📱 Features Overview

### ✅ Implemented Features
- **User Authentication** - Firebase-based secure login/register
- **Image Classification** - AI-powered waste type detection
- **Text Analysis** - Manual waste type entry and processing
- **Processing Recommendations** - Optimized methods for each waste type
- **Carbon Calculations** - CO₂ savings and carbon credit calculations
- **Certificate Generation** - Professional PDF certificates
- **Multi-language Support** - English, Hindi, Marathi
- **Responsive Design** - Mobile-friendly interface
- **Dashboard** - User statistics and activity tracking

### 🔄 Analysis Flow
1. **Input** → Image upload or text description
2. **Classification** → AI identifies waste type
3. **Recommendations** → Optimal processing method suggested
4. **Calculations** → Environmental impact computed
5. **Results** → Comprehensive analysis with certificate

## 🚨 Troubleshooting

### Common Issues

#### Backend Issues
**Port 8000 already in use:**
```bash
# Kill existing process
netstat -ano | findstr :8000
taskkill /PID <process-id> /F

# Or use different port
uvicorn app.main:app --reload --port 8001
```

**Firebase authentication errors:**
- Verify `firebase-service-account.json` path
- Check Firebase project configuration
- Ensure Authentication is enabled in Firebase Console

**ML model loading errors:**
- Verify `best.pt` file exists in `Backend/app/models/`
- Check Python dependencies (ultralytics, torch)

#### Frontend Issues
**Port 3000 already in use:**
```bash
# Use different port
PORT=3001 npm start
```

**Firebase configuration errors:**
- Verify `src/config/firebase.js` configuration
- Check API keys and project settings
- Ensure web app is registered in Firebase

**API connection errors:**
- Verify backend server is running on port 8000
- Check CORS settings in backend
- Confirm API endpoints in `src/services/api.js`

### Performance Tips
- **Backend:** Use production ASGI server (gunicorn) for deployment
- **Frontend:** Build production version with `npm run build`
- **Database:** Consider adding persistent storage for production

## 🌐 Deployment

### Frontend Deployment (Netlify/Vercel)
1. Build production version:
```bash
npm run build
```
2. Deploy `build/` folder to hosting service
3. Configure environment variables for production Firebase config

### Backend Deployment (Railway/Heroku)
1. Create `Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
2. Configure environment variables
3. Deploy to platform

## 📝 Environment Variables

### Backend (.env)
```env
FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json
ENVIRONMENT=development
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_FIREBASE_API_KEY=your-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
```

## 👥 Team Integration

### For ML Team
- Add models to `Backend/app/models/`
- Implement classifiers in `Backend/app/services/ml/`
- Update prediction endpoints as needed

### For Database Team
- Replace in-memory storage in `Backend/app/services/analysis_storage.py`
- Add database models and migrations
- Update dashboard endpoints for persistence

### For Frontend Team
- Components are in `Frontend/src/components/`
- Pages are in `Frontend/src/pages/`
- Styling uses Tailwind CSS classes

## 📊 Project Metrics

- **Frontend:** ~15 React components, 6 main pages
- **Backend:** 6 API routers, 20+ endpoints
- **Features:** Image analysis, text analysis, dashboard, certificates
- **Languages:** 3 language support (EN/HI/MR)
- **Authentication:** Firebase-based secure auth

## 🎯 Future Enhancements

1. **Database Integration** - Replace in-memory storage
2. **Advanced ML Models** - More sophisticated waste classification
3. **Real-time Analytics** - Live dashboard updates
4. **Mobile App** - React Native implementation
5. **IoT Integration** - Sensor data processing
6. **Marketplace** - Carbon credit trading platform

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review API documentation at `/docs`
3. Check browser console for frontend errors
4. Review server logs for backend issues

## 📜 License

This project was created for educational purposes and hackathon participation. Feel free to use and modify according to your needs.

---

**Built with ❤️ for sustainable agriculture and environmental impact.**
