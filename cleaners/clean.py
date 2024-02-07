#!/usr/bin/env python3

import os
import sqlite3
import sys
from datetime import datetime
from sqlite3 import Error
from time import sleep, time

from cleaners.fig import io_figlets
from db.db_functions import *

total_services = {
    "Regular": "General-Tidying, Sweep, Dust, Mop $100.00",
    "Premium": "Regular Service+, Bathrooms, Closets, Laundry $200.00",
    "Outdoor": "Mowing, Weed-Wack, Shrubs, Leaves $300.00",
}


def get_employees():
    "get employees"
    employee_list = []

    print("\nManager:")
    name = "Mike Chambers"
    date = datetime.now().strftime("%A, %d, %B %Y %I:%M%p")
    my_class = "North East"
    bage_id = "MC98342"
    employee = name, date, my_class, bage_id

    for i in name, date, my_class, bage_id:
        print(i)

    print("")
    employee_list.append(employee)
    return employee_list


p = lambda p: print(p)


def new_customer():
    """get customers"""
    valid_name = False
    discount = int
    addr = ""
    age = ""

    name = input("Name: Press <Enter> to exit: \t")
    if not name.strip():
        sys.exit("come again soon'")

    if name.isdigit() and name.isalpha():
        print("error, letters only")
        name = input("Name: \t")

    age = input("Age: \t")
    if age.isalpha() is True:
        print("error, numbers only")
        age = input("Age: \t")

    if int(64) < int(age) < int(120):
        discount = int(1), True
        print("applying discounts...!")
        sleep(0.5)
        cash = text_colors("green")
        print(cash("-15%"), "discount applied!")

    else:
        discount = int(0), False

    address = input("Enter address: \t")
    addr = address.replace(" ", "") and addr.upper()
    name = name.replace(" ", "") and name.upper()
    valid_name = True
    print(f"Welcome, {name}", "\n")
    return valid_name, name, addr, discount


def banner():
    """ui"""
    b = "=" * 78
    print(b)


def text_colors(color):
    """ui"""
    colors = {"RESET": "\033[m", "RED": "\033[31m", "GREEN": "\033[32m"}

    def text(text):
        c = colors.get(color.upper(), "")
        return f"{c}{text}{colors['RESET']}"

    return text


def user_interface():
    """ui"""

    io_figlets()

    cash = text_colors("green")
    for display1 in [
        ["Regular:", "Premium:", "Outdoor:"],
        ["Room Clean", "Regular +", "Mow"],
    ]:
        print("\n{:>20}{:>20}{:>20}".format(*display1))

    for display2 in [
        ["Dust", "Bathrooms", "Weed-Wack"],
        ["Sweep", "Closets", "Shrubs"],
    ]:
        print("{:>20}{:>20}{:>20}".format(*display2))

    for display3 in ["Mop", "Laundry", "Leaves"], [
        cash("\t\t$100"),
        cash("\t  $200"),
        cash("\t\t$300"),
    ]:
        print("{:>20}{:>20}{:>20}".format(*display3))

    print("")
    d = "Age 65+ 15% Discount"
    d_banner = d.center(70)
    print(d_banner)
    banner()
    banner()
    package = "Cleaning packages..."
    package_banner = package.center(53)

    print(f"\t{package_banner}\n ")
    print(
        "\n1.Regular Package ---> $100.00",
        "\n",
        total_services["Regular"],
    )
    print(
        "\n2.Premium Package ---> $200.00",
        "\n",
        total_services["Premium"],
    )
    print(
        "\n3.Outdoor Package ---> $300.00",
        "\n",
        total_services["Outdoor"],
    )
    print("")
    print("$.15 per square foot of house is charged for labor\n")
    print("Chose cleaning package...")
    sleep(0.4)


def cust_selection():
    """customer selections"""

    service_selection = int(
        input(
            """
    Press ---[1]---> Regular\n 
    Press ---[2]---> Premium\n
    Press ---[3]---> Outdoor\n
    """
        )
    )

    if service_selection == 1:
        reg_selection = service_selection
        return reg_selection

    if service_selection == 2:
        return service_selection

    if service_selection == 3:
        return service_selection

    else:
        if service_selection != 1 or service_selection != 2 or service_selection != 3:
            print("Error")
            print("Enter 1 2 or 3")
            return cust_selection()
    p(f"selection is {service_selection}")
    return service_selection
    # print("Error, letter selections not allowed")
    # print("Enter 1 2 or 3")


def customer_transaction(selection, discount):
    "1 2 or 3"

    LIST_PRICE = [100.00, 200.00, 300.00]
    totals = []

    if selection == int(1):
        print(f"Customer selects:\n{total_services['Regular']}\n")
        sleep(0.5)
        print("Measure Length and width of exterior for price")

        l = float(input("Length: \t"))
        w = float(input("Width: \t"))
        area = l * w
        labor = labor_charge(area)
        s = LIST_PRICE[0]
        r_total_before_discount = price_per_house(s, labor)
        totals.append(r_total_before_discount)

    elif selection == int(2):
        print(f"Customer selects:\n {total_services['Premium']}")
        print("Measure Length and width of exterior for price")
        l = float(input("Length: \t"))
        w = float(input("Width: \t"))
        premium_area = l * w
        labor2 = (lambda area: (area) * 0.15)(premium_area)
        print("area for pre = ", premium_area)
        s2 = LIST_PRICE[1]
        p_total_before_discount = price_per_house(s2, labor2)
        totals.append(p_total_before_discount)

    elif selection == int(3):
        print(f"Customer selects:\n {total_services['Outdoor']}")
        print("Measure Length and width of exterior for price")
        l = int(input("Length: \t"))
        w = int(input("Width: \t"))
        outdoor_area = l * w
        outdoor_labor = labor_charge(outdoor_area)
        s3 = LIST_PRICE[2]
        r_total_before_discount = price_per_house(s3, outdoor_labor)
        totals.append(r_total_before_discount)

    return totals


def price_per_house(selection, labor):
    p("price_per_house function line 254 ")
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
    dis = total[0] * 15 / 100
    print("getting discount...")
    return dis


def labor_charge(area):
    """calculate labor"""
    labor = area * 0.15
    cash = text_colors("green")
    print(cash("labor: "), labor)
    return labor


def final_price(reg_price=0, discount=0):
    """get final price"""
    final_discount_price = reg_price - discount
    return final_discount_price
