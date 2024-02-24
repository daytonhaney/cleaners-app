#!/usr/bin/env python3

import re
from datetime import datetime
from sqlite3 import Error
from time import sleep, time

###############################################################################
## IO Cleaners Service                                                        #
###############################################################################

total_services = {
    "Regular": "General-Tidying, Sweep, Dust, Mop",
    "Premium": "Regular Service+, Bathrooms, Closets, Laundry",
    "Outdoor": "Mowing, Weed-Wack, Shrubs, Leaves",
}


def get_employees():
    """get employees"""

    employee_list = []

    print("\nManager:")
    name = "Cam Poe"
    date = datetime.now().strftime("%A, %d, %B %Y %I:%M%p")
    address = "12 Pinball Road"
    region = "Sierra Nevada"
    badge_id = "JB3HBIRD"
    employee = (
        name,
        date,
        region,
        badge_id,
    )

    for i in name, date, address, region, badge_id:
        print(i)
    print("")

    db_path = "./business_data.db"
    if os.path.isfile(db_path):
        if e_table_exists(DB, emp_table):
            insert_employee(name, address, region, badge_id)
    elif not os.path.isfile(db_path):
        pass

    employee_list.append(employee)
    return employee_list


p = lambda p: print(p)  # p("debug")


def new_customer():
    """get customers"""

    discount = int
    addr = ""
    age = ""
    valid_name = False

    name = input("Name: <Enter> to exit  \t")
    fname = name.replace(" ", "")

    if fname.isalpha():
        name = name.title()
        valid_name = True

        age = input("Age: \t")
        if age.isalpha() is True:
            print("Error, numbers only")
            age = input("Age: \t")
            age = age.replace(" ", "")
            # added incase input chars in age
            age1 = re.findall(r"\b\d+\b", age)
            age = age1[0]

        if int(64) < int(age) < int(999):
            discount = 1, True
            print("applying discounts...!")
            sleep(0.5)
            cash = text_colors("green")
            print(cash("-15%"), "discount applied!")

        else:
            discount = 0, False

        address = input("Enter address: \t")
        addr = address.capitalize()
    return name, valid_name, discount, addr


def banner():
    """ui"""

    b = "=" * 78
    print(b)


def text_colors(color):
    """ui"""

    colors = {"RESET": "\033[m", "RED": "\033[31m", "GREEN": "\033[32m"}

    def text(text):
        c = colors.get(color.upper(), "")
        return f"{c}{text}{colors['RESET']}"

    return text


def user_interface():
    """ui"""

    io_figlets()
    cash = text_colors("green")
    for display1 in [
        ["Regular:", "Premium:", "Outdoor:"],
        ["Room Clean", "Regular +", "Mow"],
    ]:
        print("\n{:>20}{:>20}{:>20}".format(*display1))

    for display2 in [
        ["Dust", "Bathrooms", "Weed-Wack"],
        ["Sweep", "Closets", "Shrubs"],
    ]:
        print("{:>20}{:>20}{:>20}".format(*display2))

    for display3 in ["Mop", "Laundry", "Leaves"], [
        cash("\t\t$100"),
        cash("\t  $200"),
        cash("\t\t$300"),
    ]:
        print("{:>20}{:>20}{:>20}".format(*display3))
    print("")

    d = "Age 65+ 15% Discount"
    d_banner = d.center(70)
    print(d_banner)
    banner()
    banner()
    package = "Cleaning packages..."
    package_banner = package.center(53)

    print(f"\t{package_banner}\n ")
    print(
        "\n1.Regular Package ---> $100.00",
        "\n",
        total_services["Regular"],
    )
    print(
        "\n2.Premium Package ---> $200.00",
        "\n",
        total_services["Premium"],
    )
    print(
        "\n3.Outdoor Package ---> $300.00",
        "\n",
        total_services["Outdoor"],
    )
    print("")
    print("$.15 per square foot of house is charged for labor\n")
    print("Chose cleaning package...")


def cust_selection():
    """customer selections"""

    service_selection = int(
        input(
            """
    Press ---[1]---> Regular\n 
    Press ---[2]---> Premium\n
    Press ---[3]---> Outdoor\n
    """
        )
    )

    if service_selection == 1:
        return service_selection

    if service_selection == 2:
        return service_selection

    if service_selection == 3:
        return service_selection

    else:
        if service_selection != 1 or service_selection != 2 or service_selection != 3:
            print("Error")
            print("Enter 1 2 or 3")
            return cust_selection()


