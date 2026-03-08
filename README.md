# Statement Engine

A simple, logical, yet powerful bank statement generator for my own personal activities and stuff.


## Features

- **Modern GUI**: Built with CustomTkinter for a beautiful, modern interface
- **Account Information Management**: Collect and validate banking account details
- **PDF Generation**: Generate basic account info PDFs and full statements with transactions
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Sample Data**: Load sample data for testing and demonstration

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### System Dependencies (Linux)
On Arch Linux and similar distributions, install Tk GUI toolkit:
```bash
sudo pacman -S tk
```

On Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```

On Fedora/CentOS:
```bash
sudo dnf install tkinter
```

### Install Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt
```

### Required Packages
- `customtkinter` - Modern GUI framework
- `reportlab` - PDF generation
- `pillow` - Image processing
- `darkdetect` - System theme detection

## Usage

### Quick Start (Linux/macOS)
```bash
./run.sh
```

### Manual Launch Methods
```bash
# Activate virtual environment and run
source .venv/bin/activate
python launcher.py

# Direct GUI launch
source .venv/bin/activate
python gui.py

# Command-line version (basic PDF only)
python sbi.py

# Full statement generation (command-line)
python bank.py
```

## Application Features

### Account Information Tab
- Enter personal details (name, address, contact info)
- Account details (CIF, account number, type, etc.)
- Bank information (IFSC, MICR, branch)
- Statement period and balance information

### Statement Generation Tab
- **Basic Account Info PDF**: Generate a simple PDF with account details
- **Full Statement with Transactions**: Generate complete bank statement with all transactions, salaries, and adjustments

### Settings Tab
- Change color themes (blue, green, dark-blue)
- Toggle appearance mode (System, Light, Dark)
- Application information

## Testing

Run the test script to verify everything is working:

```bash
python test.py
```

This will test:
- Module imports
- Sample data creation
- Basic PDF generation

## Project Structure

```
statementengine/
├── gui.py              # Main GUI application
├── launcher.py         # Application launcher
├── bank.py             # Full statement generation logic
├── sbi.py              # Basic PDF generation
├── bank_form.py        # Account information validation
├── test.py             # Test script
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── bank_statement.pdf  # Generated PDF (after running)
└── __pycache__/       # Python bytecode
```

## Development

### Adding New Features
- GUI components are in `gui.py`
- PDF generation logic in `bank.py` and `sbi.py`
- Validation functions in `bank_form.py`

### Building for Distribution
The application can be packaged using tools like:
- PyInstaller (for executable)
- cx_Freeze (cross-platform)
- py2app (macOS)
- py2exe (Windows)

## License

This project is open source. See individual files for license information.

## Support

For issues or questions, please check the code comments or create an issue in the repository.
