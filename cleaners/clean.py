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
    "Regular": "General-Tidying, Sweep, Dust, Mop",
    "Premium": "Regular Service+, Bathrooms, Closets, Laundry",
    "Outdoor": "Mowing, Weed-Wack, Shrubs, Leaves",
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

import re
from time import sleep

import re
from time import sleep

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
                print("Error, numbers only".center(_txt_))
                sleep(0.5)

        if 64 < age < 999:
            discount = (1, True)
            print("applying discounts...!".center(_txt_))
            sleep(0.5)
            cash = text_colors("green")
            print(cash("-15%".center(_txt_)), "discount applied!".center(_txt_))
        else:
            discount = (0, False)
        address = centered_input("Enter address: ").strip()
        addr = address.capitalize()
    
    return name, valid_name, discount, addr


def user_interface():
    """ui"""

    def center_text(text, total_width=80):
        text_width = len(text)
        padding = (total_width - text_width) // 2
        return " " * padding + text

    cash = text_colors("green")

    for display1 in [
        # TODO find new technique for centering
        ["Regular:", "Premium:", "Outdoor:"],
        ["Room Clean", "Regular +", "Mow"],
    ]:
        print(center_text("{:>20}{:>20}{:>20}".format(*display1)))

    for display2 in [
        ["Dust", "Bathrooms", "Weed-Wack"],
        ["Sweep", "Closets", "Shrubs"],
    ]:
        print(center_text("{:>20}{:>20}{:>20}".format(*display2)))

    for display3 in ["Mop", "Laundry", "Leaves"], [
        cash("\t\t$100"),
        cash("\t  $200"),
        cash("\t\t$300"),
    ]:
        print(center_text("{:>20}{:>20}{:>20}".format(*display3)))

    print("")
    d = "Age 65+ 15% Discount"
    d_banner = d.center(70)
    print(d_banner)
    banner()
    banner()
    package = "Cleaning packages...".center(_txt_)
    package_banner = package.center(_txt_)
    print(f"{package_banner}".center(_txt_))
    print(
        "\n1.Regular Package ---> $100.00".center(_txt_),
        "\n",
        total_services["Regular"],
    )
    print(
        "\n2.Premium Package ---> $200.00".center(_txt_),
        "\n",
        total_services["Premium"],
    )
    print(
        "\n3.Outdoor Package ---> $300.00".center(_txt_),
        "\n",
        total_services["Outdoor"],
    )
    print("")
    print("$.15 per square foot of house is charged for labor\n")
    print("Chose cleaning package...")


def cust_selection():
    """customer selections"""

    service_selection = int(
        input(
            """
    Press ---[1]---> Regular
    Press ---[2]---> Premium
    Press ---[3]---> Outdoor
    """
        ).center(shutil.get_terminal_size().columns)
        # TODO can't center int
    )
    if service_selection == 1:
        return service_selection
    
    if service_selection == 2:
        return service_selection
    
    if service_selection == 3:
        return service_selection
    else:
        if service_selection != 1 or service_selection != 2 or service_selection != 3:
            print("Error")
            print("Enter 1 2 or 3")
            return cust_selection()


def customer_transaction(selection, discount):
    """sum of area and labor charge added to price from LIST_PRICE"""

    LIST_PRICE = [100.00, 200.00, 300.00]
    totals = []
    cash = text_colors("green")
    l = ""
    w = ""

    if selection == int(1):
        print(f"Customer selects:\n{total_services['Regular']}", cash("$100.00"), "\n")
        sleep(0.5)
        print("Measure Length and width of exterior for price")
        l = float(input("Length: \t"))
        w = float(input("Width: \t"))
        area = l * w
        labor = (lambda area: (area) * 0.15)(area)
        print("Area: \t", area)
        s = LIST_PRICE[0]
        r_total_before_discount = price_per_house(s, labor)
        totals.append(r_total_before_discount)
    
    elif selection == int(2):
        print(f"Customer selects:\n {total_services['Premium']}", cash("$200.00"), "\n")
        print("Measure Length and width of exterior for price")
        l = float(input("Length: \t"))
        w = float(input("Width: \t"))
        premium_area = l * w
        labor2 = (lambda area: (area) * 0.15)(premium_area)
        print("Area: \t", premium_area)
        s2 = LIST_PRICE[1]
        p_total_before_discount = price_per_house(s2, labor2)
        totals.append(p_total_before_discount)
    
    elif selection == int(3):
        print(f"Customer selects:\n {total_services['Outdoor']}", cash("$300.00"), "\n")
        print("Measure Length and width of exterior for price")
        l = float(input("Length: \t"))
        w = float(input("Width: \t"))
        outdoor_area = l * w
        outdoor_labor = (lambda area: (area) * 0.15)(outdoor_area)
        print("Area: \t", outdoor_area)
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
        print("{:.2f}".format(float(reg_before_discount)))
        cash(reg_before_discount)
        return reg_before_discount

    elif selection == LIST_PRICE[1]:
        total = selection + labor
        prem_before_discount = total
        print("{:.2f}".format(float(prem_before_discount)))
        cash(prem_before_discount)
        return prem_before_discount

    elif selection == LIST_PRICE[2]:
        total = selection + labor
        out_before_discount = total
        print("{:.2f}".format(float(out_before_discount)))
        cash(out_before_discount)
        return out_before_discount


def get_discount(total):
    """calculate discount"""

    dis = total * (15 / 100)
    print("getting discount...")
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
        "_______________", "___________", "_________", "__________"
    ).center(_txt_)
    center_daily_info(separators)

    i = 0
    len_cust = len(c_names)
    while i < len_cust:
        display_data = "{:<20}\t{:<20}\t{:<20}\t{:<20}".format(
            c_names[i], c_address[i], str(c_discounts[i]), round(c_totals[i], 2) # use "%.2f" % to format
        )
        center_daily_info(display_data)
        i += 1
    i = 0

    todays_ctotal = sum(c_totals)
    t = "${:.2f}".format(todays_ctotal)
    print("\n\n\n")
    for total_cash in ["Cash Earned", "____________", t]:
        center_cash_earned(total_cash)
    print("\n\n")
