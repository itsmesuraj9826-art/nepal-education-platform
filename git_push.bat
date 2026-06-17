@echo off
cd /d "%~dp0"
echo ================================================
echo  Nepal Education Platform - Git Push to GitHub
echo ================================================
echo.

:: Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH.
    echo Download from: https://git-scm.com
    pause & exit /b 1
)

:: Initialize repo if not already
if not exist ".git" (
    echo [1] Initializing Git repository...
    git init
    git branch -M main
) else (
    echo [1] Git repo already initialized.
)

:: Stage all files
echo [2] Staging all files...
git add .

:: Commit
echo [3] Committing...
git commit -m "Nepal Education Platform - Flask + Vercel Postgres"

:: Set remote
echo.
echo ================================================
echo  PASTE your GitHub repo URL below.
echo  Example: https://github.com/divyashi/nepal-edu.git
echo ================================================
set /p REPO_URL="GitHub repo URL: "

if "%REPO_URL%"=="" (
    echo ERROR: No URL entered.
    pause & exit /b 1
)

:: Remove existing remote if any, add new one
git remote remove origin 2>nul
git remote add origin %REPO_URL%

:: Push
echo [4] Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo Push failed. If you see authentication errors, run:
    echo   git config --global credential.helper manager
    echo Then try again.
) else (
    echo.
    echo ================================================
    echo  SUCCESS! Code is on GitHub.
    echo.
    echo  Next step: go to vercel.com and import this repo.
    echo ================================================
)
pause
