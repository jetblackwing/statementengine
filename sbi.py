import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

def get_input(prompt):
    return input(f"{prompt}: ")

def find_header_image():
    if os.path.exists("sbi.png"):
        return "sbi.png"
    elif os.path.exists("sbi.jpg"):
        return "sbi.jpg"
    else:
        return None

def generate_pdf(data):
    pdf = SimpleDocTemplate("bank_statement.pdf", pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    # Add Header Image
    image_path = find_header_image()
    if image_path:
        img = Image(image_path)
        img.drawHeight = 1.2 * inch
        img.drawWidth = 4 * inch
        elements.append(img)
        elements.append(Spacer(1, 0.3 * inch))
    else:
        print("Warning: No sbi.png or sbi.jpg found in directory.")

    # Create table data
    table_data = [
        ["Name", data["name"], "CIF Number", data["cif"]],
        ["Address", data["address"], "Account Number", data["acc_number"]],
        ["Pin Code", data["pin"], "Account Type", data["acc_type"]],
        ["Email", data["email"], "Account Open Date", data["acc_open_date"]],
        ["Phone Number", data["phone"], "IFSC Code", data["ifsc"]],
        ["MICR Code", data["micr"], "Branch Address", data["branch_address"]],
        ["Nominee Name", data["nominee"], "CKYC Number", data["ckyc"]],
        ["Statement Date & Time", data["statement_datetime"], "", ""],
        ["Statement From", data["statement_from"], "Statement To", data["statement_to"]],
        ["Cleared Balance", data["balance"], "", ""],
    ]

    table = Table(table_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    elements.append(table)

    pdf.build(elements)
    print("\nPDF Generated Successfully: bank_statement.pdf")

def main():
    print("Enter Bank Statement Details\n")

    data = {
        "name": get_input("Full Name"),
        "address": get_input("Address"),
        "pin": get_input("Pin Code"),
        "email": get_input("Email"),
        "phone": get_input("Phone Number"),
        "cif": get_input("CIF Number"),
        "acc_number": get_input("Account Number"),
        "acc_type": get_input("Account Type"),
        "acc_open_date": get_input("Account Open Date"),
        "ifsc": get_input("IFSC Code"),
        "micr": get_input("MICR Code"),
        "branch_address": get_input("Branch Address"),
        "nominee": get_input("Nominee Name"),
        "ckyc": get_input("CKYC Number"),
        "statement_datetime": get_input("Statement Date & Time"),
        "statement_from": get_input("Statement From Date"),
        "statement_to": get_input("Statement To Date"),
        "balance": get_input("Cleared Balance"),
    }

    generate_pdf(data)

if __name__ == "__main__":
    main()
