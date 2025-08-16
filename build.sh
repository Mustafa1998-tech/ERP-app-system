#!/bin/bash
# Exit on error
set -e

# Install Python 3.11 if not already installed
if ! command -v python3.11 &> /dev/null; then
    echo "Installing Python 3.11..."
    apt-get update && apt-get install -y python3.11 python3.11-dev python3.11-venv
fi

# Create a virtual environment with Python 3.11
python3.11 -m venv /opt/render/project/venv

# Activate the virtual environment
source /opt/render/project/venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run collectstatic if needed
python manage.py collectstatic --noinput --clear

# Run migrations
python manage.py migrate
