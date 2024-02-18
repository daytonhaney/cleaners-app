#!/usr/bin/env python3

import os
import sqlite3
import subprocess
from sqlite3 import Error

DB = "./business_data.db"

cx_table = """create table if not exists customers (
id integer primary key autoincrement,
name text  not null,
address text not null,
amount_paid integer not null)"""
# discounts integer not null) """

emp_table = """create table if not exists employees (
id integer primary key autoincrement,
name text not null,
address text not null,
region text not null,
badge_id integer not null)"""


def does_db_exist(DB):
    """check if db exists"""
    if DB == os.path.isfile(DB):
        print("")
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

    # return table is not None


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
    con = sqlite3.connect(DB)
    if con:
        new_e_table = True
        try:
            cur = con.cursor()
            cur.execute(emp_table)
            # print("e table created")
            con.close()
        except Error as e:
            print(f"error in employee_table: {e}")
    return new_e_table, con


def customer_table(con, cx_table):
    """create table - customers"""

    con = sqlite3.connect(DB)
    try:
        cur = con.cursor()
        cur.execute(cx_table)
        # print("c table created")

    except Error as e:
        print(f"Error in customer_table: {e}")
    return con


def insert_customer(valid_cx, valid_addr, amount_paid):
    """insert customer"""

    q = "insert into customers (name,street,amount_paid) values (?,?,?)"
    data = (
        valid_cx,
        valid_addr,
        amount_paid,
        # discounts,
    )
    query_exec(q, data)


def insert_employee(name, address, region, badge_id):
    """insert employee"""

    q = """INSERT INTO employees (name, address, region, badge_id) VALUES (?, ?, ?, ?)"""
    q1 = """select count(*) from 'employees'"""
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(q1)
    e_rows = cur.fetchone()[0]
    try:
        if e_rows == 0:
            data = (name, address, region, badge_id)
            query_exec(q, data)
            con.commit()
        else:
            print("record exists")
    except Error as e:
        print(f"error in insert_employee: {e}")
    con.close()


def get_customer_name(name):
    """query data"""
    q = "select * from customers where name = ?:"
    data = (name,)
    cur = query_exec(q, data)
    return cur.fetchall()


def provision_database():
    """return a db for conditionals"""

    db_create = input("\nCreate sqlite3 database [y/n]? \t ")
    if db_create in ("y", "yes"):
        path = "./business_data.db"
        if os.path.isfile(path):
            print(f"DB already exists in {path}")

        if not os.path.isfile(path):
            try:
                db = create_database()
                # print(f"{db} created ok")
                customer_table(db, cx_table)
                # print("customer table created ok")
                employee_table(db, emp_table)
                # print("employee table created ok")
                return db
            except Error as e:
                print(f" {e}")
            print(f"Databade and tables created in {path}")
    elif db_create != ("y", "yes"):
        print("db not created")


def backup_database():
    """backup database"""

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