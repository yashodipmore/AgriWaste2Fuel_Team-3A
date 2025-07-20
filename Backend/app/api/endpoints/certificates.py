"""
Certificate generation endpoint for carbon credit certificates
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, Response
import uuid
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json

from app.models.schemas import CertificateRequest, CertificateResponse
from app.core.config import settings

# Import PDF generation function
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from pdf_generator import generate_pdf_certificate

router = APIRouter()

# Mock certificate templates and data
CERTIFICATE_TEMPLATES = {
    "biogas": {
        "title": "Carbon Credit Certificate - Biogas Production",
        "description": "This certificate validates the carbon credits earned through biogas production from agricultural waste",
        "verification_authority": "AgriWaste2Fuel Platform - Team 3A",
        "standard": "Verified Carbon Standard (VCS)"
    },
    "compost": {
        "title": "Carbon Credit Certificate - Organic Composting", 
        "description": "This certificate validates the carbon credits earned through organic composting of agricultural waste",
        "verification_authority": "AgriWaste2Fuel Platform - Team 3A",
        "standard": "Gold Standard for Global Goals"
    }
}

def generate_certificate_id() -> str:
    """Generate unique certificate ID"""
    timestamp = datetime.now().strftime("%Y%m%d")
    unique_suffix = str(uuid.uuid4())[:8].upper()
    return f"AW2F-{timestamp}-{unique_suffix}"

def generate_verification_code() -> str:
    """Generate verification code"""
    return str(uuid.uuid4()).replace('-', '').upper()[:12]

def create_certificate_data(request: CertificateRequest, cert_id: str, verification_code: str) -> Dict[str, Any]:
    """Create certificate data structure"""
    
    # Determine template based on processing method
    template_key = "biogas" if "biogas" in request.processing_method.lower() else "compost"
    template = CERTIFICATE_TEMPLATES[template_key]
    
    # Calculate certificate value
    credit_rate = 2500  # INR per credit (mock rate)
    estimated_value = request.carbon_credits * credit_rate
    
    return {
        "certificate_id": cert_id,
        "verification_code": verification_code,
        "template": template,
        "user_data": {
            "name": request.user_name,
            "issue_date": datetime.now().isoformat(),
            "expiry_date": (datetime.now() + timedelta(days=365)).isoformat(),
        },
        "waste_data": {
            "waste_type": request.waste_type,
            "processing_method": request.processing_method,
            "analysis_id": request.analysis_id or "MOCK_ANALYSIS_001"
        },
        "environmental_impact": {
            "co2_saved": request.co2_saved,
            "co2_saved_unit": "tons CO₂e",
            "carbon_credits": request.carbon_credits,
            "estimated_value": f"₹{estimated_value:,.2f}",
            "environmental_benefit": f"Equivalent to removing {request.co2_saved * 0.5:.1f} cars from road for 1 year"
        },
        "verification": {
            "verification_status": "Verified",
            "verification_date": datetime.now().isoformat(),
            "next_verification": (datetime.now() + timedelta(days=180)).isoformat(),
            "authority": template["verification_authority"],
            "standard": template["standard"]
        }
    }

def generate_mock_pdf_content(cert_data: Dict[str, Any]) -> str:
    """Generate mock PDF content (HTML format for now)"""
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Carbon Credit Certificate</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ text-align: center; border-bottom: 3px solid #2E7D32; padding-bottom: 20px; }}
        .title {{ font-size: 24px; color: #2E7D32; font-weight: bold; }}
        .subtitle {{ font-size: 16px; color: #555; margin-top: 10px; }}
        .content {{ margin: 30px 0; }}
        .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #4CAF50; }}
        .highlight {{ background-color: #E8F5E8; padding: 10px; border-radius: 5px; }}
        .footer {{ text-align: center; margin-top: 40px; font-size: 12px; color: #666; }}
        .verification {{ background-color: #F3E5F5; padding: 15px; border-radius: 8px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">{cert_data['template']['title']}</div>
        <div class="subtitle">Certificate ID: {cert_data['certificate_id']}</div>
        <div class="subtitle">Issued: {datetime.fromisoformat(cert_data['user_data']['issue_date']).strftime('%B %d, %Y')}</div>
    </div>
    
    <div class="content">
        <div class="section">
            <h3>Certificate Holder</h3>
            <p><strong>Name:</strong> {cert_data['user_data']['name']}</p>
            <p><strong>Analysis ID:</strong> {cert_data['waste_data']['analysis_id']}</p>
        </div>
        
        <div class="section">
            <h3>Waste Processing Details</h3>
            <p><strong>Waste Type:</strong> {cert_data['waste_data']['waste_type']}</p>
            <p><strong>Processing Method:</strong> {cert_data['waste_data']['processing_method']}</p>
        </div>
        
        <div class="section highlight">
            <h3>Environmental Impact</h3>
            <p><strong>CO₂ Saved:</strong> {cert_data['environmental_impact']['co2_saved']} {cert_data['environmental_impact']['co2_saved_unit']}</p>
            <p><strong>Carbon Credits Earned:</strong> {cert_data['environmental_impact']['carbon_credits']} credits</p>
            <p><strong>Estimated Value:</strong> {cert_data['environmental_impact']['estimated_value']}</p>
            <p><strong>Environmental Benefit:</strong> {cert_data['environmental_impact']['environmental_benefit']}</p>
        </div>
        
        <div class="verification">
            <h3>Verification Details</h3>
            <p><strong>Verification Code:</strong> {cert_data['verification_code']}</p>
            <p><strong>Status:</strong> {cert_data['verification']['verification_status']}</p>
            <p><strong>Authority:</strong> {cert_data['verification']['authority']}</p>
            <p><strong>Standard:</strong> {cert_data['verification']['standard']}</p>
            <p><strong>Valid Until:</strong> {datetime.fromisoformat(cert_data['user_data']['expiry_date']).strftime('%B %d, %Y')}</p>
        </div>
    </div>
    
    <div class="footer">
        <p>This certificate is digitally generated and verified by the AgriWaste2Fuel Platform.</p>
        <p>Developed by Team 3A under Annam.ai Hackathon 2025</p>
        <p>For verification, visit our platform with code: {cert_data['verification_code']}</p>
        <p>{cert_data['template']['description']}</p>
    </div>
</body>
</html>
"""
    return html_content

