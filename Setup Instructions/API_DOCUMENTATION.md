# 🎯 API Documentation - AgriWaste2Fuel

## 📡 Base URL
- **Development:** `http://localhost:8000`
- **Production:** `https://your-domain.com`

## 🔐 Authentication

All protected endpoints require a valid Firebase ID token in the Authorization header:
```
Authorization: Bearer <firebase-id-token>
```

## 📋 Endpoints Overview

### 🔑 Authentication Endpoints

#### POST `/api/auth/verify-token`
Verify Firebase ID token
```json
// Request
{
  "token": "firebase-id-token-string"
}

// Response (200 OK)
{
  "valid": true,
  "user_id": "firebase-user-id",
  "email": "user@example.com"
}

// Response (401 Unauthorized)
{
  "detail": "Invalid token"
}
```

### 🖼 Image Prediction Endpoints

#### POST `/api/predict/image`
Upload and analyze agricultural waste image
```bash
# curl example
curl -X POST "http://localhost:8000/api/predict/image" \
  -H "Authorization: Bearer <token>" \
  -F "file=@image.jpg"
```

```json
// Response (200 OK)
{
  "waste_type": "Rice Straw",
  "confidence": 0.95,
  "processing_method": "Pelletization",
  "estimated_fuel_output": "2.5 tons",
  "carbon_credits": 15.5,
  "co2_saved": 25.8,
  "recommendations": [
    "Optimal moisture content: 10-15%",
    "Pelletization temperature: 80-90°C"
  ]
}

// Response (422 Validation Error)
{
  "detail": [
    {
      "loc": ["body", "file"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 📝 Text Prediction Endpoints

#### POST `/api/predict/text`
Analyze waste type from text description
```json
// Request
{
  "waste_type": "Rice Straw",
  "quantity": "10",
  "unit": "tons",
  "location": "Maharashtra, India"
}

// Response (200 OK)
{
  "waste_type": "Rice Straw",
  "confidence": 0.88,
  "processing_method": "Pelletization",
  "estimated_fuel_output": "8.5 tons",
  "carbon_credits": 52.0,
  "co2_saved": 86.4,
  "recommendations": [
    "Pre-treatment: Chopping to 2-5cm pieces",
    "Drying to 10-15% moisture content",
    "Pelletization at 80-90°C"
  ]
}
```

### 💡 Recommendations Endpoint

#### POST `/api/recommendations`
Get processing recommendations for specific waste type
```json
// Request
{
  "waste_type": "Wheat Straw",
  "quantity": "5.0",
  "location": "Punjab, India"
}

// Response (200 OK)
{
  "primary_method": "Biogas Production",
  "alternative_methods": ["Pelletization", "Briquetting"],
  "equipment_needed": [
    "Biogas digester",
    "Gas collection system",
    "Purification unit"
  ],
  "estimated_yield": "1200 m³ biogas",
  "processing_time": "30-45 days",
  "investment_required": "₹2,50,000 - ₹5,00,000"
}
```

### 🌱 Carbon Calculation Endpoints

#### POST `/api/carbon/calculate`
Calculate environmental impact
```json
// Request
{
  "waste_type": "Sugarcane Bagasse",
  "quantity": "20.0",
  "processing_method": "Pelletization"
}

// Response (200 OK)
{
  "co2_saved": 156.8,
  "carbon_credits": 78.4,
  "environmental_impact": {
    "ghg_reduction": "156.8 kg CO₂ equivalent",
    "renewable_energy": "45.2 MWh potential",
    "waste_diverted": "20 tons from burning"
  },
  "economic_benefits": {
    "carbon_credit_value": "₹15,680",
    "fuel_value": "₹32,000",
    "total_benefit": "₹47,680"
  }
}
```

### 📄 Certificate Endpoints

#### POST `/api/certificate/generate`
Generate sustainability certificate PDF
```json
// Request
{
  "user_name": "John Farmer",
  "waste_type": "Rice Straw",
  "quantity": "10 tons",
  "co2_saved": 86.4,
  "carbon_credits": 52.0,
  "processing_method": "Pelletization"
}

