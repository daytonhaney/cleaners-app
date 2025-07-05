#!/usr/bin/env python3
"""Cleaning Service console app"""

import os
import re
import shutil
from datetime import datetime
from time import sleep

from cleaners.fig import (
    _txt_,
    center_cash_earned,
    center_daily_info,
    centered_input,
    centered_text,
)
from db.db_functions import DB, e_table_exists, emp_table, insert_employee

total_services = {
    "Regular": "General-Tidying, Sweep, Dust, Mop, $100",
    "Premium": "Regular Service+, Bathrooms, Closets, Laundry, $200",
    "Outdoor": "Mowing, Weed-Wack, Shrubs, Leaves, $300",
}


def get_employees():
    """get employees"""

    employee_list = []
    mod = "Manager:"
    name = "Cam Poe"
    date = datetime.now().strftime("%A, %d, %B %Y %I:%M%p")
    address = "12 Pinball Road"
    region = "Sierra Nevada"
    badge_id = "JB3HBIRD"
    employee = (
        name,
        date,
        region,
        badge_id,
    )
    for i in mod, name, date, address, region, badge_id:
        centered_text(i)
    print("")
    
    if os.path.isfile(DB):
        if e_table_exists(DB, emp_table):
            insert_employee(name, address, region, badge_id)
    
    elif not os.path.isfile(DB):
        pass
    employee_list.append(employee)
    
    return employee_list


def new_customer():
    """get customers"""

    discount = (0, False)
    addr = ""
    valid_name = False

    name = centered_input("Customer Name <Enter> to exit: ").strip()
    fname = name.replace(" ", "")

    if fname.isalpha():
        name = name.title()
        valid_name = True

        while True:
            age_input = centered_input("Enter age: ").strip()
            if age_input.isdigit():
                age = int(age_input)
                break
            else:
                centered_text("Error, numbers only")
                sleep(0.5)

        if 64 < age < 999:
            discount = (1, True)
            centered_text("applying discounts...!")
            sleep(0.5)
            cash = text_colors("green")
            centered_text(cash("-15% discount applied!"))
        else:
            discount = (0, False)
        address = centered_input("Enter address: ").strip()
        addr = address.capitalize()
        print() # Add space for readability

    return name, valid_name, discount, addr



def user_interface():
    """ui"""

    cash = text_colors("green")
    
    # --- Table Configuration ---
    col_width = 20
    headers = ["Regular:", "Premium:", "Outdoor:"]
    
    # Extract details from the updated total_services dictionary
    details = {k: [item.strip() for item in v.split(',')] for k, v in total_services.items()}
    max_rows = max(len(v) for v in details.values())

    # --- Build and Print Table ---
    # Print Headers
    header_line = "".join(h.ljust(col_width) for h in headers)
    centered_text(header_line)

    # Print Details and Prices
    for i in range(max_rows):
        row_list = []
        for header in headers:
            package_name = header.replace(':', '')
            # Get the item, or an empty string if this package has fewer details
            item = details[package_name][i] if i < len(details[package_name]) else ""
            
            # Check if the item is a price
            if item.startswith('$'):
                # Color the price and pad correctly
                padding = ' ' * (col_width - len(item))
                row_list.append(cash(item) + padding)
            else:
                # Just pad the detail text
                row_list.append(item.ljust(col_width))
        
        centered_text("".join(row_list))
    
    print()
    centered_text("Age 65+ 15% Discount")
    banner()
    banner()
    centered_text("Cleaning packages...")
    
    # This part of the UI can now also be generated dynamically if desired,
    # but is left as is to maintain the existing detailed view.
    print(
        "\n1.Regular Package ---> $100.00".center(_txt_),
        "\n",
        total_services["Regular"].replace(", $100", ""),
    )
    print(
        "\n2.Premium Package ---> $200.00".center(_txt_),
        "\n",
        total_services["Premium"].replace(", $200", ""),
    )
    print(
        "\n3.Outdoor Package ---> $300.00".center(_txt_),
        "\n",
        total_services["Outdoor"].replace(", $300", ""),
    )
    print("")
    print("$.15 per square foot of house is charged for labor\n")
    print("Chose cleaning package...")


def cust_selection():
    """customer selections"""

    red = text_colors("red")
    prompt = """
    Press ---[1]---> Regular
    Press ---[2]---> Premium
    Press ---[3]---> Outdoor
    """
    while True:
        try:
            service_selection = int(input(prompt))
            if service_selection in [1, 2, 3]:
                return service_selection
            else:
                print(red("\nError: Please enter 1, 2, or 3.\n"))
        except ValueError:
            print(red("\nError: Invalid input. Please enter a number.\n"))



