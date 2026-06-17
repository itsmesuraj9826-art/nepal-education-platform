@echo off
cd /d "C:\Users\ASUS\Desktop\nepal_education_platform"
echo Triggering Vercel deployment via git push...
git add .
git commit -m "Trigger Vercel deployment - Nepal Education Platform"
git push origin main
echo.
echo Done! Check vercel.com for deployment status.
pause
