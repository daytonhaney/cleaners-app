#!/usr/bin/tenv python3

import sys

from cleaners.clean import *
from db.db_functions import *


def main():
    """main fn"""
    employee_audit = []
    list_audit = []
    cust_audit = []

    create = input("Create DB?(y/n) \t ")
    if create == str("Y") or create == str("y"):
        try:
            db = create_database()
            customers_table(create_database, cx_table_create)
        except Error as e:
            print(f"{e}")

        print(f"DB & table created: {DB}:{db}")

    elif create == str("N") or create == str("n"):
        print("DB not created\n")

    user_interface()
    new_customer()
    total = customer_transaction()
    backups = input("Backup Database?(y/n) \t ")
    if backups == "y" or backups == "y":
        backup_database()
    elif backups == "n" or backups == "N":
        print("Skipping backups")
    else:
        print("Error")

    print("--end-customer_trasnaction()---")

    while(total):
        loop = int(input("Press 1 then <Enter> to go again: \t "))
        if loop is int(1):
            cust_audit = []
            main()
        else:
            sys.exit()


main()
