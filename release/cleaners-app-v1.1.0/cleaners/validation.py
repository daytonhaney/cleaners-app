#!/usr/bin/env python3
"""Input validation utilities for CleanersApp"""

import re, os


def validate_customer_name(name):
    """Validate customer name"""
    if not name or not name.strip():
        return False, "Customer name cannot be empty"

    name = name.strip()
    min_length = 2
    max_length = 50

    if len(name) < min_length:
        return False, f"Name must be at least {min_length} characters"

    if len(name) > max_length:
        return False, f"Name cannot exceed {max_length} characters"

    # Check for valid characters (letters, spaces, hyphens, apostrophes)
    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"

    return True, name.title()


def validate_address(address):
    """Validate customer address"""
    if not address or not address.strip():
        return False, "Address cannot be empty"

    address = address.strip()
    max_length = 100

    if len(address) > max_length:
        return False, f"Address cannot exceed {max_length} characters"

    return True, address


def validate_age(age):
    """Validate customer age"""
    try:
        age_int = int(age)
        if age_int < 1 or age_int > 120:
            return False, "Please enter a valid age between 1 and 120"
        return True, age_int
    except ValueError:
        return False, "Age must be a valid number"


def validate_square_footage(area):
    """Validate square footage input"""
    try:
        min_sqft = 100
        max_sqft = 10000

        area_float = float(area)
        if area_float < min_sqft:
            return False, f"Area must be at least {min_sqft} square feet"

        if area_float > max_sqft:
            return False, f"Area cannot exceed {max_sqft} square feet"

        return True, area_float
    except ValueError:
        return False, "Area must be a valid number"


def validate_package_selection(selection):
    """Validate package selection"""
    try:
        selection_int = int(selection)
        if selection_int in [1, 2, 3]:
            return True, selection_int
        return False, "Please select 1 (Regular), 2 (Premium), or 3 (Outdoor)"
    except ValueError:
        return False, "Please enter a valid number (1, 2, or 3)"


def validate_payment_amount(amount):
    """Validate payment amount"""
    try:
        amount_float = float(amount)
        if amount_float < 0:
            return False, "Payment amount cannot be negative"
        return True, amount_float
    except ValueError:
        return False, "Payment amount must be a valid number"


def sanitize_string(text):
    """Sanitize text input to prevent issues"""
    if not text:
        return ""

    # Remove potentially problematic characters
    sanitized = re.sub(r'[<>"\';\\]', "", text)
    return sanitized.strip()


def validate_email(email):
    """Validate email format (basic validation)"""
    if not email:
        return False, "Email cannot be empty"

    email = email.strip().lower()
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(pattern, email):
        return False, "Please enter a valid email address"

    return True, email


def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return False, "Phone number cannot be empty"

    # Remove all non-digit characters
    digits_only = re.sub(r"\D", "", phone)

    if len(digits_only) < 10:
        return False, "Phone number must have at least 10 digits"

    if len(digits_only) > 15:
        return False, "Phone number cannot exceed 15 digits"

    return True, digits_only


def get_validation_summary():
    """Get validation limits for display"""
    return {
        "name": "2-50 characters",
        "address": "Max 100 characters",
        "square_footage": "100-10000 sq ft",
        "age": "1-120 years",
    }
