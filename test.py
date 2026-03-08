#!/usr/bin/env python3
"""
Test script for Bank Statement Engine
=====================================

This script tests the basic functionality without launching the GUI.
"""

import sys
import os
import subprocess

def check_venv():
    """Check if we're in a virtual environment"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def activate_venv_and_run():
    """Activate virtual environment and run the tests"""
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
            print("Please run: source .venv/bin/activate && python test.py")
            return False
    else:
        print("Virtual environment not found.")
        print("Please create one with: python -m venv .venv")
        print("Then activate it: source .venv/bin/activate")
        print("Then install dependencies: pip install -r requirements.txt")
        return False
    return True

def test_imports():
    """Test that all modules can be imported"""
    try:
        from bank_form import BankingAccountInfo, create_sample_account_info
        from bank import generate_statement_pdf
        from sbi import generate_pdf
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_sample_data():
    """Test sample data creation"""
    try:
        from bank_form import create_sample_account_info
        info = create_sample_account_info()
        assert info.name == "MR AJITH P D"
        assert info.account_number == "338202010016310"
        assert info.cleared_balance == 1286456.00
        print("✓ Sample data creation successful")
        return True
    except Exception as e:
        print(f"✗ Sample data error: {e}")
        return False

def test_basic_pdf():
    """Test basic PDF generation"""
    try:
        from bank_form import create_sample_account_info
        from sbi import generate_pdf

        info = create_sample_account_info()
        data = {
            "name": info.name,
            "address": " ".join(info.address_lines),
            "pin": info.pincode,
            "email": info.email,
            "phone": info.mobile,
            "cif": info.cif_number,
            "acc_number": info.account_number,
            "acc_type": info.account_type,
            "acc_open_date": info.account_open_date,
            "ifsc": info.ifsc_code,
            "micr": info.micr_code,
            "branch_address": info.branch_address,
            "nominee": info.nominee_name,
            "ckyc": info.ckyc_no,
            "statement_datetime": f"{info.statement_date} {info.statement_time}",
            "statement_from": info.statement_from_date,
            "statement_to": info.statement_to_date,
            "balance": str(info.cleared_balance),
        }

        generate_pdf(data)
        print("✓ Basic PDF generation successful")
        return True
    except Exception as e:
        print(f"✗ Basic PDF generation error: {e}")
        return False

def main():
    # Check if we're in a virtual environment
    if not check_venv():
        if not activate_venv_and_run():
            return

    print("Testing Bank Statement Engine...")
    print("=" * 40)

    tests = [
        test_imports,
        test_sample_data,
        test_basic_pdf,
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()

    print(f"Results: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo run the GUI application:")
        print("  python launcher.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()