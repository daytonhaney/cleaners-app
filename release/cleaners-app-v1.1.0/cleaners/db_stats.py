#!/usr/bin/env python3
"""Database statistics functions for cleaning service demo"""

import sqlite3
from collections import defaultdict

DB = "./business_data.db"


def get_database_stats():
    """Get comprehensive database statistics"""

    if not sqlite3.connect(DB):
        return None

    stats = {
        "total_customers": 0,
        "total_employees": 0,
        "total_revenue": 0.0,
        "total_discounts": 0.0,
        "avg_transaction": 0.0,
        "customers_by_region": defaultdict(int),
        "recent_transactions": [],
        "top_customers": [],
        "revenue_by_month": defaultdict(float),
        "employee_regions": defaultdict(int),
    }

    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        # Customer statistics
        cur.execute("SELECT COUNT(*) FROM customers")
        stats["total_customers"] = cur.fetchone()[0]

        # Employee statistics
        cur.execute("SELECT COUNT(*) FROM employees")
        stats["total_employees"] = cur.fetchone()[0]

        # Revenue statistics
        cur.execute("SELECT SUM(amount_paid), SUM(discount) FROM customers")
        revenue_data = cur.fetchone()
        stats["total_revenue"] = revenue_data[0] or 0.0
        stats["total_discounts"] = revenue_data[1] or 0.0

        # Average transaction
        if stats["total_customers"] > 0:
            stats["avg_transaction"] = stats["total_revenue"] / stats["total_customers"]

        # Employee regions (get from employees table)
        cur.execute("SELECT region, COUNT(*) FROM employees GROUP BY region")
        for region, count in cur.fetchall():
            stats["employee_regions"][region] = count

        # Recent transactions (top 10)
        cur.execute("""
            SELECT name, address, amount_paid, discount,
                   (CASE WHEN amount_paid IS NULL THEN 0 ELSE amount_paid END) - 
                   (CASE WHEN discount IS NULL THEN 0 ELSE discount END) as final_total
            FROM customers 
            ORDER BY rowid DESC 
            LIMIT 10
        """)

        for row in cur.fetchall():
            stats["recent_transactions"].append(
                {
                    "name": row[0],
                    "address": row[1],
                    "amount_paid": row[2] or 0.0,
                    "discount": row[3] or 0.0,
                    "final_total": row[4],
                }
            )

        # Top customers by revenue
        cur.execute("""
            SELECT name, address, amount_paid, discount,
                   (CASE WHEN amount_paid IS NULL THEN 0 ELSE amount_paid END) - 
                   (CASE WHEN discount IS NULL THEN 0 ELSE discount END) as final_total
            FROM customers 
            WHERE amount_paid IS NOT NULL
            ORDER BY final_total DESC 
            LIMIT 5
        """)

        for row in cur.fetchall():
            stats["top_customers"].append(
                {
                    "name": row[0],
                    "address": row[1],
                    "amount_paid": row[2],
                    "discount": row[3] or 0.0,
                    "final_total": row[4],
                }
            )

        conn.close()

    except Exception as e:
        print(f"Error getting database stats: {e}")
        return None

    return stats


def display_database_stats():
    """Display formatted database statistics"""

    stats = get_database_stats()

    if not stats:
        print("No statistics available - database may be empty or inaccessible.")
        return

    print("\n" + "=" * 60)
    print("DATABASE STATISTICS")
    print("=" * 60)

    # Overview section
    print("\nOVERVIEW:")
    print("-" * 20)
    print(f"Total Customers: {stats['total_customers']}")
    print(f"Total Employees: {stats['total_employees']}")
    print(f"Total Revenue: ${stats['total_revenue']:,.2f}")
    print(f"Total Discounts: ${stats['total_discounts']:,.2f}")
    print(f"Average Transaction: ${stats['avg_transaction']:,.2f}")

    # Employee regions
    if stats["employee_regions"]:
        print(f"\nEMPLOYEES BY REGION:")
        print("-" * 25)
        for region, count in stats["employee_regions"].items():
            print(f"{region}: {count}")

    # Recent transactions
    if stats["recent_transactions"]:
        print(f"\nRECENT TRANSACTIONS (Top 10):")
        print("-" * 40)
        print(f"{'Customer':<20} {'Amount':<12} {'Discount':<10} {'Final':<10}")
        print("-" * 55)
        for trans in stats["recent_transactions"]:
            name = (
                trans["name"][:18] + ".." if len(trans["name"]) > 20 else trans["name"]
            )
            print(
                f"{name:<20} ${trans['amount_paid']:<11.2f} ${trans['discount']:<9.2f} ${trans['final_total']:<9.2f}"
            )

    # Top customers
    if stats["top_customers"]:
        print(f"\nTOP CUSTOMERS BY REVENUE:")
        print("-" * 35)
        for i, customer in enumerate(stats["top_customers"], 1):
            name = (
                customer["name"][:25] + ".."
                if len(customer["name"]) > 27
                else customer["name"]
            )
            print(f"{i}. {name:<27} ${customer['final_total']:>9.2f}")

    # Business insights
    print(f"\nBUSINESS INSIGHTS:")
    print("-" * 20)

    if stats["total_customers"] > 0:
        discount_rate = (
            (
                stats["total_discounts"]
                / (stats["total_revenue"] + stats["total_discounts"])
            )
            * 100
            if (stats["total_revenue"] + stats["total_discounts"]) > 0
            else 0
        )
        print(f"Discount Rate: {discount_rate:.1f}%")
        print(
            f"Average Discount per Customer: ${stats['total_discounts'] / stats['total_customers']:.2f}"
        )

    if stats["total_employees"] > 0:
        revenue_per_employee = stats["total_revenue"] / stats["total_employees"]
        print(f"Revenue per Employee: ${revenue_per_employee:,.2f}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    display_database_stats()
