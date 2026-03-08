"""
Banking Account Information Collection Module
==============================================

This module provides user input forms for collecting banking account information
and validates all entries before storing them.
"""

from datetime import datetime
import re
from decimal import Decimal


class BankingAccountInfo:
    """Container for all banking account information"""

    def __init__(self):
        # Personal Information
        self.name = ""
        self.address_lines = []  # List of address lines
        self.pincode = ""
        self.email = ""
        self.mobile = ""

        # Account Information
        self.cif_number = ""
        self.account_number = ""
        self.account_type = ""  # e.g., "Savings Account"
        self.account_open_date = ""

        # Bank Details
        self.ifsc_code = ""
        self.micr_code = ""
        self.branch_address = ""

        # Compliance Information
        self.nominee_name = ""
        self.ckyc_no = ""

        # Statement Information
        self.statement_date = ""
        self.statement_time = ""
        self.statement_from_date = ""
        self.cleared_balance = Decimal("0.00")
        self.currency = "INR"

    def __repr__(self):
        return (f"BankingAccountInfo(name={self.name}, account={self.account_number}, "
                f"balance={self.cleared_balance})")


def validate_name(value):
    """Validate name is non-empty"""
    if not value or not value.strip():
        raise ValueError("Name cannot be empty")
    return value.strip().upper()


def validate_pincode(value):
    """Validate pincode is 6 digits"""
    value = value.strip()
    if not re.match(r"^\d{6}$", value):
        raise ValueError("Pincode must be exactly 6 digits")
    return value


def validate_email(value):
    """Validate email format"""
    value = value.strip()
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
        raise ValueError("Invalid email format")
    return value


def validate_date(value, format="%d-%m-%Y"):
    """Validate date format"""
    value = value.strip()
    try:
        datetime.strptime(value, format)
        return value
    except ValueError:
        raise ValueError(f"Invalid date format. Use {format}")


def validate_datetime(value):
    """Validate datetime format (DD-MM-YYYY HH:MM)"""
    value = value.strip()
    try:
        datetime.strptime(value, "%d-%m-%Y %H:%M")
        return value
    except ValueError:
        raise ValueError("Invalid datetime format. Use DD-MM-YYYY HH:MM")


def validate_ifsc(value):
    """Validate IFSC code (11 characters)"""
    value = value.strip().upper()
    if not re.match(r"^[A-Z]{4}0[A-Z0-9]{6}$", value):
        raise ValueError("Invalid IFSC code format (must be 11 characters, e.g., UBIN0533823)")
    return value


def validate_micr(value):
    """Validate MICR code (9 digits)"""
    value = value.strip()
    if not re.match(r"^\d{9}$", value):
        raise ValueError("MICR code must be exactly 9 digits")
    return value


def validate_amount(value):
    """Validate numeric amount"""
    try:
        amount = Decimal(value.strip())
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        return amount
    except:
        raise ValueError("Invalid amount format")


def validate_alphanumeric(value):
    """Validate alphanumeric string"""
    value = value.strip()
    if not value:
        raise ValueError("Value cannot be empty")
    if not re.match(r"^[a-zA-Z0-9]+$", value):
        raise ValueError("Must contain only alphanumeric characters")
    return value.upper()


def get_input(prompt, validator=None, allow_empty=False):
    """
    Get user input with validation

    Args:
        prompt: Question to display to user
        validator: Function to validate input
        allow_empty: Whether to allow empty input

    Returns:
        Validated input value
    """
    while True:
        try:
            value = input(prompt).strip()

            if not value:
                if allow_empty:
                    return ""
                raise ValueError("This field is required")

            if validator:
                return validator(value)
            return value
        except ValueError as e:
            print(f"  ❌ Error: {e}")
            print(f"  Please try again...\n")


