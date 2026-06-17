@echo off
cd /d "C:\Users\ASUS\Desktop\nepal_education_platform"

echo =====================================================
echo  Nepal Education Platform - Vercel Deployment
echo =====================================================
echo.

:: Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Install from https://nodejs.org
    pause & exit /b 1
)

:: Install Vercel CLI if not present
vercel --version >nul 2>&1
if errorlevel 1 (
    echo [1/5] Installing Vercel CLI...
    npm install -g vercel
) else (
    echo [1/5] Vercel CLI already installed.
)

echo.
echo [2/5] Logging into Vercel...
echo      A browser window will open — click CONFIRM in the email/browser.
echo.
vercel login

echo.
echo [3/5] Deploying project to Vercel...
echo      When prompted:
echo        - Set up and deploy? Y
echo        - Which scope? (choose your account)
echo        - Link to existing project? N
echo        - Project name: nepal-education-platform
echo        - Directory: ./ (just press Enter)
echo        - Override settings? N
echo.
vercel deploy --yes

echo.
echo [4/5] Setting environment variables...
echo      (Press Enter to accept prompts, type values when asked)
echo.

vercel env add SECRET_KEY production
vercel env add JWT_SECRET_KEY production
vercel env add FLASK_ENV production
vercel env add AI_PROVIDER production

echo.
echo [5/5] Final production deployment...
vercel --prod

echo.
echo =====================================================
echo  DONE! Your app is live on Vercel.
echo.
echo  NEXT STEPS:
echo  1. Go to vercel.com/dashboard
echo  2. Open your project - Storage - Create Database - Postgres
echo  3. Name it "nepal-edu-db" and Connect to Project
echo  4. Go to Storage - Query tab
echo  5. Paste schema_postgres.sql content and Run
echo =====================================================
pause
