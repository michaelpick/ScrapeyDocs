@echo off
:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b
)

:: Set up the Python virtual environment
echo Setting up the virtual environment...
python -m venv venv

if not exist "venv\Scripts\activate" (
    echo Failed to create the virtual environment. Exiting...
    pause
    exit /b
)

:: Activate the virtual environment
echo Activating the virtual environment...
call venv\Scripts\activate

:: Install the required Python packages
echo Installing requirements...
pip install --upgrade pip
pip install requests beautifulsoup4 html2text

:: Run the documentation-scraper.py script
echo Running the scraping script...
python documentation-scraper.py

:: Deactivate the virtual environment
echo Deactivating the virtual environment...
deactivate

:: Notify user of completion and keep the window open
echo Script execution completed. Check the 'Outputs' directory for results.
pause
