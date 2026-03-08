#!/usr/bin/env python3
"""
Bank Statement Engine - GUI Application
=======================================

Cross-platform desktop application for generating bank statements and PDFs.

Features:
- Modern GUI with CustomTkinter
- Account information collection
- PDF generation for account details
- Full statement generation with transactions
- Cross-platform support (Windows, Linux, macOS)

Author: GitHub Copilot
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import sys
from datetime import datetime
from bank_form import BankingAccountInfo, collect_account_info, create_sample_account_info
from sbi import generate_pdf as generate_basic_pdf
from bank import generate_statement_pdf

# Set appearance
ctk.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class BankStatementGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Bank Statement Engine")
        self.geometry("900x700")
        self.resizable(True, True)

        # Initialize data
        self.account_info = BankingAccountInfo()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Create tabview
        self.tabview = ctk.CTkTabview(self, width=850, height=650)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # Create tabs
        self.tabview.add("Account Info")
        self.tabview.add("Statement Generation")
        self.tabview.add("Settings")

        # Setup each tab
        self.setup_account_info_tab()
        self.setup_statement_tab()
        self.setup_settings_tab()

    def setup_account_info_tab(self):
        tab = self.tabview.tab("Account Info")

        # Personal Information Section
        personal_frame = ctk.CTkFrame(tab)
        personal_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(personal_frame, text="Personal Information", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # Name
        name_frame = ctk.CTkFrame(personal_frame)
        name_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(name_frame, text="Full Name:").pack(side="left", padx=5)
        self.name_entry = ctk.CTkEntry(name_frame, placeholder_text="Enter full name")
        self.name_entry.pack(side="right", padx=5, fill="x", expand=True)

        # Address
        addr_frame = ctk.CTkFrame(personal_frame)
        addr_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(addr_frame, text="Address:").pack(side="left", padx=5)
        self.address_entry = ctk.CTkEntry(addr_frame, placeholder_text="Enter address")
        self.address_entry.pack(side="right", padx=5, fill="x", expand=True)

        # Pincode and Email
        contact_frame = ctk.CTkFrame(personal_frame)
        contact_frame.pack(fill="x", padx=5, pady=2)

        pin_frame = ctk.CTkFrame(contact_frame)
        pin_frame.pack(side="left", fill="x", expand=True, padx=2)
        ctk.CTkLabel(pin_frame, text="Pincode:").pack(side="left", padx=5)
        self.pincode_entry = ctk.CTkEntry(pin_frame, placeholder_text="6 digits")
        self.pincode_entry.pack(side="right", padx=5, fill="x", expand=True)

        email_frame = ctk.CTkFrame(contact_frame)
        email_frame.pack(side="right", fill="x", expand=True, padx=2)
        ctk.CTkLabel(email_frame, text="Email:").pack(side="left", padx=5)
        self.email_entry = ctk.CTkEntry(email_frame, placeholder_text="email@example.com")
        self.email_entry.pack(side="right", padx=5, fill="x", expand=True)

        # Mobile
        mobile_frame = ctk.CTkFrame(personal_frame)
        mobile_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(mobile_frame, text="Mobile:").pack(side="left", padx=5)
        self.mobile_entry = ctk.CTkEntry(mobile_frame, placeholder_text="10 digits")
        self.mobile_entry.pack(side="right", padx=5, fill="x", expand=True)

        # Account Information Section
        account_frame = ctk.CTkFrame(tab)
        account_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(account_frame, text="Account Information", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # Bank Selection
        bank_select_frame = ctk.CTkFrame(account_frame)
        bank_select_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(bank_select_frame, text="Select Bank:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=5)
        self.bank_var = ctk.StringVar(value="sbi")
        self.bank_menu = ctk.CTkOptionMenu(bank_select_frame, values=["sbi", "fb"], variable=self.bank_var,
                                         font=ctk.CTkFont(size=12))
        self.bank_menu.pack(side="right", padx=5)

        # CIF and Account Number
        cif_acc_frame = ctk.CTkFrame(account_frame)
        cif_acc_frame.pack(fill="x", padx=5, pady=2)

        cif_frame = ctk.CTkFrame(cif_acc_frame)
        cif_frame.pack(side="left", fill="x", expand=True, padx=2)
        ctk.CTkLabel(cif_frame, text="CIF Number:").pack(side="left", padx=5)
        self.cif_entry = ctk.CTkEntry(cif_frame, placeholder_text="CIF number")
        self.cif_entry.pack(side="right", padx=5, fill="x", expand=True)

        acc_frame = ctk.CTkFrame(cif_acc_frame)
        acc_frame.pack(side="right", fill="x", expand=True, padx=2)
        ctk.CTkLabel(acc_frame, text="Account Number:").pack(side="left", padx=5)
        self.account_entry = ctk.CTkEntry(acc_frame, placeholder_text="Account number")
        self.account_entry.pack(side="right", padx=5, fill="x", expand=True)

        # Account Type and Open Date
        type_date_frame = ctk.CTkFrame(account_frame)
        type_date_frame.pack(fill="x", padx=5, pady=2)

        type_frame = ctk.CTkFrame(type_date_frame)
        type_frame.pack(side="left", fill="x", expand=True, padx=2)
        ctk.CTkLabel(type_frame, text="Account Type:").pack(side="left", padx=5)
        self.account_type_entry = ctk.CTkEntry(type_date_frame, placeholder_text="e.g., Savings Account")
        self.account_type_entry.pack(side="right", padx=5, fill="x", expand=True)

        date_frame = ctk.CTkFrame(type_date_frame)
        date_frame.pack(side="right", fill="x", expand=True, padx=2)
        ctk.CTkLabel(date_frame, text="Open Date:").pack(side="left", padx=5)
        self.account_open_date_entry = ctk.CTkEntry(date_frame, placeholder_text="DD-MM-YYYY")
        self.account_open_date_entry.pack(side="right", padx=5, fill="x", expand=True)

        # Bank Details Section
        bank_frame = ctk.CTkFrame(tab)
        bank_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(bank_frame, text="Bank Details", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # IFSC and MICR
        ifsc_micr_frame = ctk.CTkFrame(bank_frame)
        ifsc_micr_frame.pack(fill="x", padx=5, pady=2)

        ifsc_frame = ctk.CTkFrame(ifsc_micr_frame)
        ifsc_frame.pack(side="left", fill="x", expand=True, padx=2)
        ctk.CTkLabel(ifsc_frame, text="IFSC Code:").pack(side="left", padx=5)
        self.ifsc_entry = ctk.CTkEntry(ifsc_frame, placeholder_text="e.g., SBIN0001234")
        self.ifsc_entry.pack(side="right", padx=5, fill="x", expand=True)

        micr_frame = ctk.CTkFrame(ifsc_micr_frame)
        micr_frame.pack(side="right", fill="x", expand=True, padx=2)
        ctk.CTkLabel(micr_frame, text="MICR Code:").pack(side="left", padx=5)
        self.micr_entry = ctk.CTkEntry(micr_frame, placeholder_text="MICR code")
        self.micr_entry.pack(side="right", padx=5, fill="x", expand=True)

        # Branch Address
        branch_frame = ctk.CTkFrame(bank_frame)
        branch_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(branch_frame, text="Branch Address:").pack(side="left", padx=5)
        self.branch_entry = ctk.CTkEntry(branch_frame, placeholder_text="Branch address")
        self.branch_entry.pack(side="right", padx=5, fill="x", expand=True)

        # Additional Information Section
        additional_frame = ctk.CTkFrame(tab)
        additional_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(additional_frame, text="Additional Information", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # Nominee and CKYC
        nom_ckyc_frame = ctk.CTkFrame(additional_frame)
        nom_ckyc_frame.pack(fill="x", padx=5, pady=2)

        nom_frame = ctk.CTkFrame(nom_ckyc_frame)
        nom_frame.pack(side="left", fill="x", expand=True, padx=2)
        ctk.CTkLabel(nom_frame, text="Nominee Name:").pack(side="left", padx=5)
        self.nominee_entry = ctk.CTkEntry(nom_frame, placeholder_text="Nominee name")
        self.nominee_entry.pack(side="right", padx=5, fill="x", expand=True)

        ckyc_frame = ctk.CTkFrame(nom_ckyc_frame)
        ckyc_frame.pack(side="right", fill="x", expand=True, padx=2)
        ctk.CTkLabel(ckyc_frame, text="CKYC Number:").pack(side="left", padx=5)
        self.ckyc_entry = ctk.CTkEntry(ckyc_frame, placeholder_text="CKYC number")
        self.ckyc_entry.pack(side="right", padx=5, fill="x", expand=True)

        # Statement Information
        stmt_frame = ctk.CTkFrame(additional_frame)
        stmt_frame.pack(fill="x", padx=5, pady=2)

        stmt_date_frame = ctk.CTkFrame(stmt_frame)
        stmt_date_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(stmt_date_frame, text="Statement Date & Time:").pack(side="left", padx=5)
        self.stmt_datetime_entry = ctk.CTkEntry(stmt_date_frame, placeholder_text="DD-MM-YYYY HH:MM")
        self.stmt_datetime_entry.pack(side="right", padx=5, fill="x", expand=True)

        stmt_period_frame = ctk.CTkFrame(stmt_frame)
        stmt_period_frame.pack(fill="x", padx=5, pady=2)

        from_frame = ctk.CTkFrame(stmt_period_frame)
        from_frame.pack(side="left", fill="x", expand=True, padx=2)
        ctk.CTkLabel(from_frame, text="From Date:").pack(side="left", padx=5)
        self.from_date_entry = ctk.CTkEntry(from_frame, placeholder_text="DD-MM-YYYY")
        self.from_date_entry.pack(side="right", padx=5, fill="x", expand=True)

        to_frame = ctk.CTkFrame(stmt_period_frame)
        to_frame.pack(side="right", fill="x", expand=True, padx=2)
        ctk.CTkLabel(to_frame, text="To Date:").pack(side="left", padx=5)
        self.to_date_entry = ctk.CTkEntry(to_frame, placeholder_text="DD-MM-YYYY")
        self.to_date_entry.pack(side="right", padx=5, fill="x", expand=True)

        balance_frame = ctk.CTkFrame(stmt_frame)
        balance_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(balance_frame, text="Cleared Balance:").pack(side="left", padx=5)
        self.balance_entry = ctk.CTkEntry(balance_frame, placeholder_text="Amount in INR")
        self.balance_entry.pack(side="right", padx=5, fill="x", expand=True)

        # Buttons
        button_frame = ctk.CTkFrame(tab)
        button_frame.pack(pady=10, padx=10, fill="x")

        self.save_button = ctk.CTkButton(button_frame, text="Save Account Info", command=self.save_account_info)
        self.save_button.pack(side="left", padx=5)

        self.load_button = ctk.CTkButton(button_frame, text="Load Sample Data", command=self.load_sample_data)
        self.load_button.pack(side="left", padx=5)

        self.clear_button = ctk.CTkButton(button_frame, text="Clear All", command=self.clear_form)
        self.clear_button.pack(side="right", padx=5)

    def setup_statement_tab(self):
        tab = self.tabview.tab("Statement Generation")

        # Options
        options_frame = ctk.CTkFrame(tab)
        options_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(options_frame, text="Statement Generation Options", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # Statement type selection
        self.stmt_type_var = ctk.StringVar(value="basic")
        basic_radio = ctk.CTkRadioButton(options_frame, text="Basic Account Info PDF", variable=self.stmt_type_var, value="basic")
        basic_radio.pack(pady=5, padx=20, anchor="w")

        full_radio = ctk.CTkRadioButton(options_frame, text="Full Statement with Transactions", variable=self.stmt_type_var, value="full")
        full_radio.pack(pady=5, padx=20, anchor="w")

        # Generate button
        generate_frame = ctk.CTkFrame(tab)
        generate_frame.pack(pady=20, padx=10, fill="x")

        self.generate_button = ctk.CTkButton(generate_frame, text="Generate PDF", command=self.generate_pdf,
                                           font=ctk.CTkFont(size=14, weight="bold"), height=40)
        self.generate_button.pack(pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(generate_frame, text="", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=5)

    def setup_settings_tab(self):
        tab = self.tabview.tab("Settings")

        # Appearance settings
        appearance_frame = ctk.CTkFrame(tab)
        appearance_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(appearance_frame, text="Appearance", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # Theme selection
        theme_frame = ctk.CTkFrame(appearance_frame)
        theme_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(theme_frame, text="Color Theme:").pack(side="left", padx=5)
        self.theme_var = ctk.StringVar(value="blue")
        theme_menu = ctk.CTkOptionMenu(theme_frame, values=["blue", "green", "dark-blue"], variable=self.theme_var, command=self.change_theme)
        theme_menu.pack(side="right", padx=5)

        # Appearance mode
        mode_frame = ctk.CTkFrame(appearance_frame)
        mode_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(mode_frame, text="Appearance Mode:").pack(side="left", padx=5)
        self.mode_var = ctk.StringVar(value="system")
        mode_menu = ctk.CTkOptionMenu(mode_frame, values=["System", "Light", "Dark"], variable=self.mode_var, command=self.change_mode)
        mode_menu.pack(side="right", padx=5)

        # About section
        about_frame = ctk.CTkFrame(tab)
        about_frame.pack(pady=20, padx=10, fill="x")

        ctk.CTkLabel(about_frame, text="About", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        about_text = """
