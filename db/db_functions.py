#!/usr/bin/env python3
"""Cleaning Service sqlite3 database functions"""

import os
import sqlite3
import subprocess
from sqlite3 import Error

#from cleaners.clean import *
#from cleaners.fig import *
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


def query_exec(q, data=None):
    """query data"""

    con = sqlite3.connect(DB)
    cur = con.cursor()
    try:
        if data:
            cur.execute(q, data)
        else:
            cur.execute(q)
        con.commit()
        return cur
    except Error as e:
        print(f"Error in query_exec: {e}")
    finally:
        cur.close()


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


def insert_cust_totals(name, addr, amount_paid=0, discount=0):
    """insert customer name and address,
    set defaults to 0 for amount_paid and discount until payment is made"""

    q = """insert into customers (name,address,amount_paid,discount) values (?,?,?,?)"""
    data = (
        name,
        addr,
        amount_paid,
        discount,
    )
    if os.path.isfile(DB):
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
                print("record exists")
        except Error as e:
            print(f"Error in insert_employee: {e}")
        con.close()

    else:
        pass


def get_customer_name(name):
    """query data"""

    q = "select * from customers where name = ?:"
    data = (name,)
    cur = query_exec(q, data)
    
    return cur.fetchall()


def provision_database():
    """return a db for conditionals"""

    db_create = input(f"Create sqlite3 {DB} [y/n]? \t ")
    if db_create in ["y", "yes", "Y", "YES"]:
        if os.path.isfile(DB):
            print(f"Database already exists in {DB}")
        if not os.path.isfile(DB):
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
        print("\n")


def backup_database():
    """backup database"""

    if os.path.isfile(DB):
        backup = input(f"Backup {DB} [y/n]? \t ")
        if backup in ["y", "yes", "Y", "YES"]:
            data_backups = os.path.isfile("business_data.db")
            if data_backups:
                subprocess.run(["chmod", "u+x", "backup.sh"])
                subprocess.run(["./backup.sh"])
                exit()
    else:
        print("Run ./backup.sh to create backup")
        exit()
