#!/usr/bin/tenv python3
import os
import sqlite3
import sys
from datetime import datetime
from sqlite3 import Error
from time import sleep

import pyfiglet

from db.db_functions import *

# connection and first table tested Ok
# creates sql db in current directory (DB)
#

employee_audit = []
list_audit = []
cust_audit = []

PRICE = {"r": 100, "p": 200, "o": 300}

total_services = {
    "Regular": "General-Tidying, Sweep, Dust, Mop $100.00",
    "Premium": "Regular Service+, Bathrooms, Closets, Laundry, Senior 10% Discount ,$200.00",
    "Outdoor": "Mowing, Weed-Wack, Shrubs, Leaves, Senior, 10% Discount, $200.00",
}


def text_colors(color):
    "ui"
    colors = {"RESET": "\033[m", "RED": "\033[31m]", "GREEN": "\033[32m"}

    def text(text):
        c = colors.get(color.upper(), "")
        return f"{c}{text}{colors['RESET']}"

    return text


def banner():
    "ui"
    b = "=" * 78
    print(b)


def intro():
    "prints info to screen"
    inout = pyfiglet.figlet_format(" IN & OUT Cleaning Corp.")
    name, date, my_class, badge_id = (
        "Jay Pren",
        datetime.now().strftime("%A, %d, %B %Y %I:%M%p"),
        "CMIS-120",
        8911,
    )
    for i in (name, date, my_class, badge_id):
        print("")
        print(i)

    employee_audit = " ".join(
        [str(i) for i in [name, date, my_class, badge_id]],
    )

    print("\n", employee_audit)

    banner()
    banner()
    print(inout.center(78))
    return employee_audit


def user_interface():
    "ui"
    intro()
    cash = text_colors("green")
    print("")

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

    d = "Age 65+ 15% Discount"
    d_banner = d.center(50)
    print(d_banner)

    banner()
    banner()
    return user_interface


def new_customer():
    """customers"""
    addr = ""
    new_cx = input("Name:\t")
    valid_age = input("Age:\t")

    if new_cx.isdigit() is True:
        print("error, letters only")
        new_cx = input("Name:\t")

    if valid_age.isalpha() is True:
        print("error, numbers only")
        valid_age = int(input("Age:\t"))
    if int(64) < int(valid_age) < int(100):
        discount = True

        print("\nDiscount Applied!\n")
    else:
        discount = False

    addr = input("Address:\t")
    valid_name = new_cx.replace(" ", "") and new_cx.upper()
    valid_addr = addr.replace(" ", "") and addr.upper()
    c = [valid_name, valid_addr, valid_age, discount]
    cust_audit.extend(c)
    print(cust_audit)
    print("")
    print(f"Welcome, {new_cx}")

    return cust_audit


def customer_transaction():
    "1 2 or 3"
    p = [100, 200, 300]
    service_selection = True
    while True:
        print("Cleaning packages...\n ")
        sleep(0.50)
        print("\n1.Regular Package ---> $100.00", "\n", total_services["Regular"])
        sleep(0.50)
        print("\n2.Premium Package ---> $200.00", "\n", total_services["Premium"])
        sleep(0.50)
        print("\n3.Outdoor Package ---> $300.00", "\n", total_services["Outdoor"])
        print("$.15 per square foot of house is charged for labor\n")
        break

    print("Chose cleaning package...")
    sleep(0.4)
    service_selection = int(
        input(
            """
    Press ---[1]---> Regular\n 
    Press ---[2]---> Premium\n
    Press ---[3]---> Outdoor\n
    """,
        )
    )

    if service_selection == int(1):
        print(f"Customer selects:\n {total_services['Regular']}")
        service_selection = total_services["Regular"]

    elif service_selection == int(2):
        print(f"Customer selects:\n {total_services['Premium']}")
        service_selection = total_services["Premium"]

    elif service_selection == int(3):
        for selection in total_services.items():
            print(
                f"Customer selects:\n  {selection}\n\tServices:\n\t {total_services['Regular']}"
            )
            service_selection = total_services["Outdoor"]
    else:
        if (
            service_selection != total_services["Regular"]
            or total_services["Premium"]
            or total_services["Outdoor"]
        ):
            print("Error")
            print("Enter 1 2 or 3")
            customer_transaction()
    print("Measure length and width of exterior for price")
    length = int(input("Length:\t"))
    width = int(input("Width:\t"))
    total_price = price_per_house(length, width)

    if all(cust_audit):
        total_price = get_discount(total_price)

    print(total_price)

    print(cust_audit)
    return cust_audit


def get_discount(price):
    if cust_audit[3] is True:
        dis = price * 0.15
        dis_price = price - dis
        return dis_price


def price_per_house(l, w) -> int:
    """area of house"""
    price = 0
    p = {"reg": 100, "prem": 200, "out": 300}
    labor = float(0.15)
    area: int = l * w
    labor_p = area * labor

    if total_services["Regular"]:
        price = labor_p + p["reg"]

    if total_services["Premium"]:
        price = labor_p + p["prem"]

    if total_services["Outdoor"]:
        price = labor_p + p["out"]

    print("testies")
    return price


def main():
    """main fn"""
    data = []
    new_table = False

    create = input("Create DB?(y/n) \t ")
    if create == str("Y") or create == str("y"):
        try:
            db = create_database()
            customers_table(create_database, cx_table_create)
        except Error as e:
            print(f"{e}")

        print(f"DB & table created: {DB}:{db}")

    elif create == str("N") or create == str("n"):
        print("DB not created")

    user_interface()
    new_customer()
    customer_transaction()

    backups = input("Backup Database?(y/n) \t ")
    if backups == "y" or backups == "y":
        backup_database()
    elif backups == "n" or backups == "N":
        print("Skipping backups")
    else:
        print("Error")

    print("--end-customer_trasnaction()---")

    while create is not None:
        loop = int(input("Press 1 then <Enter> to go again: \t "))
        if loop is int(1):
            main()
        else:
            sys.exit()


main()
