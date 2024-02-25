#!/usr/bin/env python3

from cleaners.clean import (
    cust_selection,
    customer_transaction,
    display_customer_info,
    final_price,
    get_discount,
    get_employees,
    new_customer,
    text_colors,
    user_interface,
)
from db.db_functions import backup_database, insert_cust_totals, provision_database


def main():
    """main fn"""

    # p("begin main")
    customers = True
    cust_names = None
    cust_addrs = None
    c_names = list()
    c_address = list()
    c_discounts = list()
    c_totals = list()

    discounts = []
    c_data = []

    cash = text_colors("green")
    check_db = provision_database()

    while customers:

        employee_list = get_employees()
        cust_names, valid_name, discount, cust_addrs = new_customer()
        customers = valid_name
        if valid_name:
            c_names.append(cust_names)
            c_address.append(cust_addrs)
            discounts.append(discount)
            user_interface()
            if discount == (1, True):
                # discount final total
                selection = cust_selection()
                totals = customer_transaction(selection, discounts[-1])
                final_total = totals[-1]
                dis = get_discount(final_total)
                f_discount = "{:.2f}".format(dis)
                print("Dis:", cash(dis))
                dis_ft = final_price(final_total, dis)
                c_totals.append(dis_ft)
                c_discounts.append(f_discount)
            else:
                dis = 0
                c_discounts.append(dis)
                selection = cust_selection()
                ft = customer_transaction(selection, discounts[-1])
                c_totals.extend(ft)
            insert_cust_totals(cust_names, cust_addrs, c_totals[-1], c_discounts[-1])
    display_customer_info(c_names, c_address, c_discounts, c_totals)
    backup_database()


main()
