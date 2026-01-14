#!/usr/bin/env python3
"""Cleaning Service Demo Mode - For testing and fun with fake data"""

import sys
from cleaners.cli import process_args
from cleaners.clean import (
    text_colors,
    display_customer_info,
)
from cleaners.fig import io_figlets, io_figlets_title
from cleaners.fake_data import populate_fake_data, fake_transaction
from cleaners.db_stats import display_database_stats
from db.db_functions import provision_database, get_customer_name

# Import Rich UI for main title
try:
    from cleaners.rich_ui import rich_title, rich_newlines, rich_success, rich_info

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def demo_menu():
    """Demo mode menu"""
    success = text_colors("green")
    info = text_colors("cyan")

    while True:
        print("\n" + "=" * 50)
        print("CLEANING SERVICE DEMO MODE")
        print("=" * 50)
        print("1. Generate Fake Customers & Employees")
        print("2. Show Sample Fake Transaction")
        print("3. View Current Database Stats")
        print("4. Clear Database & Start Fresh")
        print("5. Exit Demo Mode")
        print("=" * 50)

        try:
            choice = input("Select an option (1-5): ").strip()

            if choice == "1":
                print("\nGenerating fake data...")
                num_customers = input(
                    "How many customers to generate? (default 10): "
                ).strip()
                num_employees = input(
                    "How many employees to generate? (default 5): "
                ).strip()

                num_customers = int(num_customers) if num_customers.isdigit() else 10
                num_employees = int(num_employees) if num_employees.isdigit() else 5

                populate_fake_data(num_customers, num_employees)
                if RICH_AVAILABLE:
                    rich_success(
                        f"Generated {num_customers} customers and {num_employees} employees!"
                    )
                else:
                    print(
                        success(
                            f"Generated {num_customers} customers and {num_employees} employees!"
                        )
                    )

            elif choice == "2":
                print("\nSample Fake Transaction:")
                print("-" * 30)
                transaction = fake_transaction()

                if RICH_AVAILABLE:
                    rich_info(f"Customer: {transaction['customer']['name']}")
                    rich_info(f"Email: {transaction['customer']['email']}")
                    rich_info(f"Address: {transaction['customer']['address']}")
                    rich_info(
                        f"Services: {', '.join([s['service'] for s in transaction['services']])}"
                    )
                    rich_info(f"Subtotal: ${transaction['subtotal']}")
                    if transaction["discount_percent"] > 0:
                        rich_info(
                            f"Discount: {transaction['discount_percent']}% (-${transaction['discount_amount']})"
                        )
                    rich_info(f"Final Total: ${transaction['final_total']}")
                    rich_info(f"Date: {transaction['date'].strftime('%Y-%m-%d %H:%M')}")
                else:
                    print(f"Customer: {transaction['customer']['name']}")
                    print(f"Email: {transaction['customer']['email']}")
                    print(f"Address: {transaction['customer']['address']}")
                    print(
                        f"Services: {', '.join([s['service'] for s in transaction['services']])}"
                    )
                    print(f"Subtotal: ${transaction['subtotal']}")
                    if transaction["discount_percent"] > 0:
                        print(
                            f"Discount: {transaction['discount_percent']}% (-${transaction['discount_amount']})"
                        )
                    print(f"Final Total: ${transaction['final_total']}")
                    print(f"Date: {transaction['date'].strftime('%Y-%m-%d %H:%M')}")

            elif choice == "3":
                display_database_stats()

            elif choice == "4":
                confirm = (
                    input("This will delete all data. Are you sure? (yes/no): ")
                    .strip()
                    .lower()
                )
                if confirm == "yes":
                    import os

                    if os.path.exists("./business_data.db"):
                        os.remove("./business_data.db")
                        print("Database cleared!")
                        # Recreate fresh database
                        provision_database()
                    else:
                        print("No database to clear.")
                else:
                    print("Database clear cancelled.")

            elif choice == "5":
                print("Thanks for using Cleaning Service Demo!")
                break

            else:
                print("Invalid choice. Please select 1-5.")

        except KeyboardInterrupt:
            print("\nDemo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Demo mode main function"""

    # Process command-line arguments first
    result = process_args("demo")
    if result is not None:  # CLI args were processed, exit if needed
        return

    # Ensure database exists
    check_db = provision_database()
    if not check_db:
        print("Failed to initialize database!")
        return

    # Display title using Rich if available, otherwise fallback
    if RICH_AVAILABLE:
        rich_title()
        rich_newlines(1)
    else:
        title = io_figlets(io_figlets_title)

    print("\nWelcome to CLEANING SERVICE DEMO MODE!")
    print("This is a fun testing environment with fake data generation.")
    print("Use regular main.py for production use.\n")

    demo_menu()


if __name__ == "__main__":
    main()
