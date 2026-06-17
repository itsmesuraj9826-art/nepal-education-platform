@echo off
echo ================================================
echo  Nepal Education Platform - Local Setup
echo ================================================
echo.

:: ── 1. Create virtual environment ────────────────
echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.12+ first.
    pause & exit /b 1
)
echo       Done.

:: ── 2. Activate venv and install packages ────────
echo [2/4] Installing Python packages...
call venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed.
    pause & exit /b 1
)
echo       Done.

:: ── 3. Create MySQL database ─────────────────────
echo [3/4] Setting up MySQL database...
echo       Enter your MySQL root password when prompted.
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS nepal_edu_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
if errorlevel 1 (
    echo WARNING: Could not create database automatically.
    echo          Open MySQL Workbench and run:
    echo          CREATE DATABASE nepal_edu_platform;
    echo          Then run schema.sql manually.
) else (
    mysql -u root -p nepal_edu_platform < schema.sql
    echo       Database and schema created.
)

:: ── 4. Create uploads folder ─────────────────────
echo [4/4] Creating uploads directory...
if not exist uploads mkdir uploads
if not exist uploads\answer_sheets mkdir uploads\answer_sheets
echo       Done.

echo.
echo ================================================
echo  Setup complete!
echo.
echo  Next steps in PyCharm:
echo  1. File > Open > select this folder
echo  2. Add Interpreter: venv\Scripts\python.exe
echo  3. Edit .env - set DB_PASSWORD and AI keys
echo  4. Run app.py  (Flask server on http://127.0.0.1:5000)
echo ================================================
pause