def customer_transaction(selection, discount):
    """sum of area and labor charge added to price from LIST_PRICE"""

    LIST_PRICE = [100.00, 200.00, 300.00]
    package_names = list(total_services.keys())
    totals = []
    cash = text_colors("green")
    l = ""
    w = ""

    if selection == int(1):
        package_name = package_names[0]
        print(f"Customer selects: {package_name}\n{total_services[package_name]}", cash("$100.00"), "\n")
        sleep(0.5)
        print("Measure Length and width of exterior for price")
        l = float(input("Length: ".ljust(8)))
        w = float(input("Width:  ".ljust(8)))
        area = l * w
        labor = (lambda area: (area) * 0.15)(area)
        print(f"Area:    {area:.2f}")
        print() # Add space for readability
        s = LIST_PRICE[0]
        r_total_before_discount = price_per_house(s, labor)
        totals.append(r_total_before_discount)
    
    elif selection == int(2):
        package_name = package_names[1]
        print(f"Customer selects: {package_name}\n{total_services[package_name]}", cash("$200.00"), "\n")
        print("Measure Length and width of exterior for price")
        l = float(input("Length: ".ljust(8)))
        w = float(input("Width:  ".ljust(8)))
        premium_area = l * w
        labor2 = (lambda area: (area) * 0.15)(premium_area)
        print(f"Area:    {premium_area:.2f}")
        s2 = LIST_PRICE[1]
        p_total_before_discount = price_per_house(s2, labor2)
        totals.append(p_total_before_discount)
    
    elif selection == int(3):
        package_name = package_names[2]
        print(f"Customer selects: {package_name}\n{total_services[package_name]}", cash("$300.00"), "\n")
        print("Measure Length and width of exterior for price")
        l = float(input("Length: ".ljust(8)))
        w = float(input("Width:  ".ljust(8)))
        outdoor_area = l * w
        outdoor_labor = (lambda area: (area) * 0.15)(outdoor_area)
        print(f"Area:    {outdoor_area:.2f}")
        s3 = LIST_PRICE[2]
        o_total_before_discount = price_per_house(s3, outdoor_labor)
        totals.append(o_total_before_discount)
    
    return totals



def price_per_house(selection, labor):
    """sets vars to use in customer_transaction"""

    LIST_PRICE = [100.00, 200.00, 300.00]
    cash = text_colors("green")

    if selection == LIST_PRICE[0]:
        total = selection + labor
        reg_before_discount = total
        print(f"Subtotal: {reg_before_discount:.2f}")
        cash(reg_before_discount)
        return reg_before_discount

    elif selection == LIST_PRICE[1]:
        total = selection + labor
        prem_before_discount = total
        print(f"Subtotal: {prem_before_discount:.2f}")
        cash(prem_before_discount)
        return prem_before_discount

    elif selection == LIST_PRICE[2]:
        total = selection + labor
        out_before_discount = total
        print(f"Subtotal: {out_before_discount:.2f}")
        cash(out_before_discount)
        return out_before_discount


def get_discount(total):
    """calculate discount"""

    cash = text_colors("green")
    dis = total * (15 / 100)
    print(cash("getting discount..."))
    return dis


def labor_charge(area):
    """calculate labor"""

    labor = area * (15 / 100)
    cash = text_colors("green")
    print(cash("labor: "), labor)
    return labor


def final_price(reg_price=0, discount=0):
    """get final price"""

    final_discount_price = reg_price - discount
    return final_discount_price


def banner():
    """ui"""

    b = "="
    print(b.center(shutil.get_terminal_size().columns))


def text_colors(color):
    """ui"""

    colors = {"RESET": "\033[m", "RED": "\033[31m", "GREEN": "\033[32m"}

    def text(text):
        c = colors.get(color.upper(), "")
        return f"{c}{text}{colors['RESET']}"

    return text


def display_customer_info(c_names, c_address, c_discounts, c_totals):
    """print formatted daily info + cash total"""

    print("\n\n\n\n\n")
    header = "{:<15}{:>51}".format("*** Todays Customer Info...", "Store ID: 3214")
    center_daily_info(header)
    print("\n\n")
    header_titles = "{:<20}\t{:<20}\t{:<20}\t{:<20}".format(
        "Customer Name", "Address", "Discount", "Total"
    )
    center_daily_info(header_titles)
    separators = "{:<20}\t{:<20}\t{:<20}\t{:<20}".format(
        "_______________", "___________", "__________", "__________"
    ).center(_txt_)
    center_daily_info(separators)

    i = 0
    len_cust = len(c_names)
    while i < len_cust:
        display_data = "{:<20}\t{:<20}\t{:<20}\t${:<20.2f}".format(
            c_names[i], c_address[i], str(c_discounts[i]), c_totals[i]
        )
        center_daily_info(display_data)
        i += 1
    i = 0

    todays_ctotal = sum(c_totals)
    t = "${:.2f}".format(todays_ctotal)
    print("\n\n\n")
    for total_cash in ["Cash Earned", "__________", t]:
        center_cash_earned(total_cash)
    print("\n\n")