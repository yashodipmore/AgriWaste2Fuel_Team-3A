# 🔧 Developer Setup Guide

## 🏗 Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Firebase      │
│   React App     │◄──►│   FastAPI       │◄──►│   Auth Service  │
│   Port 3000     │    │   Port 8000     │    │   Cloud         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Tailwind CSS  │    │   ML Models     │    │   User Data     │
│   i18n Support  │    │   YOLO + Text   │    │   Sessions      │
│   Responsive    │    │   Classification │    │   Tokens        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📂 Detailed File Structure

### Frontend Structure
```
Frontend/
├── public/
│   ├── index.html              # Main HTML template
│   ├── manifest.json           # PWA configuration
│   └── AgriLogo.png           # App logo
├── src/
│   ├── components/             # Reusable UI components
│   │   ├── Navbar.jsx         # Navigation bar with auth
│   │   ├── Footer.jsx         # Site footer
│   │   ├── ImageUpload.jsx    # Image upload component
│   │   ├── TextInput.jsx      # Manual text input
│   │   ├── ResultCard.jsx     # Analysis results display
│   │   ├── CertificateDownload.jsx # PDF download
│   │   └── LanguageSelector.jsx # i18n language switcher
│   ├── pages/                  # Main page components
│   │   ├── Home.jsx           # Landing page
│   │   ├── Login.jsx          # User authentication
│   │   ├── Register.jsx       # User registration
│   │   ├── Input.jsx          # Analysis input page
│   │   ├── Result.jsx         # Results display page
│   │   ├── Dashboard.jsx      # User dashboard
│   │   └── About.jsx          # About page
│   ├── contexts/               # React contexts
│   │   └── AuthContext.js     # Firebase auth context
│   ├── services/               # API communication
│   │   └── api.js             # All backend API calls
│   ├── i18n/                   # Internationalization
│   │   ├── index.js           # i18n configuration
│   │   └── locales/           # Translation files
│   │       ├── en.json        # English translations
│   │       ├── hi.json        # Hindi translations
│   │       └── mr.json        # Marathi translations
│   ├── App.js                  # Main app component
│   ├── index.js               # React entry point
│   └── index.css              # Global styles
├── package.json                # Dependencies and scripts
└── tailwind.config.js         # Tailwind CSS configuration
```

### Backend Structure
```
Backend/
├── app/
│   ├── main.py                 # FastAPI application entry
│   ├── api/
│   │   └── endpoints/          # API route handlers
│   │       ├── auth.py        # Authentication endpoints
│   │       ├── prediction.py  # ML prediction endpoints
│   │       ├── dashboard.py   # Dashboard data endpoints
│   │       └── certificate.py # Certificate generation
│   ├── models/                 # Pydantic data models
│   │   ├── prediction.py      # Prediction request/response
│   │   ├── user.py           # User data models
│   │   └── dashboard.py      # Dashboard models
│   ├── services/               # Business logic
│   │   ├── auth_service.py    # Firebase authentication
│   │   ├── analysis_storage.py # User data storage
│   │   ├── certificate_service.py # PDF generation
│   │   └── ml/                # Machine learning services
│   │       ├── image_classifier.py # YOLO image classification
│   │       ├── text_classifier.py  # Text analysis
│   │       └── recommendations.py  # Processing recommendations
│   └── core/                   # Core configuration
│       ├── config.py          # App configuration
│       └── database.py        # Database setup (future)
├── models/                     # ML model files
│   └── best.pt               # YOLOv8 trained model
├── requirements.txt            # Python dependencies
└── firebase-service-account.json # Firebase admin credentials
```

## 🛠 Development Workflow

### 1. Environment Setup

#### Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Verify activation
which python  # Should show venv path
```

#### Node.js Environment
```bash
# Check Node version (required: v16+)
node --version
npm --version

# Clean install
rm -rf node_modules package-lock.json
npm install
```

### 2. Database Setup (Current: In-Memory)

The current implementation uses in-memory storage via `analysis_storage.py`. For production:

```python
# Current storage (analysis_storage.py)
class AnalysisStorage:
    def __init__(self):
        self.user_data = {}  # In-memory storage
        