Bank Statement Engine v1.0

A cross-platform application for generating
bank statements and PDF documents.

Built with Python and CustomTkinter.
        """
        ctk.CTkLabel(about_frame, text=about_text, justify="left").pack(pady=10, padx=10)

    def save_account_info(self):
        try:
            # Collect data from form
            self.account_info.name = self.name_entry.get().strip()
            self.account_info.address_lines = [self.address_entry.get().strip()]
            self.account_info.pincode = self.pincode_entry.get().strip()
            self.account_info.email = self.email_entry.get().strip()
            self.account_info.mobile = self.mobile_entry.get().strip()
            self.account_info.cif_number = self.cif_entry.get().strip()
            self.account_info.account_number = self.account_entry.get().strip()
            self.account_info.account_type = self.account_type_entry.get().strip()
            self.account_info.account_open_date = self.account_open_date_entry.get().strip()
            self.account_info.ifsc_code = self.ifsc_entry.get().strip()
            self.account_info.micr_code = self.micr_entry.get().strip()
            self.account_info.branch_address = self.branch_entry.get().strip()
            self.account_info.nominee_name = self.nominee_entry.get().strip()
            self.account_info.ckyc_no = self.ckyc_entry.get().strip()
            self.account_info.statement_date = self.stmt_datetime_entry.get().strip()
            self.account_info.statement_from_date = self.from_date_entry.get().strip()
            self.account_info.statement_to_date = self.to_date_entry.get().strip()
            self.account_info.cleared_balance = self.balance_entry.get().strip()

            # Basic validation
            if not self.account_info.name:
                raise ValueError("Name is required")
            if not self.account_info.account_number:
                raise ValueError("Account number is required")

            messagebox.showinfo("Success", "Account information saved successfully!")
            self.status_label.configure(text="Account info saved", text_color="green")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save account info: {str(e)}")
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")

    def load_sample_data(self):
        # Load sample data for testing
        sample_data = create_sample_account_info()

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, sample_data.name)

        self.address_entry.delete(0, "end")
        self.address_entry.insert(0, " ".join(sample_data.address_lines))

        self.pincode_entry.delete(0, "end")
        self.pincode_entry.insert(0, sample_data.pincode)

        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, sample_data.email)

        self.mobile_entry.delete(0, "end")
        self.mobile_entry.insert(0, sample_data.mobile)

        self.cif_entry.delete(0, "end")
        self.cif_entry.insert(0, sample_data.cif_number)

        self.account_entry.delete(0, "end")
        self.account_entry.insert(0, sample_data.account_number)

        self.account_type_entry.delete(0, "end")
        self.account_type_entry.insert(0, sample_data.account_type)

        self.account_open_date_entry.delete(0, "end")
        self.account_open_date_entry.insert(0, sample_data.account_open_date)

        self.ifsc_entry.delete(0, "end")
        self.ifsc_entry.insert(0, sample_data.ifsc_code)

        self.micr_entry.delete(0, "end")
        self.micr_entry.insert(0, sample_data.micr_code)

        self.branch_entry.delete(0, "end")
        self.branch_entry.insert(0, sample_data.branch_address)

        self.nominee_entry.delete(0, "end")
        self.nominee_entry.insert(0, sample_data.nominee_name)

        self.ckyc_entry.delete(0, "end")
        self.ckyc_entry.insert(0, sample_data.ckyc_no)

        self.stmt_datetime_entry.delete(0, "end")
        self.stmt_datetime_entry.insert(0, f"{datetime.now().strftime('%d-%m-%Y %H:%M')}")

        self.from_date_entry.delete(0, "end")
        self.from_date_entry.insert(0, "01-08-2025")

        self.to_date_entry.delete(0, "end")
        self.to_date_entry.insert(0, "31-01-2026")

        self.balance_entry.delete(0, "end")
        self.balance_entry.insert(0, "1286456.00")

        messagebox.showinfo("Success", "Sample data loaded!")
        self.status_label.configure(text="Sample data loaded", text_color="green")

    def clear_form(self):
        # Clear all form fields
        for entry in [self.name_entry, self.address_entry, self.pincode_entry, self.email_entry,
                     self.mobile_entry, self.cif_entry, self.account_entry, self.account_type_entry,
                     self.account_open_date_entry, self.ifsc_entry, self.micr_entry, self.branch_entry, self.nominee_entry,
                     self.ckyc_entry, self.stmt_datetime_entry, self.from_date_entry,
                     self.to_date_entry, self.balance_entry]:
            entry.delete(0, "end")

        self.status_label.configure(text="Form cleared", text_color="blue")

    def generate_pdf(self):
        try:
            stmt_type = self.stmt_type_var.get()
            selected_bank = self.bank_var.get()

            if stmt_type == "basic":
                # Generate basic account info PDF
                if not self.account_info.name:
                    raise ValueError("Please save account information first")

                data = {
                    "name": self.account_info.name,
                    "address": " ".join(self.account_info.address_lines),
                    "pin": self.account_info.pincode,
                    "email": self.account_info.email,
                    "phone": self.account_info.mobile,
                    "cif": self.account_info.cif_number,
                    "acc_number": self.account_info.account_number,
                    "acc_type": self.account_info.account_type,
                    "acc_open_date": getattr(self.account_info, 'account_open_date', ''),
                    "ifsc": self.account_info.ifsc_code,
                    "micr": self.account_info.micr_code,
                    "branch_address": self.account_info.branch_address,
                    "nominee": self.account_info.nominee_name,
                    "ckyc": self.account_info.ckyc_no,
                    "statement_datetime": self.account_info.statement_date,
                    "statement_from": self.account_info.statement_from_date,
                    "statement_to": getattr(self.account_info, 'statement_to_date', ''),
                    "balance": str(self.account_info.cleared_balance),
                }

                generate_basic_pdf(data, selected_bank)
                messagebox.showinfo("Success", f"Basic account info PDF generated successfully for {selected_bank.upper()}!")

            elif stmt_type == "full":
                # Generate full statement with transactions
                output_file = generate_statement_pdf(self.account_info, selected_bank)
                messagebox.showinfo("Success", f"Full statement PDF generated successfully for {selected_bank.upper()}!\nSaved to: {output_file}")

            self.status_label.configure(text="PDF generated successfully", text_color="green")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")

    def change_theme(self, theme):
        ctk.set_default_color_theme(theme)

    def change_mode(self, mode):
        ctk.set_appearance_mode(mode)


def main():
    app = BankStatementGUI()
    app.mainloop()


if __name__ == "__main__":
    main()