def customer_transaction(selection, discount):
    """sum of area and labor charge added to price from LIST_PRICE"""

    LIST_PRICE = [100.00, 200.00, 300.00]
    totals = []
    cash = text_colors("green")

    if selection == int(1):
        print(f"Customer selects:\n{total_services['Regular']}", cash("$100.00"), "\n")
        sleep(0.5)
        print("Measure Length and width of exterior for price")
        l = float(input("Length: \t"))
        w = float(input("Width: \t"))
        area = l * w
        labor = labor_charge(area)
        s = LIST_PRICE[0]
        r_total_before_discount = price_per_house(s, labor)
        totals.append(r_total_before_discount)

    elif selection == int(2):
        print(f"Customer selects:\n {total_services['Premium']}", cash("$200.00"), "\n")
        print("Measure Length and width of exterior for price")
        l = float(input("Length: \t"))
        w = float(input("Width: \t"))
        premium_area = l * w
        labor2 = (lambda area: (area) * 0.15)(premium_area)
        print("area for pre = ", premium_area)
        s2 = LIST_PRICE[1]
        p_total_before_discount = price_per_house(s2, labor2)
        totals.append(p_total_before_discount)

    elif selection == int(3):
        print(f"Customer selects:\n {total_services['Outdoor']}", cash("$300.00"), "\n")
        print("Measure Length and width of exterior for price")
        l = int(input("Length: \t"))
        w = int(input("Width: \t"))
        outdoor_area = l * w
        outdoor_labor = labor_charge(outdoor_area)
        s3 = LIST_PRICE[2]
        o_total_before_discount = price_per_house(s3, outdoor_labor)
        totals.append(o_total_before_discount)
    return totals


def price_per_house(selection, labor):
    """sets vars for sum of labor and selection from list_price"""
    LIST_PRICE = [100.00, 200.00, 300.00]
    cash = text_colors("green")

    if selection == LIST_PRICE[0]:
        total = selection + labor
        reg_before_discount = total
        print("{:.2f}".format(float(reg_before_discount)))
        cash(reg_before_discount)
        return reg_before_discount

    elif selection == LIST_PRICE[1]:
        total = selection + labor
        prem_before_discount = total
        print("{:.2f}".format(float(prem_before_discount)))
        cash(prem_before_discount)
        return prem_before_discount

    elif selection == LIST_PRICE[2]:
        total = selection + labor
        out_before_discount = total
        print("{:.2f}".format(float(out_before_discount)))
        cash(out_before_discount)
        return out_before_discount


def get_discount(total):
    """calculate discount"""

    dis = total * (15 / 100)
    print("getting discount...")
    return dis


def labor_charge(area):
    """calculate labor"""

    labor = area * 0.15
    cash = text_colors("green")
    print(cash("labor: "), labor)
    return labor


def final_price(reg_price=0, discount=0):
    """get final price"""

    final_discount_price = reg_price - discount
    return final_discount_price


def display_customer_info(c_names, c_address, c_discounts, c_totals):
    """print daily info + cash flow"""
    p("\n")
    len_cust = len(c_names)
    p("{:<15}{:>51}".format("*** Todays Customer Info...", "Store ID: 3214"))
    print("\n")

    print(
        "{:<20}\t{:<20}\t{:<20}\t{:<10}".format(
            "Name",
            "Address",
            "Discount",
            "Total Cost",
        )
    )
    print(
        "{:<20}\t{:<20}\t{:<20}\t{:<20}".format(
            "_______________",
            "_______________",
            "_____________",
            "_____________",
        )
    )
    i = 0
    while i < len_cust:
        print(
            "{:<20}\t{:<20}\t{:<20}\t{:<20}".format(
                c_names[i],
                c_address[i],
                str(c_discounts[i]),
                round(c_totals[i], 2),
            )
        )
        print("")
        i = i + 1
    i = 0
    # todays_total = sum(subtotals for sublists in c_totals for subtotals in sublists)

    print("\n")
    tt = "{:.2f}".format(c_totals[-1])
    print("{:<80}".format("Cash earned: "))
    print("{:<80}".format("-------------"))
    print("$", tt)


def io_figlets():
    """vanilla py"""

    io_figlets = [
        """
     ___          ___      ___        _   
    |_ _|_ __    ( _ )    / _ \ _   _| |_ 
     | || '_ \   / _ \/\ | | | | | | | __|
     | || | | | | (_>  < | |_| | |_| | |_ 
    |___|_| |_|  \___/\/  \___/ \__,_|\__|
                                      
      ____ _                  _                ____                  
     / ___| | ___  __ _ _ __ (_)_ __   __ _   / ___|___  _ __ _ __   
    | |   | |/ _ \/ _` | '_ \| | '_ \ / _` | | |   / _ \| '__| '_ \  
    | |___| |  __/ (_| | | | | | | | | (_| | | |__| (_) | |  | |_) | 
     \____|_|\___|\__,_|_| |_|_|_| |_|\__, |  \____\___/|_|  | .__(_)
                                      |___/                  |_|     
    """
    ]
    print(io_figlets[-1])


################################################################################
## database stuff                                                              #
################################################################################


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


################################################################################
## main                                                                        #
################################################################################


import os.path
from datetime import datetime


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

    display_customer_info(c_names, c_address, c_discounts, c_totals)
    backup_database()


main()
