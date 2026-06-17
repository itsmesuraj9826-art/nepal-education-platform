@echo off
cd /d "C:\Users\ASUS\Desktop\nepal_education_platform"
echo Cleaning up old .git if any...
if exist ".git" rmdir /s /q ".git"
echo Initializing git...
git init
git branch -M main
git config user.email "kdivyashi24@tbc.edu.np"
git config user.name "Divyashi Karna"
echo Adding all files...
git add .
echo Committing...
git commit -m "Nepal Education Platform - Flask + Vercel Postgres (All 7 phases)"
echo Setting remote...
git remote add origin https://github.com/itsmesuraj9826-art/nepal-education-platform.git
echo Pushing to GitHub...
git push -u origin main
echo.
echo ============================================
echo Done! Check above for any errors.
echo ============================================
pause
