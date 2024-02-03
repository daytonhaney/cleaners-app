#!/usr/bin/tenv python3

from datetime import datetime
from time import sleep

import pyfiglet

employee_audit = []
list_audit = []
cust_audit = []

PRICE = {"r": 100, "p": 200, "o": 300}
total_services = {
    "Regular": "General-Tidying, Sweep, Dust, Mop $100.00",
    "Premium": "Regular Service+, Bathrooms, Closets, Laundry $200.00",
    "Outdoor": "Mowing, Weed-Wack, Shrubs, Leaves $300.00",
}
LIST_PRICE = [100,200,300]

def text_colors(color):
    """ui"""
    colors = {"RESET": "\033[m", "RED": "\033[31m]", "GREEN": "\033[32m"}

    def text(text):
        c = colors.get(color.upper(), "")
        return f"{c}{text}{colors['RESET']}"

    return text


def banner():
    """ui"""
    b = "=" * 78
    print(b)


def get_discount(total):
    """calculate discount"""
    if cust_audit[3] is True:
        dis = total * 0.15
        dis_price = total - dis
        print("getting discount...")
        print(dis_price)
        return dis_price


def labor_charge(area):
    """calculate labor"""
    labor = area * 0.15
    return labor


def printer():
    """test"""
    x = print("testing-------------------------------------")
    return x
printer()



def intro():
    """prints info"""
    inout = pyfiglet.figlet_format(" IN & OUT Cleaning Corp.")
    name, date, my_class, badge_id = (
        "Mike Chambers",
        datetime.now().strftime("%A, %d, %B %Y %I:%M%p"),
        "North East",
        "M891132",
    )

    for i in (name, date, my_class, badge_id):
        print(i)

    employee_audit.append([name, date, my_class, badge_id])
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

    print("")
    d = "Age 65+ 15% Discount"
    d_banner = d.center(80)
    print(d_banner)
    banner()
    banner()
    return user_interface


def new_customer():
    """customers"""
    new_c = []
    addr = ""
    new_cx = input("Name:\t")
    valid_age = input("Age:\t")

    if new_cx.isdigit() is True:
        print("error, letters only")
        new_cx = input("Name:\t")

    if valid_age.isalpha() is True:
        print("error, numbers only")
        valid_age = int(input("Age:\t"))
    if int(64) < int(valid_age) < int(120):
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
    print(f"Welcome, {new_cx}", "\n")

    return cust_audit


def customer_transaction():
    "1 2 or 3"
    PRICE = [100, 200, 300]
    valid = False
    while valid is False:
        print("\tCleaning packages...\n ")
        sleep(0.50)
        print(
            "\n1.Regular Package ---> $100.00",
            "\n",
            total_services["Regular"],
        )
        sleep(0.50)
        print(
            "\n2.Premium Package ---> $200.00",
            "\n",
            total_services["Premium"],
        )
        sleep(0.50)
        print(
            "\n3.Outdoor Package ---> $300.00",
            "\n",
            total_services["Outdoor"],
        )
        print("")
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
        print(f"Customer selects:\n{total_services['Regular']}\n")
        print("Measure Length and width of exterior for price")
        l = int(input("Length:\t"))
        w = int(input("Width:\t"))
        s = PRICE[0]
        price_per_house(s,l,w)
        return

    if service_selection == int(2):
        print(f"Customer selects:\n {total_services['Premium']}")
        print("Measure Length and width of exterior for price")
        l = int(input("Length:\t"))
        w = int(input("Width:\t"))
        s2 = PRICE[1]
        price_per_house(s2,l,w)
        return

    elif service_selection == int(3):
        print(f"Customer selects:\n {total_services['Outdoor']}")
        print("Measure Length and width of exterior for price")
        l = int(input("Length:\t"))
        w = int(input("Width:\t"))
        s3 = PRICE[2]
        price_per_house(s3,l,w)
        return

    else:
        if (
            service_selection != total_services["Regular"]
            or total_services["Premium"]
            or total_services["Outdoor"]
        ):
            print("Error")
            print("Enter 1 2 or 3")
            customer_transaction()


def price_per_house(s,l,w):
    """price"""
    area = l * w
    if s == LIST_PRICE[0]: # ? have any effeTotal price with discount: 182.75cts?
        labor = labor_charge(area)
        total = s + labor
        total += 100 # something not being added correctly, hard coded 100
        reg_total = round(total,3)
        print(f"Rrice for Regular: ${reg_total}")


    elif s == LIST_PRICE[1]:
        labor = labor_charge(area)
        total = s + labor
        total += 200
        prem_total = round(total,3)
        print(f"price for Premium: ${prem_total}")

    elif s == total_services["Outdoor"]:
        labor = labor_charge(area)
        total = s + labor
        total += 300
        out_total = round(total,3)
        print(f"price for Outdoor: ${out_total}")

    if all(cust_audit) is True:
        labor = labor_charge(area)
        discounted = get_discount(total)
        total = s + labor
        print(f"Total price with discount: {discounted}")
        return discounted

    if all(cust_audit) is False:
        labor_charge(area)
        discounted = get_discount(total)
        print(f"Total price with discount: {discounted}")
        return discounted




