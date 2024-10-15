#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Set up the Python virtual environment
echo "Setting up the virtual environment..."
python3 -m venv venv

if [ ! -f "venv/bin/activate" ]; then
    echo "Failed to create the virtual environment. Exiting..."
    exit 1
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Install the required Python packages
echo "Installing requirements..."
pip install --upgrade pip
pip install requests beautifulsoup4 html2text

# Run the documentation-scraper.py script
echo "Running the scraping script..."
python3 documentation-scraper.py

# Deactivate the virtual environment
echo "Deactivating the virtual environment..."
deactivate

# Notify user of completion
echo "Script execution completed. Check the 'Outputs' directory for results."
