#!/usr/bin/env python3
"""
Bank Statement Engine - Launcher
=================================

This script launches the GUI application for the Bank Statement Engine.

Requirements:
- Python 3.7+
- customtkinter
- reportlab
- pillow
- darkdetect

Install dependencies:
    pip install -r requirements.txt

Run the application:
    python launcher.py
"""

import sys
import os
import subprocess

def check_venv():
    """Check if we're in a virtual environment"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def activate_venv_and_run():
    """Activate virtual environment and run the application"""
    venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv')
    if os.path.exists(venv_path):
        # We're not in venv, so activate it and rerun
        python_exe = os.path.join(venv_path, 'bin', 'python')
        if os.name == 'nt':  # Windows
            python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')

        if os.path.exists(python_exe):
            # Rerun this script with the venv python
            os.execv(python_exe, [python_exe] + sys.argv)
        else:
            print("Virtual environment found but python executable not found.")
            print("Please run: source .venv/bin/activate && python launcher.py")
            sys.exit(1)
    else:
        print("Virtual environment not found.")
        print("Please create one with: python -m venv .venv")
        print("Then activate it: source .venv/bin/activate")
        print("Then install dependencies: pip install -r requirements.txt")
        sys.exit(1)

def main():
    # Check if we're in a virtual environment
    if not check_venv():
        activate_venv_and_run()
        return

    # Now we're in the virtual environment, import and run the GUI
    try:
        from gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("\nPlease ensure you're in the virtual environment and dependencies are installed:")
        print("  source .venv/bin/activate")
        print("  pip install -r requirements.txt")
        print("\nRequired packages:")
        print("  - customtkinter")
        print("  - reportlab")
        print("  - pillow")
        print("  - darkdetect")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()