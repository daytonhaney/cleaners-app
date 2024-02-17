#!/usr/bin/env python3

import re
from datetime import datetime
from sqlite3 import Error
from time import sleep, time

from cleaners.fig import io_figlets
from db.db_functions import *

total_services = {
    "Regular": "General-Tidying, Sweep, Dust, Mop",
    "Premium": "Regular Service+, Bathrooms, Closets, Laundry",
    "Outdoor": "Mowing, Weed-Wack, Shrubs, Leaves",
}


def get_employees():
    """get employees"""

    employee_list = []

    print("\nManager:")
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

    # insert_employee(name, address, region, badge_id)
    for i in name, date, address, region, badge_id:
        print(i)
    print("")

    # create table if not exists to avoid duplicates on restart

    table = e_table_exists(DB, "employees")
    if table is True:
        new_employee_table = employee_table(DB, emp_table)
        insert_employee(name, address, region, badge_id)

    employee_list.append(employee)
    return employee_list


p = lambda p: print(p)  # p("debug")


def new_customer():
    """get customers"""

    discount = int
    addr = ""
    age = ""
    valid_name = False

    name = input("Name: <Enter> to exit  \t")
    fname = name.replace(" ", "")

    if fname.isalpha():
        name = name.title()
        valid_name = True

        age = input("Age: \t")
        if age.isalpha() is True:
            print("Error, numbers only")
            age = input("Age: \t")
            age = age.replace(" ", "")
            # added incase input chars in age
            age1 = re.findall(r"\b\d+\b", age)
            age = age1[0]

        if int(64) < int(age) < int(999):
            discount = int(1), True
            print("applying discounts...!")
            sleep(0.5)
            cash = text_colors("green")
            print(cash("-15%"), "discount applied!")

        else:
            discount = int(0), False

        address = input("Enter address: \t")
        addr = address.capitalize()
    return name, valid_name, discount, addr


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
    "1 2 or 3"

    LIST_PRICE = [100.00, 200.00, 300.00]
    totals = []
    cash = text_colors("green")

    if selection == int(1):
        print(f"Customer selects:\n{total_services['Regular']}", cash("$100.00"), "\n")
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
        print(f"Customer selects:\n {total_services['Premium']}", cash("$200.00"), "\n")
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
        print(f"Customer selects:\n {total_services['Outdoor']}", cash("$300.00"), "\n")
        print("Measure Length and width of exterior for price")
        l = int(input("Length: \t"))
        w = int(input("Width: \t"))
        outdoor_area = l * w
        outdoor_labor = labor_charge(outdoor_area)
        s3 = LIST_PRICE[2]
        o_total_before_discount = price_per_house(s3, outdoor_labor)
        totals.append(o_total_before_discount)
    return totals


def price_per_house(selection, labor):
    """price per house"""
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


def display_customer_info(c_names, c_address, c_discounts, c_totals):
    """print daily info + cash flow"""
    p("\n")
    len_cust = len(c_names)

    i = 0
    p("{:<15}{:>51}".format("*** Todays Customer Info...", "Store ID: 3214"))
    print("\n")

    print(
        "{:<20}\t{:<20}\t{:<20}\t{:<10}".format(
            "Name",
            "Address",
            "Discount",
            "Total Cost",
        )
    )
    print(
        "{:<20}\t{:<20}\t{:<20}\t{:<20}".format(
            "_______________",
            "_______________",
            "_____________",
            "_____________",
        )
    )
    while i < len_cust:

        print(
            "{:<20}\t{:<20}\t{:<20}\t{:<20}".format(
                c_names[i],
                c_address[i],
                str(c_discounts[i]),
                str(c_totals[i]),
            )
        )

        print("")
        i = i + 1
    i = 0
    # c_totals is a nested list s and thus needs to be flattened before taking sum
    todays_total = sum(subtotals for sublists in c_totals for subtotals in sublists)

    print("\n")
    tt = "{:.2f}".format(todays_total)
    print("{:>10}".format("Cash earned: "))
    print("{:<10}".format("-------------"))
    print("$" + tt)
    print("\n")
