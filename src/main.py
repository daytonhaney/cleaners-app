#!/usr/bin/tenv python3
import os
import sqlite3
from datetime import datetime
from sqlite3 import Error
from time import sleep

import pyfiglet

from db.db_functions import *

# connection and first table tested Ok
# creates sql db in current directory (DB)
#

employee_audit = list()
list_audit = list()
cust_audit = list()

total_services = {
    "Regular": "General-Tidying, Sweep, Dust, Mop, $100.00",
    "Premium": "Regular Service+, Bathrooms, Closets, Laundry, Senior 10% Discount, $200.00",
    "Outdoor": "Mowing, Weed-Wack, Shrubs, Leaves, Senior, 10% Discount, $200.00\n",
}


def text_colors(color):
    "ui"
    colors = {"RESET": "\033[m", "RED": "\033[31m]", "GREEN": "\033[32m"}

    def text(text):
        c = colors.get(color.upper(), "")
        return f"{c}{text}{colors['RESET']}"
    print(text)
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
    for i in (name, date, my_class):
        print("")
        print(i)

    a = employee_audit.extend([name, date, my_class, badge_id])

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

    sleep(1)

    dis = "Age 65+ 10% Discount"
    dis_banner = dis.center(60)
    print("\n", dis_banner)
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
        cash = text_colors("green")
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
    service_selection = True
    while True:
        print("Cleaning packages...\n ")
        sleep(0.50)
        print("\n1.Regular Package ---> $100.00", "\n", total_services["Regular"])
        sleep(0.50)
        print("\n2.Premium Package ---> $200.00", "\n", total_services["Premium"])
        sleep(0.50)
        print("\n3.Outdoor Package ---> $300.00", total_services["Outdoor"])
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
            print(f"Customer selects:\n {total_services['Outdoor']}")
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

    cust_audit.append(service_selection)
    print(cust_audit)
    return cust_audit


def price_per_house(total_area):
    """area of house"""
    prices = {"REGULAR": 100, "PREMIUM": 200, "OUTDOOR": 300}
    l = float(input("""Enter length x" y'' """))
    w = float(input("""Enter Width x"y'' """))
    labor = float(0.15)

    area = l * w
    price = labor * area

    def payment():
        p = cust_audit.get("service_selection", "")
        print(p)
        return p

    return payment


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

    if __name__ == "__main__":
        main()


main()