// Response (200 OK)
// Content-Type: application/pdf
// Returns PDF file for download
```

### 📊 Dashboard Endpoints

#### GET `/api/dashboard/summary`
Get user dashboard summary
```json
// Response (200 OK)
{
  "total_analyses": 25,
  "total_co2_saved": 1250.6,
  "total_carbon_credits": 625.3,
  "total_fuel_potential": "125.5 tons",
  "favorite_waste_type": "Rice Straw",
  "recent_activity": [
    {
      "date": "2025-01-15",
      "waste_type": "Wheat Straw",
      "quantity": "5 tons",
      "co2_saved": 43.2
    }
  ]
}
```

#### GET `/api/dashboard/stats`
Get detailed user statistics
```json
// Response (200 OK)
{
  "monthly_stats": {
    "2025-01": {
      "analyses": 8,
      "co2_saved": 420.5,
      "carbon_credits": 210.25
    }
  },
  "waste_type_breakdown": {
    "Rice Straw": 12,
    "Wheat Straw": 8,
    "Sugarcane Bagasse": 5
  },
  "processing_methods": {
    "Pelletization": 15,
    "Biogas Production": 8,
    "Briquetting": 2
  }
}
```

#### POST `/api/dashboard/save-analysis`
Save analysis result to user dashboard
```json
// Request
{
  "waste_type": "Rice Straw",
  "quantity": "10",
  "unit": "tons",
  "co2_saved": 86.4,
  "carbon_credits": 52.0,
  "processing_method": "Pelletization",
  "analysis_date": "2025-01-15T10:30:00Z"
}

// Response (200 OK)
{
  "success": true,
  "message": "Analysis saved successfully",
  "analysis_id": "analysis_123456"
}
```

## 🔄 Response Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource not found |
| 422 | Validation Error | Request data validation failed |
| 500 | Internal Server Error | Server error |

## 📝 Data Models

### Waste Prediction Request
```typescript
interface WasteTextRequest {
  waste_type: string;      // "Rice Straw", "Wheat Straw", etc.
  quantity: string;        // Numeric string
  unit: string;           // "tons", "kg", "quintals"
  location?: string;      // Optional location context
}
```

### Prediction Response
```typescript
interface PredictionResponse {
  waste_type: string;
  confidence: number;      // 0.0 to 1.0
  processing_method: string;
  estimated_fuel_output: string;
  carbon_credits: number;
  co2_saved: number;
  recommendations: string[];
}
```

### Dashboard Stats
```typescript
interface DashboardStats {
  total_analyses: number;
  total_co2_saved: number;
  total_carbon_credits: number;
  total_fuel_potential: string;
  favorite_waste_type: string;
  recent_activity: Activity[];
}

interface Activity {
  date: string;           // ISO date string
  waste_type: string;
  quantity: string;
  co2_saved: number;
}
```

## 🚨 Error Handling

### Standard Error Response
```json
{
  "detail": "Error description",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

### Common Error Codes
- `VALIDATION_ERROR` - Request data validation failed
- `AUTHENTICATION_ERROR` - Invalid or missing authentication
- `MODEL_ERROR` - ML model prediction failed
- `FILE_ERROR` - File upload/processing error
- `STORAGE_ERROR` - Data storage operation failed

## 🧪 Testing Examples

### Image Upload Test
```bash
# Test image upload
curl -X POST "http://localhost:8000/api/predict/image" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test-images/rice-straw.jpg" \
  -v
```

### Text Analysis Test
```bash
# Test text prediction
curl -X POST "http://localhost:8000/api/predict/text" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "waste_type": "Rice Straw",
    "quantity": "10",
    "unit": "tons",
    "location": "Maharashtra, India"
  }'
```

### Dashboard Data Test
```bash
# Test dashboard summary
curl -X GET "http://localhost:8000/api/dashboard/summary" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📚 SDK & Client Libraries

### JavaScript/React Client
```javascript
// services/api.js
const API_BASE_URL = 'http://localhost:8000';

export const predictFromImage = async (file, token) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/api/predict/image`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  return response.json();
};

export const predictFromText = async (data, token) => {
  const response = await fetch(`${API_BASE_URL}/api/predict/text`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });
  
  return response.json();
};
```

### Python Client
```python
import requests

class AgriWasteAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.headers = {'Authorization': f'Bearer {token}'}
    
    def predict_from_text(self, waste_type, quantity, unit, location=None):
        data = {
            'waste_type': waste_type,
            'quantity': quantity,
            'unit': unit,
            'location': location
        }
        response = requests.post(
            f'{self.base_url}/api/predict/text',
            json=data,
            headers=self.headers
        )
        return response.json()
    
    def get_dashboard_summary(self):
        response = requests.get(
            f'{self.base_url}/api/dashboard/summary',
            headers=self.headers
        )
        return response.json()
```

## 🔍 Rate Limiting

Current implementation has no rate limiting. For production, consider:
- **Rate Limit:** 100 requests per minute per user
- **Burst Limit:** 10 requests per second
- **Daily Limit:** 1000 requests per day

## 📈 API Metrics

Monitor these key metrics:
- **Response Time:** Average < 2 seconds
- **Success Rate:** > 99%
- **ML Model Accuracy:** > 85%
- **Error Rate:** < 1%

---

**🚀 Ready to integrate with AgriWaste2Fuel API!**
