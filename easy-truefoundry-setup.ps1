# Team 3A - TrueFoundry आसान Deployment Script
# बस copy-paste करके run करें! 

Write-Host "🚀 AgriWaste2Fuel - Team 3A TrueFoundry Deployment" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Yellow

# Step 1: Check Python
Write-Host "`n📋 Step 1: Python Check कर रहे हैं..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python नहीं मिला! पहले Python install करें from python.org" -ForegroundColor Red
    exit
}

# Step 2: Install TrueFoundry CLI
Write-Host "`n📦 Step 2: TrueFoundry CLI install कर रहे हैं..." -ForegroundColor Cyan
pip install truefoundry
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ TrueFoundry CLI successfully installed!" -ForegroundColor Green
} else {
    Write-Host "❌ CLI install नहीं हुआ। Internet connection check करें" -ForegroundColor Red
    exit
}

# Step 3: Login
Write-Host "`n🔐 Step 3: TrueFoundry में login करें..." -ForegroundColor Cyan
Write-Host "Browser खुलेगा, अपने account से login करें" -ForegroundColor Yellow
tfy login

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Successfully logged in!" -ForegroundColor Green
} else {
    Write-Host "❌ Login नहीं हुआ। Retry करें या manually login करें" -ForegroundColor Red
    exit
}

# Step 4: Check current directory
Write-Host "`n📁 Step 4: Project directory check कर रहे हैं..." -ForegroundColor Cyan
$currentDir = Get-Location
Write-Host "Current directory: $currentDir" -ForegroundColor White

if (Test-Path "Backend\Dockerfile") {
    Write-Host "✅ Backend folder found!" -ForegroundColor Green
} else {
    Write-Host "❌ Backend folder नहीं मिला। सही directory में जाएं" -ForegroundColor Red
    Write-Host "Command: cd 'c:\Users\morey\OneDrive\Desktop\AgriWaste2Fuel'" -ForegroundColor Yellow
    exit
}

# Step 5: Create Project (Manual step message)
Write-Host "`n🏗️ Step 5: Project बनाना होगा (Manual)..." -ForegroundColor Cyan
Write-Host "अब ये steps browser में करें:" -ForegroundColor Yellow
Write-Host "1. https://app.truefoundry.com जाएं" -ForegroundColor White
Write-Host "2. 'Create New Project' पर click करें" -ForegroundColor White
Write-Host "3. Project name: agriwaste2fuel-team3a" -ForegroundColor White
Write-Host "4. Description: Team 3A AgriWaste2Fuel Backend" -ForegroundColor White
Write-Host "5. 'Create Project' पर click करें" -ForegroundColor White

Read-Host "`nProject बनाने के बाद Enter दबाएं..."

# Step 6: List projects
Write-Host "`n📋 Step 6: Available projects check कर रहे हैं..." -ForegroundColor Cyan
tfy project list

# Step 7: Set project (user will need to confirm project name)
Write-Host "`n🎯 Step 7: Project set करें..." -ForegroundColor Cyan
$projectName = Read-Host "अपना project name type करें (agriwaste2fuel-team3a)"
if ($projectName -eq "") {
    $projectName = "agriwaste2fuel-team3a"
}

tfy project set $projectName
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Project set successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Project set नहीं हुआ। Project name check करें" -ForegroundColor Red
}

# Step 8: Deploy database (Manual instruction)
Write-Host "`n🗄️ Step 8: Database deploy करना होगा (Manual)..." -ForegroundColor Cyan
Write-Host "Browser में ये steps follow करें:" -ForegroundColor Yellow
Write-Host "1. Project dashboard में 'Add Service' पर click करें" -ForegroundColor White
Write-Host "2. 'Database' option select करें" -ForegroundColor White
Write-Host "3. 'PostgreSQL' choose करें" -ForegroundColor White
Write-Host "4. Name: agriwaste-postgres" -ForegroundColor White
Write-Host "5. Version: 14" -ForegroundColor White
Write-Host "6. 'Deploy Database' पर click करें" -ForegroundColor White

Read-Host "`nDatabase deploy होने के बाद Enter दबाएं..."

# Step 9: Deploy backend service (Manual instruction)
Write-Host "`n🚀 Step 9: Backend service deploy करना होगा (Manual)..." -ForegroundColor Cyan
Write-Host "Browser में ये steps follow करें:" -ForegroundColor Yellow
Write-Host "1. 'Add Service' पर click करें again" -ForegroundColor White
Write-Host "2. 'Web Service' select करें" -ForegroundColor White
Write-Host "3. 'From GitHub' option choose करें" -ForegroundColor White
Write-Host "4. Repository: https://github.com/annam-ai-iitropar/team_3A" -ForegroundColor White
Write-Host "5. Branch: main" -ForegroundColor White
Write-Host "6. Folder Path: /Backend" -ForegroundColor White
Write-Host "7. Service Name: api-service" -ForegroundColor White
Write-Host "8. Port: 8000" -ForegroundColor White
Write-Host "9. 'Deploy Service' पर click करें" -ForegroundColor White

Read-Host "`nBackend deploy होने के बाद Enter दबाएं..."

# Step 10: Check deployment status
Write-Host "`n📊 Step 10: Deployment status check कर रहे हैं..." -ForegroundColor Cyan
tfy service list

# Step 11: Success message
Write-Host "`n🎉 Deployment Guide Complete!" -ForegroundColor Green
Write-Host "=============================`n" -ForegroundColor Yellow

Write-Host "✅ TrueFoundry CLI installed और login हो गया" -ForegroundColor Green
Write-Host "✅ Project setup guide दिया गया" -ForegroundColor Green
Write-Host "✅ Database और Backend deployment steps बताए गए" -ForegroundColor Green

Write-Host "`n🔗 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Browser में manually services deploy करें" -ForegroundColor White
Write-Host "2. Environment variables set करें" -ForegroundColor White
Write-Host "3. API URL copy करके frontend में use करें" -ForegroundColor White
Write-Host "4. Test करें कि सब कुछ काम कर रहा है" -ForegroundColor White

Write-Host "`n📞 Help के लिए:" -ForegroundColor Yellow
Write-Host "- TrueFoundry docs: https://docs.truefoundry.com" -ForegroundColor White
Write-Host "- Team 3A group में पूछें" -ForegroundColor White
Write-Host "- Manual guide: TRUEFOUNDRY_SIMPLE_GUIDE.md पढ़ें" -ForegroundColor White

Write-Host "`n🚀 Team 3A - All the best for deployment! 💪" -ForegroundColor Green
