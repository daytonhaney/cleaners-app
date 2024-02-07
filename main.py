#!/usr/bin/env python3
import os
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
    p("begin main")
    customers = True
    addrs = None
    names = None

    labor = []
    totals = []
    discounts = []

    c_data = []
    e_data = []

    customer_transaction_totals = []
    customer_names = []
    customer_address = []

    db_create = input("\nCreate sqlite3 database?(y/n) \t ")

    cash = text_colors("green")
    pay = text_colors("red")
    prices, discount = ([100, 200, 300], [0.15])

    if db_create == str("Y") or db_create == str("y"):
        print("Creating database...\n")
        sleep(0.5)
        try:
            db = create_database()
            customers_table(create_database, cx_table_create)
        except Error as e:
            print(f" {e}")
            print(f"\nBusiness_data.db & table created: {DB} in current directory")
    elif db_create == str("N") or db_create == str("n"):
        print("DB not created\n")

    while customers:

        employee_list = get_employees()
        employee_list.append(e_data)
        valid_name, names, addrs, discount = new_customer()
        print(type(valid_name))
        customers = valid_name
        if valid_name:
            customer_names.append(names)
            customer_address.append(addrs)
            discounts.append(discount)

            print(f"{customer_names}{customer_address}{discounts}\n")
            p("")
            user_interface()
            selection = cust_selection()
            c_data.append(selection)
            p(selection)
            totals = customer_transaction(selection, discounts[-1])
            customer_transaction_totals.append(
                totals
            )  # the selection is the return of price_per_house inside customer_transaction

            # debug info:
            print(
                "discount stack =",
                pay(discounts),
                "totals before discount =",
                customer_transaction_totals,
            )

            cash("Final total:")
            print(customer_transaction_totals[0])

            if discounts:
                discount_stack = discounts.pop()

                if discount_stack == (1, True):
                    dis = get_discount(customer_transaction_totals[-1])
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

    print("exit")
    sys.exit("come again")


main()