@router.post("/generate-certificate")
async def generate_certificate(request: CertificateRequest):
    """
    Generate carbon credit certificate for successful waste processing
    
    **Features:**
    - Unique certificate ID generation
    - Professional PDF certificate creation using ReportLab
    - Verification code generation
    - Environmental impact summary
    - Returns PDF content directly for download
    """
    
    try:
        # Generate unique identifiers
        cert_id = generate_certificate_id()
        verification_code = generate_verification_code()
        
        # Create certificate data for PDF generation
        cert_data = {
            'certificate_id': cert_id,
            'user_name': request.user_name,
            'waste_type': request.waste_type,
            'processing_method': request.processing_method,
            'co2_saved': request.co2_saved,
            'carbon_credits': request.carbon_credits,
            'issue_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'verification_code': verification_code,
            'analysis_id': request.analysis_id or 'N/A'
        }
        
        # Generate PDF certificate
        pdf_content = generate_pdf_certificate(cert_data)
        
        # Save certificate for record keeping
        cert_filename = f"certificate_{cert_id}.pdf"
        cert_path = os.path.join(settings.CERTIFICATES_DIR, cert_filename)
        
        # Save PDF file
        with open(cert_path, 'wb') as f:
            f.write(pdf_content)
        
        # Save certificate data as JSON for verification
        data_filename = f"cert_data_{cert_id}.json"
        data_path = os.path.join(settings.CERTIFICATES_DIR, data_filename)
        
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(cert_data, f, indent=2, default=str)
        
        # Return PDF content directly as downloadable response
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=AgriWaste2Fuel_Team3A_Certificate_{cert_id}.pdf"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Certificate generation failed: {str(e)}"
        )

@router.get("/download/{certificate_id}")
async def download_certificate(certificate_id: str):
    """
    Download certificate file by certificate ID
    """
    try:
        cert_filename = f"certificate_{certificate_id}.html"
        cert_path = os.path.join(settings.CERTIFICATES_DIR, cert_filename)
        
        if not os.path.exists(cert_path):
            raise HTTPException(
                status_code=404,
                detail="Certificate not found"
            )
        
        return FileResponse(
            path=cert_path,
            filename=f"carbon_credit_certificate_{certificate_id}.html",
            media_type="text/html"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Certificate download failed: {str(e)}"
        )

