#!/usr/bin/env python3
"""Fake data generator for cleaning service app"""

from faker import Faker
import random

# Initialize Faker with US locale
fake = Faker("en_US")

# Cleaning service specific data
CLEANING_SERVICES = [
    "Regular House Cleaning",
    "Deep Cleaning",
    "Post-Construction Cleanup",
    "Carpet Cleaning",
    "Window Washing",
    "Office Cleaning",
    "Move-in/Move-out Cleaning",
    "Kitchen Deep Clean",
    "Bathroom Sanitization",
    "Dusting and Polishing",
]

REGIONS = [
    "Sierra Nevada",
    "Lake Tahoe",
    "Reno Area",
    "Carson City",
    "Sparks",
    "Incline Village",
]


def fake_customer():
    """Generate fake customer data"""
    return {
        "name": fake.name(),
        "address": fake.street_address(),
        "phone": fake.phone_number(),
        "email": fake.email(),
    }


def fake_employee():
    """Generate fake employee data"""
    first_name = fake.first_name()
    last_name = fake.last_name()
    return {
        "name": f"{first_name} {last_name}",
        "address": fake.street_address(),
        "phone": fake.phone_number(),
        "badge_id": fake.bothify("????-###"),
        "region": random.choice(REGIONS),
    }


def fake_service_selection():
    """Generate fake service selection"""
    num_services = random.randint(1, 4)
    selected = random.sample(CLEANING_SERVICES, num_services)

    services = []
    for service in selected:
        # Fake dimensions based on service type
        if "Carpet" in service:
            length = random.uniform(100, 2000)  # sq ft
            width = 1  # per sq ft pricing
        elif "Window" in service:
            length = random.randint(5, 50)  # number of windows
            width = 1  # per window pricing
        else:
            length = random.uniform(500, 3000)  # sq ft
            width = 1  # per sq ft pricing

        services.append({"service": service, "length": length, "width": width})

    return services


def fake_transaction():
    """Generate complete fake transaction"""
    customer = fake_customer()
    services = fake_service_selection()

    # Calculate total (simplified pricing)
    total = 0
    for service in services:
        if "Regular" in service["service"]:
            price = 0.15 * service["length"]  # $0.15 per sq ft
        elif "Deep" in service["service"]:
            price = 0.35 * service["length"]  # $0.35 per sq ft
        elif "Carpet" in service["service"]:
            price = 0.25 * service["length"]  # $0.25 per sq ft
        elif "Window" in service["service"]:
            price = 15 * service["length"]  # $15 per window
        else:
            price = 0.20 * service["length"]  # $0.20 per sq ft

        total += price

    # Apply discount randomly
    discount_percent = random.choice([0, 0, 0, 10, 15, 20])  # 40% chance of discount
    discount_amount = total * (discount_percent / 100)
    final_total = total - discount_amount

    return {
        "customer": customer,
        "services": services,
        "subtotal": round(total, 2),
        "discount_percent": discount_percent,
        "discount_amount": round(discount_amount, 2),
        "final_total": round(final_total, 2),
        "date": fake.date_time_this_year(),
    }


def populate_fake_data(num_customers=10, num_employees=5):
    """Populate database with fake data"""
    from db.db_functions import insert_employee, insert_cust_totals, provision_database

    # Ensure database is provisioned
    provision_database()

    print(f"Generating {num_employees} fake employees...")
    for i in range(num_employees):
        emp = fake_employee()
        insert_employee(emp["name"], emp["address"], emp["region"], emp["badge_id"])
        print(f"  - {emp['name']} - {emp['region']} - Badge: {emp['badge_id']}")

    print(f"\nGenerating {num_customers} fake customers and transactions...")
    for i in range(num_customers):
        transaction = fake_transaction()
        customer = transaction["customer"]

        # Insert customer data
        insert_cust_totals(
            customer["name"],
            customer["address"],
            transaction["discount_amount"],
            transaction["final_total"],
        )

        services_desc = ", ".join([s["service"] for s in transaction["services"]])
        print(
            f"  - {customer['name']} - ${transaction['final_total']} - {services_desc}"
        )

    print(f"\nFake data generation complete!")
    print(f"   Added {num_customers} customers and {num_employees} employees")


if __name__ == "__main__":
    # Demo the fake data generator
    print("Fake Cleaning Service Data Demo")
    print("=" * 50)

    # Generate sample data
    print("\nSample Customer:")
    customer = fake_customer()
    for key, value in customer.items():
        print(f"  {key.title()}: {value}")

    print("\nSample Employee:")
    employee = fake_employee()
    for key, value in employee.items():
        print(f"  {key.title()}: {value}")

    print("\nSample Transaction:")
    transaction = fake_transaction()
    print(f"  Customer: {transaction['customer']['name']}")
    print(f"  Services: {[s['service'] for s in transaction['services']]}")
    print(f"  Subtotal: ${transaction['subtotal']}")
    if transaction["discount_percent"] > 0:
        print(
            f"  Discount: {transaction['discount_percent']}% (${transaction['discount_amount']})"
        )
    print(f"  Final Total: ${transaction['final_total']}")
    print(f"  Date: {transaction['date'].strftime('%Y-%m-%d %H:%M')}")
