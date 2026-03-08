#!/bin/bash
"""
Bank Statement Engine - Linux Runner
====================================

This script sets up the virtual environment and runs the GUI application.
"""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python -m venv "$SCRIPT_DIR/.venv"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please ensure Python venv is available."
        exit 1
    fi
fi

# Activate virtual environment
source "$SCRIPT_DIR/.venv/bin/activate"

# Check if dependencies are installed
python -c "import customtkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r "$SCRIPT_DIR/requirements.txt"
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies."
        exit 1
    fi
fi

# Run the application
echo "Starting Bank Statement Engine..."
python "$SCRIPT_DIR/launcher.py"

# Deactivate virtual environment
deactivate