# Future: Replace with database
# - PostgreSQL for production
# - SQLite for development
# - MongoDB for document storage
```

### 3. API Development

#### Adding New Endpoints
```python
# 1. Create model in models/
class NewRequest(BaseModel):
    field: str
    
# 2. Add endpoint in api/endpoints/
@router.post("/new-endpoint")
async def new_endpoint(request: NewRequest):
    # Logic here
    return {"result": "success"}
    
# 3. Register router in main.py
app.include_router(new_router, prefix="/api")
```

#### Frontend API Integration
```javascript
// Add to services/api.js
export const newApiCall = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/new-endpoint`, data);
    return response.data;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};
```

### 4. Component Development

#### React Component Template
```jsx
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const NewComponent = ({ prop1, prop2 }) => {
  const { t } = useTranslation();
  const [state, setState] = useState(null);
  
  useEffect(() => {
    // Component lifecycle logic
  }, []);
  
  return (
    <div className="component-container">
      <h2>{t('component.title')}</h2>
      {/* Component JSX */}
    </div>
  );
};

export default NewComponent;
```

#### Adding Translations
```json
// Add to i18n/locales/en.json
{
  "component": {
    "title": "New Component Title",
    "description": "Component description"
  }
}
```

## 🔍 Testing & Debugging

### Backend Testing
```bash
# Manual API testing
curl -X POST "http://localhost:8000/api/predict/image" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample-image.jpg"

# View API documentation
# http://localhost:8000/docs

# Check server logs
tail -f server.log
```

### Frontend Testing
```bash
# Start development server with debugging
REACT_APP_DEBUG=true npm start

# Build and test production
npm run build
npx serve -s build

# Check bundle size
npm run build -- --analyze
```

### Integration Testing
1. Start backend server
2. Start frontend development server
3. Test complete user flow:
   - Register/Login
   - Upload image
   - Enter text
   - View results
   - Download certificate
   - Check dashboard

## 📊 Performance Optimization

### Backend Optimization
```python
# Use async/await for I/O operations
@app.get("/async-endpoint")
async def async_endpoint():
    result = await async_operation()
    return result

# Add caching for ML predictions
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_prediction(image_hash):
    return model.predict(image_hash)
```

### Frontend Optimization
```jsx
// Use React.memo for expensive components
import React, { memo } from 'react';

const ExpensiveComponent = memo(({ data }) => {
  return <div>{/* Expensive rendering */}</div>;
});

// Use lazy loading for routes
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Dashboard />
    </Suspense>
  );
}
```

## 🚀 Deployment Configuration

### Backend Deployment
```dockerfile
# Dockerfile for backend
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Deploy to Netlify
npm install -g netlify-cli
netlify deploy --prod --dir=build

# Deploy to Vercel
npm install -g vercel
vercel --prod
```

### Environment Variables

#### Backend (.env)
```env
# Development
ENVIRONMENT=development
DEBUG=true
FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json

# Production
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:pass@host:port/db
```

#### Frontend (.env)
```env
# Development
REACT_APP_API_URL=http://localhost:8000
REACT_APP_DEBUG=true

# Production
REACT_APP_API_URL=https://your-api-domain.com
REACT_APP_DEBUG=false
```

## 🔧 Maintenance & Monitoring

### Health Checks
```python
# Backend health endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### Error Monitoring
```javascript
// Frontend error boundary
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }
    return this.props.children;
  }
}
```

## 💡 Development Tips

1. **Hot Reloading**: Use `--reload` for backend and React dev server for frontend
2. **API Documentation**: Always check `/docs` for backend API reference
3. **Component Inspector**: Use React DevTools for component debugging
4. **Network Tab**: Monitor API calls in browser developer tools
5. **Git Workflow**: Use feature branches for new development

---

**Happy coding! 👨‍💻 Build amazing sustainable solutions! 🌱**
