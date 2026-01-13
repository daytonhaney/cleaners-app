#!/usr/bin/env python3
"""Cleaning Service sqlite3 database functions"""

import os
import sqlite3
import subprocess
from sqlite3 import Error

# from cleaners.clean import *
# from cleaners.fig import *
DB = "./business_data.db"


cx_table = """create table if not exists customers (
    id integer primary key autoincrement,
    name text  not null,
    address text not null,
    amount_paid not null,
    discount not null) """

emp_table = """create table if not exists employees (
    id integer primary key autoincrement,
    name text not null,
    address text not null,
    region text not null,
    badge_id integer not null)"""


def does_db_exist(DB):
    """check if db exists"""
    if DB == os.path.isfile(DB):
        return True


def e_table_exists(db, table):
    """check if table exists"""

    q = """select count(name) from sqlite_master where type='table' and name='employees'"""
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(q)
    if cur.fetchone()[0] == 1:
        table = True
        # print("t")
    else:
        table = False
        # print("f")
    con.commit()
    con.close()

    return table


def c_table_exists(db, table):
    """check if table exists"""

    q = """select count(name) from sqlite_master where type='table' and name='customers'"""
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(q)
    rows = cur.fetchone()[0]

    if rows != 0:
        c_table = True
        # print("t")
    else:
        c_table = False
        # print("f")
    con.commit()
    con.close()

    return c_table


def create_database():
    """create db"""
    con = None
    try:
        con = sqlite3.connect(DB)
        return con
    except OSError as e:
        print(f"Error in create_database: {e}")

    return con


def query_exec(q, data=None, keep_open=False):
    """query data - always uses parameterization for security"""

    con = sqlite3.connect(DB)
    cur = con.cursor()
    try:
        if data:
            cur.execute(q, data)
        else:
            # For security, only allow hardcoded queries without parameters
            # Check if query contains any user-input patterns
            if any(
                pattern in q.upper()
                for pattern in [
                    "SELECT",
                    "INSERT",
                    "UPDATE",
                    "DELETE",
                    "DROP",
                    "CREATE",
                    "ALTER",
                ]
            ):
                # Allow only table creation and schema queries without data
                if not any(
                    keyword in q.upper() for keyword in ["VALUES", "WHERE", "SET"]
                ):
                    cur.execute(q)
                else:
                    raise ValueError("Query with user data requires parameterization")
            else:
                cur.execute(q)
        con.commit()

        if keep_open:
            return cur, con
        else:
            return cur
    except Error as e:
        print(f"Error in query_exec: {e}")
        if keep_open:
            cur.close()
            con.close()
    finally:
        if not keep_open:
            cur.close()
            con.close()


def employee_table(con, emp_table):
    """create table - employees"""
    """conditionsals added to avoid duplicates on program restarts"""

    new_e_table = False
    if os.path.isfile(DB):
        con = sqlite3.connect(DB)
        if con:
            new_e_table = True
            try:
                cur = con.cursor()
                cur.execute(emp_table)
                # print("e table created")
                con.close()
            except Error as e:
                print(f"Error in employee_table: {e}")

    return new_e_table, con


def customer_table(con, cx_table):
    """create table - customers"""

    if os.path.isfile(DB):
        con = sqlite3.connect(DB)
        try:
            cur = con.cursor()
            cur.execute(cx_table)
            # print("c table created")
        except Error as e:
            print(f"Error in customer_table: {e}")
        return con
    else:
        pass


def insert_cust_totals(names, addresses, discounts, totals):
    """insert customer name and address,
    set defaults to 0 for amount_paid and discount until payment is made"""

    q = """insert into customers (name,address,amount_paid,discount) values (?,?,?,?)"""

    # Handle case where single values are passed
    if isinstance(names, str):
        names = [names]
        addresses = [addresses] if addresses else [""]
        discounts = [discounts] if discounts else [0]
        totals = [totals] if totals else [0]

    if os.path.isfile(DB):
        # Insert each customer
        for i in range(len(names)):
            data = (
                names[i],
                addresses[i] if i < len(addresses) else "",
                totals[i] if i < len(totals) else 0,
                discounts[i] if i < len(discounts) else 0,
            )
            query_exec(q, data)
    elif not os.path.isfile(DB):
        pass


def insert_employee(name, address, region, badge_id):
    """insert employee"""

    q = """INSERT INTO employees (name, address, region, badge_id) VALUES (?, ?, ?, ?)"""
    q1 = """select count(*) from 'employees'"""
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(q1)
    e_rows = cur.fetchone()[0]
    if os.path.isfile(DB):
        try:
            if e_rows == 0:
                data = (name, address, region, badge_id)
                query_exec(q, data)
                con.commit()
            else:
                # print("record exists")
                pass
        except Error as e:
            print(f"Error in insert_employee: {e}")
        finally:
            con.close()

    else:
        pass


def get_customer_name(name):
    """query data"""

    q = "select * from customers where name = ?"
    data = (name,)
    result = query_exec(q, data, keep_open=True)

    if result:
        cur, con = result
        try:
            return cur.fetchall()
        finally:
            cur.close()
            con.close()
    return []


def provision_database():
    """return a db for conditionals"""

    # Check if database already exists first
    if os.path.isfile(DB):
        print(f"Database already exists in {DB}")
        try:
            db = sqlite3.connect(DB)
            return db
        except Error as e:
            print(f"Error connecting to existing database: {e}")

    # Try to get user input, default to 'y' if not available
    try:
        db_create = input(f"Create sqlite3 {DB} [y/n]? \t ")
    except (EOFError, KeyboardInterrupt):
        # Handle cases where input is not available (e.g., in executable)
        db_create = "y"  # Default to creating database
        print(f"Auto-creating database {DB}")

    if db_create in ["y", "yes", "Y", "YES"]:
        try:
            db = create_database()
            cx_new_tbl = customer_table(db, cx_table)
            emp_new_tbl = employee_table(db, emp_table)
            print(f"Database and tables created in {DB}")
            return db
        except Error as e:
            print(f"Error in provision_database {e}")
    else:
        print("DB not created")
        return None
        print("\n")


def backup_database():
    """backup database - self-contained implementation"""

    if os.path.isfile("business_data.db"):
        # Try to get user input, default to 'n' if not available
        try:
            backup_choice = input("Backup database? [y/n]: \t ")
        except (EOFError, KeyboardInterrupt):
            # Handle cases where input is not available (e.g., in executable)
            backup_choice = "n"  # Default to not backing up
            print("Skipping database backup")

        if backup_choice in ["y", "yes", "Y", "YES"]:
            import shutil
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y-%m-%d")
            backup_name = f"business_data_backup-{timestamp}.db"

            try:
                shutil.copy2("business_data.db", backup_name)
                print(f"Backup successful: {backup_name}")
                return True
            except Exception as e:
                print(f"Backup failed: {e}")
                return False
        else:
            print("Database backup skipped")
            return False
    else:
        print("No database file found to backup")
        return False