def collect_account_info():
    """
    Interactive form to collect all banking account information

    Returns:
        BankingAccountInfo object with all user-provided data
    """
    print("\n" + "="*70)
    print("BANKING ACCOUNT INFORMATION COLLECTION FORM")
    print("="*70)

    info = BankingAccountInfo()

    # ===== PERSONAL INFORMATION =====
    print("\n📋 PERSONAL INFORMATION")
    print("-" * 70)

    info.name = get_input("Full Name: ", validate_name)

    print("\nAddress (enter up to 5 lines, press Enter without text when done):")
    for i in range(5):
        addr_line = input(f"  Line {i+1}: ").strip()
        if addr_line:
            info.address_lines.append(addr_line)
        else:
            break

    if not info.address_lines:
        raise ValueError("Address cannot be empty")

    info.pincode = get_input("Pincode (6 digits): ", validate_pincode)
    info.email = get_input("Email: ", validate_email)
    info.mobile = get_input("Mobile Number (optional): ", allow_empty=True)

    # ===== ACCOUNT INFORMATION =====
    print("\n💳 ACCOUNT INFORMATION")
    print("-" * 70)

    info.cif_number = get_input("CIF Number: ", validate_alphanumeric)
    info.account_number = get_input("Account Number: ", validate_alphanumeric)
    info.account_type = get_input("Account Type (e.g., Savings Account): ")
    info.account_open_date = get_input("Account Open Date (DD-MM-YYYY): ", validate_date)

    # ===== BANK DETAILS =====
    print("\n🏦 BANK DETAILS")
    print("-" * 70)

    info.ifsc_code = get_input("IFSC Code (e.g., UBIN0533823): ", validate_ifsc)
    info.micr_code = get_input("MICR Code (9 digits): ", validate_micr)
    info.branch_address = get_input("Branch Address: ")

    # ===== COMPLIANCE INFORMATION =====
    print("\n✅ COMPLIANCE INFORMATION")
    print("-" * 70)

    info.nominee_name = get_input("Nominee Name (optional): ", allow_empty=True)
    info.ckyc_no = get_input("CKYC Number (optional): ", allow_empty=True)

    # ===== STATEMENT INFORMATION =====
    print("\n📄 STATEMENT INFORMATION")
    print("-" * 70)

    info.statement_date = get_input("Statement Date (DD-MM-YYYY): ", validate_date)
    info.statement_time = get_input("Statement Time (HH:MM): ",
                                    lambda x: validate_datetime(f"{info.statement_date} {x}").split()[1])
    info.statement_from_date = get_input("Statement From Date (DD-MM-YYYY): ", validate_date)
    info.cleared_balance = get_input("Cleared Balance (₹): ", validate_amount)

    print("\n✅ Account information collected successfully!")
    print("="*70)

    return info


def load_account_info_from_dict(data):
    """
    Load account information from a dictionary (for JSON/API integration)

    Args:
        data: Dictionary containing account information

    Returns:
        BankingAccountInfo object
    """
    info = BankingAccountInfo()

    # Map dictionary keys to object attributes
    mapping = {
        'name': ('name', validate_name),
        'address_lines': ('address_lines', lambda x: x if isinstance(x, list) else [x]),
        'pincode': ('pincode', validate_pincode),
        'email': ('email', validate_email),
        'mobile': ('mobile', lambda x: x),
        'cif_number': ('cif_number', validate_alphanumeric),
        'account_number': ('account_number', validate_alphanumeric),
        'account_type': ('account_type', lambda x: x),
        'account_open_date': ('account_open_date', validate_date),
        'ifsc_code': ('ifsc_code', validate_ifsc),
        'micr_code': ('micr_code', validate_micr),
        'branch_address': ('branch_address', lambda x: x),
        'nominee_name': ('nominee_name', lambda x: x),
        'ckyc_no': ('ckyc_no', lambda x: x),
        'statement_date': ('statement_date', validate_date),
        'statement_time': ('statement_time', lambda x: x),
        'statement_from_date': ('statement_from_date', validate_date),
        'cleared_balance': ('cleared_balance', validate_amount),
    }

    for key, (attr, validator) in mapping.items():
        if key in data:
            try:
                setattr(info, attr, validator(data[key]))
            except Exception as e:
                print(f"Warning: Could not set {key}: {e}")

    return info


def create_sample_account_info():
    """Create a sample account info for testing"""
    info = BankingAccountInfo()

    # Personal Information
    info.name = "MR AJITH P D"
    info.address_lines = [
        "PANIKULANGARA HOUSE N",
        "ADUVASSERY,S",
        "ADUVASSERY P.O VIA",
        "CHENGAMANAD,ATHNI"
    ]
    info.pincode = "683585"
    info.email = "ajith@example.com"
    info.mobile = "8123458224"

    # Account Information
    info.cif_number = "202185132"
    info.account_number = "338202010016310"
    info.account_type = "Savings Account"
    info.account_open_date = "15-03-2020"

    # Bank Details
    info.ifsc_code = "UBIN0533823"
    info.micr_code = "533002105"
    info.branch_address = "ATHANI (ERNAKULAM DIST)"

    # Compliance Information
    info.nominee_name = "SNEHA AJITH"
    info.ckyc_no = "CKYC2021001234"

    # Statement Information
    info.statement_date = "04-02-2026"
    info.statement_time = "14:00"
    info.statement_from_date = "01-08-2025"
    info.cleared_balance = Decimal("1286456.00")

    return info
