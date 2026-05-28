#!/usr/bin/env python3
"""PDF export functionality for cleaning service reports"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.platypus.tableofcontents import TableOfContents
from datetime import datetime
import os
from typing import List, Tuple, Optional


def generate_pdf_report(
    customer_names: List[str],
    customer_addresses: List[str],
    customer_discounts: List[float],
    customer_totals: List[float],
    filename: str = None,
) -> Optional[str]:
    """Generate a PDF report of daily transactions"""

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cleaning_report_{timestamp}.pdf"

    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []

    # Get styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center
        textColor=colors.darkblue,
    )

    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Heading2"],
        fontSize=16,
        spaceAfter=20,
        alignment=1,  # Center
        textColor=colors.darkgreen,
    )

    # Title
    story.append(Paragraph("In & Out Cleaners - Report", title_style))
    story.append(Spacer(1, 20))

    # Report info
    report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    story.append(Paragraph(f"Generated on: {report_date}", styles["Normal"]))
    story.append(Spacer(1, 20))

    # Summary section
    if customer_names:
        total_customers = len(customer_names)
        total_revenue = sum(customer_totals)
        total_discounts = sum(customer_discounts)

        story.append(Paragraph("Summary", subtitle_style))

        summary_data = [
            ["Metric", "Value"],
            ["Total Customers", str(total_customers)],
            ["Total Revenue", f"${total_revenue:,.2f}"],
            ["Total Discounts Given", f"${total_discounts:,.2f}"],
            ["Net Revenue", f"${total_revenue - total_discounts:,.2f}"],
        ]

        summary_table = Table(summary_data, colWidths=[2 * inch, 2 * inch])
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        story.append(summary_table)
        story.append(Spacer(1, 20))

        # Customer details section
        story.append(Paragraph("Customer Transactions", subtitle_style))
        story.append(Spacer(1, 12))

        # Customer data table
        customer_data = [["Customer Name", "Address", "Discount", "Total"]]

        for i, name in enumerate(customer_names):
            address = customer_addresses[i] if i < len(customer_addresses) else "N/A"
            discount = customer_discounts[i] if i < len(customer_discounts) else 0.0
            total = customer_totals[i] if i < len(customer_totals) else 0.0

            customer_data.append([name, address, f"${discount:.2f}", f"${total:.2f}"])

        # Create customer table
        customer_table = Table(
            customer_data, colWidths=[2 * inch, 2.5 * inch, 1 * inch, 1 * inch]
        )
        customer_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTSIZE", (0, 1), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )

        # Alternate row colors for better readability
        for i in range(1, len(customer_data)):
            if i % 2 == 0:
                bg_color = colors.lightgrey
            else:
                bg_color = colors.beige
            customer_table.setStyle(
                TableStyle([("BACKGROUND", (0, i), (-1, i), bg_color)])
            )

        story.append(customer_table)
    else:
        story.append(
            Paragraph("No customer transactions to display.", styles["Normal"])
        )

    # Footer
    story.append(Spacer(1, 30))
    story.append(
        Paragraph("Thank you for choosing our cleaning services!", styles["Normal"])
    )
    story.append(
        Paragraph("Professional Cleaning Service Management System", styles["Normal"])
    )

    # Build PDF
    try:
        doc.build(story)
        print(f"PDF report saved as: {filename}")
        print(f"File location: {os.path.abspath(filename)}")
        return filename
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None


def ask_pdf_export() -> bool:
    """Ask user if they want to export to PDF"""
    try:
        choice = (
            input(
                "\nWould you like to save a PDF report of today's transactions? (y/n): "
            )
            .strip()
            .lower()
        )
        return choice in ["y", "yes", "Y", "YES"]
    except (EOFError, KeyboardInterrupt):
        return False


def export_daily_report_pdf(
    customer_names: List[str],
    customer_addresses: List[str],
    customer_discounts: List[float],
    customer_totals: List[float],
) -> bool:
    """Export daily report to PDF with user confirmation"""

    if ask_pdf_export():
        try:
            filename = generate_pdf_report(
                customer_names, customer_addresses, customer_discounts, customer_totals
            )

            if filename:
                print(f"\n[SUCCESS] PDF report successfully created!")
                print(f"[FILE] {filename}")
                return True
            else:
                print("[ERROR] Failed to create PDF report.")
                return False

        except Exception as e:
            print(f"[ERROR] Error creating PDF: {e}")
            return False
    else:
        print("PDF export skipped.")
        return False


def get_all_customers():
    """Get all customers from database"""
    try:
        import sqlite3
        from db.db_functions import DB

        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers ORDER BY id")
        customers = cursor.fetchall()
        conn.close()
        return customers
    except Exception as e:
        print(f"Error retrieving customers: {e}")
        return []


def export_database_to_pdf() -> None:
    """Export all database data to PDF"""
    try:
        from db.db_functions import provision_database

        # Ensure database exists
        provision_database()

        # Get all customer data
        customers = get_all_customers()

        if not customers:
            print("No customer data found in database to export.")
            return

        # Extract data for PDF
        customer_names = [str(cust[1]) for cust in customers]  # name
        customer_addresses = [str(cust[2]) for cust in customers]  # address
        customer_discounts = [
            float(cust[4]) if cust[4] else 0.0 for cust in customers
        ]  # discount
        customer_totals = [
            float(cust[3]) if cust[3] else 0.0 for cust in customers
        ]  # amount_paid

        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"database_export_{timestamp}.pdf"

        # Generate PDF
        result = generate_pdf_report(
            customer_names,
            customer_addresses,
            customer_discounts,
            customer_totals,
            filename,
        )

        if result:
            print(f"\n[SUCCESS] Database successfully exported to PDF!")
            print(f"[FILE] {result}")
            print(f"[INFO] Total records exported: {len(customers)}")
        else:
            print("[ERROR] Failed to export database to PDF.")

    except ImportError as e:
        print(f"[ERROR] Database module not available: {e}")
    except Exception as e:
        print(f"[ERROR] Error exporting database to PDF: {e}")
