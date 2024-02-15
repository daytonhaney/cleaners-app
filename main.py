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
            sleep(0.3)
            print(f"{path} created")
            try:
                db = create_database()
                customers_table(create_database, cx_table)
                employee_table(db, emp_table)
            except Error as e:
                print(f" {e}")
                print(f"\nBusiness_data.db & table created: {DB} in current directory")
    elif db_create == str("N") or db_create == str("n"):
        print("DB not created\n")

    while customers:

        employee_list = get_employees()
        e_data.append(employee_list)

        cust_names, valid_name, discount, cust_addrs = new_customer()
        customers = valid_name

        if valid_name:

            c_names.append(cust_names)
            c_address.append(cust_addrs)
            discounts.append(discount)

            discounts.append(c_discounts)  # for final function

            user_interface()
            selection = cust_selection()
            c_data.append(selection)
            p(selection)

            totals = customer_transaction(selection, discounts[-1])
            c_totals.append(totals)

            pay("\nFinal total:")
            print(c_totals)

            if discounts:
                discount_stack = discounts.pop()

                if discount_stack == (1, True):
                    dis = get_discount(c_totals[-1])
                    PRICE = totals.pop()

                    print("\nPrice:", pay(PRICE))
                    final_total = final_price(PRICE, dis)
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
