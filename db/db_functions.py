#!/usr/bin/env python3

import os
import sqlite3
import subprocess
from sqlite3 import Error

DB = "business_data.db"

cx_table = """create table if not exists customers (
id integer primary key autoincrement,
name text  not null,
address text not null,
amount_paid integer not null)"""


emp_table = """create table if not exists employees (
id integer primary key autoincrement,
name text not null,
address text not null,
region text not null,
badge_id integer not null)"""


def create_database():
    DB = "business_data.db"
    con = None
    try:
        con = sqlite3.connect(DB)
        return con
    except OSError as e:
        print(e)

    return con


def query_exec(q, data=None):
    "query data"
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
        print(f"{e}")
    finally:
        cur.close()


def employee_table(con, emp_table):
    "create table - employees"

    con = sqlite3.connect(DB)
    try:
        cur = con.cursor()
        cur.execute(emp_table)

    except Error as e:
        print(f"{e}")
    return con


def customer_table(con, cx_table):
    """create table - customers"""

    con = sqlite3.connect(DB)
    try:
        cur = con.cursor()
        cur.execute(cx_table)

    except Error as e:
        print(f"{e}")
    return con


def insert_customer(valid_cx, valid_addr, amount_paid, discount=bool):
    """insert customer"""
    # 0 or 1 if discount is true

    q = "insert into customers (name,street,amount_paid, discount) values (?,?,?)"
    data = (valid_cx, valid_addr, amount_paid, discount)
    query_exec(q, data)


def insert_employee(name, address, region, badge_id):
    """insert employee"""
    q = "insert into employees (name,address,region,badge_id) values (?,?,?,?)"
    data = (
        name,
        address,
        region,
        badge_id,
    )
    query_exec(q, data)


def get_customer_name(name):
    """query data"""
    q = "select * from customers where name = ?:"
    data = (name,)
    cur = query_exec(q, data)
    return cur.fetchall()


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


def backup_database():
    """backup database"""

    backup = input(f"Backup {DB}[y/n]? \t ")
    if backup == str("Y") or backup == str("y"):
        data_backups = os.path.isfile("business_data.db")
        if data_backups:
            subprocess.run(["chmod", "u+x", "backup.sh"])
            subprocess.run(["./backup.sh"])
        else:
            print("DB not found")
