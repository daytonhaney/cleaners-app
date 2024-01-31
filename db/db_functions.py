#!/usr/bin/env python3

# connection and first table tested Ok
# in progress
#
import subprocess
import sqlite3
from sqlite3 import Error

DB = "business_data.db"

cx_table_create = """create table if not exists customers (
    id integer primary key,
    name text not null,
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
    except OSError as e:
        print(f"{e}")
    finally:
        cur.close()


def customers_table(con, cx_table_create):
    con = sqlite3.connect(DB)
    try:
        cur = con.cursor()
        cur.execute(cx_table_create)

    except OSError as e:
        print(f"{e}")
    return con


def insert_customer(
    id, valid_cx, valid_addr, amount_paid, discount=bool
):  # built in id?
    # 0 or 1 if discount is true
    "add customer to db"
    q = "insert into customers (name,street,amount_paid) values (?,?,?)"
    data = (id, valid_cx, valid_addr, amount_paid, discount)
    query_exec(q, data)


def get_customer_name(name):
    "query customer names"
    q = "select * from customers where name = ?:"
    data = (name,)
    cur = query_exec(q, data)
    return cur.fetchall()


def close_connection(DB):
    con = None
    if con is True:
        con.close()


def backup_database():
    subprocess.run(["chmod", "+x", "backup.sh"])
    subprocess.run(["./backup.sh"])
