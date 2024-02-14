#!/usr/bin/env python3
import os.path
import sqlite3
import sys
from datetime import datetime
from sqlite3 import Error
from time import sleep

from cleaners.clean import *
from db.db_functions import *


def main():
    """main fn"""

    # dbug stments
    # p("begin main")
    customers = True
    cust_names = None
    cust_addrs = None

    labor = []
    totals = []
    discounts = []

    c_data = []
    e_data = []

    c_names = list()
    c_address = list()
    c_discounts = list()
    c_totals = list()

    db_create = input("\nCreate sqlite3 database?(y/n) \t ")

    cash = text_colors("green")
    pay = text_colors("red")

    if db_create == str("Y") or db_create == str("y"):
        path = "./business_data.db"
        check_db = os.path.isfile(path)
        if check_db is True:
            print(f"DB already exists in {path}")
        else:
            print("Creating database...\n")
            sleep(0.1)
            print(f"{DB} created in {path}")
            try:
                db = create_database()
                customers_table(create_database, cx_table_create)
                e_table = employee_table(create_database, emp_table_create)
            except Error as e:
                print(f" {e}")
                print(f"\nBusiness_data.db & table created: {DB} in current directory")
    elif db_create == str("N") or db_create == str("n"):
        print("DB not created\n")

    while customers:

        employee_list = get_employees()
        employee_list.append(e_data)

        cust_names, valid_name, discount, cust_addrs = new_customer()
        customers = valid_name

        if valid_name:

            c_names.append(cust_names)
            c_address.append(cust_addrs)
            discounts.append(discount)

            discounts.append(c_discounts)  # for final function

            print(
                f"Name:{c_names}Address:{c_address}Discount:{discounts} c_discounts:{c_discounts}\n"
            )
            p("")

            user_interface()
            selection = cust_selection()
            c_data.append(selection)
            p(selection)

            totals = customer_transaction(selection, discounts[-1])
            c_totals.append(
                totals
            )  # the selection is the return of price_per_house inside customer_transaction

            # debug info:
            print(
                "discount stack =",
                pay(discounts),
                c_discounts.append(discounts),
                "totals before discount =",
                c_totals,
            )

            pay("\nFinal total:")
            print(c_totals)

            if discounts:
                discount_stack = discounts.pop()

                if discount_stack == (1, True):
                    dis = get_discount(c_totals[-1])
                    PRICE = totals.pop()  # price no dis
                    # error can't multiply sequence by non-int type float in var

                    print("\nPrice:", pay(PRICE))
                    print("\nDiscount price: ", cash(dis))
                    pay(PRICE)
                    final_total = final_price(PRICE, dis)
                    # get both totals final_price()
                    banner()
                    print("\tFinal total after discount:")
                    print("\t{:.2f}".format(final_total))
            else:
                continue

    display_customer_info(c_names, c_address, discounts, c_totals)

    backup = input(f"Backup {DB}?(y/n) \t ")
    if backup == str("Y") or backup == str("y"):
        check_ = os.path.isfile("business_data.db")
        if check_:
            backup_database()
    else:
        pass


main()
