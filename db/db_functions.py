#!/usr/bin/env python3

# connection and first table tested Ok
# in progress
#
import sqlite3
import subprocess
from sqlite3 import Error

DB = "business_data.db"

cx_table_create = """create table if not exists customers (
id integer primary key autoincrement,
name text  not null,
street text not null,
amount_paid integer not null)"""



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


def employee_table(con, emp_table_create):
    "create table - employees"

    emp_table_create = """create table if not exists employees (
    id integer primary key auto increment,
    name text not null,
    street text not null,
    badge_id integer not null)"""
    con = sqlite3.connect(DB)
    try:
        cur = con.cursor()
        cur.execute(emp_table_create)

    except Error as e:
        print(f"{e}")
    return con


def customers_table(con, cx_table_create):
    """create table - customers"""

    cx_table_create = """create table if not exists customers (
    id integer primary key autoincrement,
    name text  not null,
    street text not null,
    amount_paid integer not null)"""
    con = sqlite3.connect(DB)
    try:
        cur = con.cursor()
        cur.execute(cx_table_create)

    except Error as e:
        print(f"{e}")
    return con


def insert_customer(valid_cx, valid_addr, amount_paid, discount=bool):
    """insert customer"""
    # 0 or 1 if discount is true

    q = "insert into customers_table (name,street,amount_paid, discount) values (?,?,?)"
    data = (valid_cx, valid_addr, amount_paid, discount)
    query_exec(q, data)


def get_customer_name(name):
    """query data"""
    q = "select * from customers where name = ?:"
    data = (name,)
    cur = query_exec(q, data)
    return cur.fetchall()


def backup_database():
    """backup database"""
    subprocess.run(["chmod", "u+x", "backup.sh"])
    subprocess.run(["./backup.sh"])