@router.get("/verify/{verification_code}")
async def verify_certificate(verification_code: str):
    """
    Verify certificate authenticity using verification code
    """
    try:
        # Search for certificate with matching verification code
        certificates_dir = settings.CERTIFICATES_DIR
        
        for filename in os.listdir(certificates_dir):
            if filename.startswith("cert_data_") and filename.endswith(".json"):
                file_path = os.path.join(certificates_dir, filename)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    cert_data = json.load(f)
                
                if cert_data.get("verification_code") == verification_code:
                    # Check if certificate is still valid
                    expiry_date = datetime.fromisoformat(cert_data['user_data']['expiry_date'])
                    is_valid = datetime.now() < expiry_date
                    
                    return {
                        "success": True,
                        "certificate_found": True,
                        "is_valid": is_valid,
                        "certificate_id": cert_data["certificate_id"],
                        "user_name": cert_data["user_data"]["name"],
                        "issue_date": cert_data["user_data"]["issue_date"],
                        "expiry_date": cert_data["user_data"]["expiry_date"],
                        "co2_saved": cert_data["environmental_impact"]["co2_saved"],
                        "carbon_credits": cert_data["environmental_impact"]["carbon_credits"],
                        "verification_status": cert_data["verification"]["verification_status"],
                        "message": "Certificate verified successfully" if is_valid else "Certificate has expired"
                    }
        
        # Certificate not found
        return {
            "success": False,
            "certificate_found": False,
            "message": "Certificate not found with the provided verification code"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Certificate verification failed: {str(e)}"
        )

@router.get("/list/{user_name}")
async def list_user_certificates(user_name: str):
    """
    List all certificates for a specific user
    """
    try:
        certificates = []
        certificates_dir = settings.CERTIFICATES_DIR
        
        for filename in os.listdir(certificates_dir):
            if filename.startswith("cert_data_") and filename.endswith(".json"):
                file_path = os.path.join(certificates_dir, filename)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    cert_data = json.load(f)
                
                if cert_data["user_data"]["name"].lower() == user_name.lower():
                    certificates.append({
                        "certificate_id": cert_data["certificate_id"],
                        "issue_date": cert_data["user_data"]["issue_date"],
                        "expiry_date": cert_data["user_data"]["expiry_date"],
                        "waste_type": cert_data["waste_data"]["waste_type"],
                        "processing_method": cert_data["waste_data"]["processing_method"],
                        "co2_saved": cert_data["environmental_impact"]["co2_saved"],
                        "carbon_credits": cert_data["environmental_impact"]["carbon_credits"],
                        "estimated_value": cert_data["environmental_impact"]["estimated_value"],
                        "download_url": f"/api/v1/certificates/download/{cert_data['certificate_id']}"
                    })
        
        return {
            "success": True,
            "user_name": user_name,
            "certificates": certificates,
            "total_certificates": len(certificates),
            "total_co2_saved": sum(cert["co2_saved"] for cert in certificates),
            "total_credits": sum(cert["carbon_credits"] for cert in certificates),
            "message": f"Found {len(certificates)} certificates for {user_name}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list certificates: {str(e)}"
        )

@router.get("/generate-certificate", response_model=CertificateResponse)
async def generate_certificate_get(
    user_id: Optional[str] = Query(None, description="User identifier"),
    co2_saved: Optional[float] = Query(None, description="CO2 equivalent saved in tons"),
    waste_type: Optional[str] = Query(None, description="Type of waste processed"),
    processing_method: Optional[str] = Query(None, description="Processing method used")
):
    """
    Generate carbon credit certificate via GET request (for frontend compatibility)
    
    **Query Parameters:**
    - user_id: User identifier
    - co2_saved: CO2 equivalent saved in tons
    - waste_type: Type of waste processed
    - processing_method: Processing method used
    """
    
    # Set default values and calculate carbon credits
    co2_value = co2_saved or 2.5
    carbon_credits_value = co2_value * 0.95  # Mock calculation: 95% efficiency
    
    # Create request object from query parameters
    request_data = CertificateRequest(
        user_name=user_id or "Anonymous User",
        co2_saved=co2_value,
        carbon_credits=carbon_credits_value,
        waste_type=waste_type or "Agricultural Waste",
        processing_method=processing_method or "biogas",
        analysis_id=f"ANALYSIS_{uuid.uuid4().hex[:8].upper()}"
    )
    
    # Call the main certificate generation function
    return await generate_certificate(request_data)
