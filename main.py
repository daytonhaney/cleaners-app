#!/usr/bin/env python3
"""Cleaning Service entry point"""

from cleaners.cli import process_args
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
from cleaners.fig import io_figlets, io_figlets_title
from db.db_functions import backup_database, insert_cust_totals, provision_database

try:
    from cleaners.rich_ui import rich_newlines, rich_title

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def main():
    """Run the interactive cleaners app."""

    result = process_args("main")
    if result is not None:
        return

    customers = True
    c_names = []
    c_address = []
    c_discounts = []
    c_totals = []
    discounts = []

    cash = text_colors("green")
    provision_database()

    if RICH_AVAILABLE:
        rich_title()
        rich_newlines(1)
    else:
        io_figlets(io_figlets_title)

    while customers:
        get_employees()
        cust_name, valid_name, discount, cust_addr = new_customer()
        customers = valid_name

        if not valid_name:
            continue

        c_names.append(cust_name)
        c_address.append(cust_addr)
        discounts.append(discount)
        user_interface()

        try:
            from cleaners.rich_ui import rich_loading

            rich_loading("Processing transaction...")
        except ImportError:
            pass

        selection = cust_selection()

        if discount == (1, True):
            totals = customer_transaction(selection, discounts[-1])
            final_total = totals[-1]
            discount_amount = get_discount(final_total)
            discount_display = f"{discount_amount:.2f}"

            try:
                from cleaners.rich_ui import rich_discount_applied, rich_final_total

                rich_discount_applied(discount_amount)
                discounted_total = final_price(final_total, discount_amount)
                rich_final_total(discounted_total)
            except ImportError:
                print(cash(f"Discount: ${discount_amount:.2f}"))
                discounted_total = final_price(final_total, discount_amount)
                print(cash(f"Final Total: ${discounted_total:.2f}"))

            c_totals.append(discounted_total)
            c_discounts.append(discount_display)
        else:
            totals = customer_transaction(selection, discounts[-1])
            final_total = totals[-1]
            print(cash(f"Final Total: ${final_total:.2f}"))
            c_totals.append(final_total)
            c_discounts.append(0)

        insert_cust_totals(
            cust_name,
            cust_addr,
            c_discounts[-1],
            c_totals[-1],
        )

    display_customer_info(c_names, c_address, c_discounts, c_totals)
    backup_database()


if __name__ == "__main__":
    main()
