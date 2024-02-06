#!/usr/bin/env python3
import os
import sqlite3
import sys
from datetime import datetime
from sqlite3 import Error
from time import sleep

import pyfiglet

from cleaners.clean import *
from db.db_functions import *


def main():
    """main fn"""

    total_services = {
        "Regular": "General-Tidying, Sweep, Dust, Mop $100.00",
        "Premium": "Regular Service+, Bathrooms, Closets, Laundry $200.00",
        "Outdoor": "Mowing, Weed-Wack, Shrubs, Leaves $300.00",
    }
    pay = text_colors("red")

    # dbug stments
    p("23 begin main")
    customers = True
    addrs = None
    names = None

    discounts = []
    c_data = []

    customer_transaction_totals = []
    customer_names = []
    customer_address = []

    prices, discount = ([100, 200, 300], [0.15])

    while customers:
        p("--- while customers-----")
        get_employees()
        db_create = input("\nCreate sqlite3 database?(y/n) \t ")

        if db_create == str("Y") or db_create == str("y"):
            print("Creating database...\n")
            sleep(0.5)
            try:
                db = create_database()
                customers_table(create_database, cx_table_create)
            except Error as e:
                print(f" {e}")
            print(f"\nDatabase.db & table created: {DB} in current directory")
        elif db_create == str("N") or db_create == str("n"):
            print("DB not created\n")

        valid_name, names, addrs, discount = new_customer()
        customers = valid_name

        if valid_name:

            p(" if valid name")
            customer_names.append(names)
            customer_address.append(addrs)
            discounts.append(discount)
            print(" --if-- ")
            print(f"{customer_names}{customer_address}{discounts}")
            user_interface()

            selection = cust_selection()
            c_data.append(selection)

            totals = customer_transaction(selection, discounts[-1])
            customer_transaction_totals.append(
                totals
            )  # the selection is the return of price_per_house inside customer_transaction

            discount_stack = discounts.pop()
            print(
                "discount stack=",
                pay(discount_stack),
                "totals=",
                customer_transaction_totals,
            )
            p(customer_transaction_totals[-1])
            print(customer_transaction_totals[0])

            if discount_stack == 1:
                cash = text_colors("green")
                discount_price = get_discount(
                    customer_transaction_totals[-1]
                    # error can't multiply sequence by non-int type float in var dis
                )
                print("{:^10}".format(discount_price))
                cash(f"{discount_price}").center(40)
                # test
                pay = text_colors("red")
                pay(f"{discount_price}")

    print("exit")
    sys.exit("come again")


main()
