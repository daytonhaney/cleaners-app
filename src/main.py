#!/usr/bin/env python3
from datetime import datetime
from time import sleep
import sqlite3
from sqlite3 import Error
import os
import pyfiglet
from db.db_functions import *

# connection and first table tested Ok
# creates sql db in current directory (DB)
#

list_audit = list()
employee_audit = dict()
cust_audit = dict()

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

    return text


def banner():
    "ui"
    b = "=" * 78
    print(b)


def intro():
    "prints info to screen"
    inout = pyfiglet.figlet_format(" IN & OUT Cleaning Corp.")
    name, date, my_class = (
        "Jay Pren",
        datetime.now().strftime("%A, %d, %B %Y %I:%M%p"),
        "CMIS-120\n\n\n",
    )
    for i in (name, date, my_class):
        print("")
        print(i)
    employee_audit["name"] = name
    employee_audit["date"] = date
    employee_audit["class"] = my_class
    print(employee_audit)
    banner()
    banner()
    print(inout.center(78))


def user_interface():
    "ui"
    intro()
    cash = text_colors("green")
    cash("This is green")
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
        cash("\t  $100"),
        cash("\t\t$100"),
    ]:
        print("{:>20}{:>20}{:>20}".format(*display3))

    sleep(1)

    discount = "Age 65+ 10% Discount"
    discount_center = discount.center(60)
    print("\n", discount_center)
    banner()
    banner()
    return user_interface


def new_customer():
    """customers"""
    discount = bool
    addr = ""
    new_cx = input("Name:\t")
    valid_age = input("Age:\t")
    addr = input("Address:\t")

    if new_cx.isdigit() is True:
        print("error, letters only")
        new_cx = input("Name:\t")
        valid_name = True

    if valid_age.isalpha() is True:
        print("error, numbers only")
        valid_age = int(input("Age:\t"))
        if valid_age >= int(65):
            discount = True
        else:
            discount = False

    valid_name = new_cx.replace(" ", "") and new_cx.upper()
    valid_addr = addr.replace(" ", "") and addr.upper()
    cust_audit["name"] = valid_name
    cust_audit["age"] = valid_age
    cust_audit["address"] = valid_addr
    cust_audit["discount"] = discount

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
        print(f"You chose:\n {total_services['Regular']}")
        service_selection = total_services["Regular"]
        cust_audit["order"] = service_selection

    elif service_selection == int(2):
        print(f"You chose:\n {total_services['Premium']}")
        service_selection = total_services["Premium"]
        cust_audit["order"] = service_selection

    elif service_selection == int(3):
        for selection in total_services:
            print("{}:{}".format(selection, total_services[selection]))
        print(f"You chose:\n {total_services['Outdoor']}")
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
    print(cust_audit)
    return service_selection, cust_audit


def price_per_house(total_area):
    """area of house"""
    prices = {"REGULAR": 100, "PREMIUM": 200, "OUTDOOR": 300}
    l = float(input("""Enter length x" y'' """))
    w = float(input("""Enter Width x"y'' """))
    labor = float(0.15)

    area = l * w
    price = labor * area
    cust_audit["area"] = area
    cust_audit["price"] = price

    def payment():
        p = cust_audit.get("service_selection", "")
        print(p)
        return p

    return payment


def main():
    """main fn"""
    db_created = {}
    new_table = False

    create = input("Create DB?(y/n) \t ")
    if create == str("Y") or create == str("y"):
        con = None
        try:
            con = sqlite3.connect(DB)
            customers_table(con, cx_table_create)
            con.close()
        except Error as e:
            print(f"{e}")

        db_created["create"] = True
        print(f"DB created: {DB}{con}")

    elif create == str("N") or create == str("n"):
        print("DB not created")
        db_created["create"] = False

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
    print("--endmain--")

    if __name__ == "__main__":
        main()


main()
