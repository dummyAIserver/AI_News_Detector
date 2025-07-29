@echo off
echo ============================================
echo  FAKE NEWS DETECTOR - SETUP AND LAUNCH TOOL
echo  Compatible with Python 3.9
echo ============================================

:: Step 1: Check if Python 3.9 is installed
py -3.9 --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Python 3.9 is not installed or not added to PATH.
    echo ➤ Download it from https://www.python.org/downloads/release/python-390/
    pause
    exit /b
)

:: Step 2: Create virtual environment
echo Creating virtual environment with Python 3.9...
py -3.9 -m venv new

:: Step 3: Activate virtual environment and install requirements
echo Activating virtual environment...
call new\Scripts\activate

echo Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install flask requests scikit-learn nltk
pip install -r requirements.txt

:: Step 4: Launch the Flask app
echo Running the Flask app...
python app.py

:: Optional: Wait for user to close
pause
