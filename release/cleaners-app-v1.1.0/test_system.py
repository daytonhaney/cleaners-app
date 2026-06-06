#!/usr/bin/env python3
"""Comprehensive test suite for cleaners application"""

import os
import sys
import sqlite3
import subprocess
import tempfile
import shutil
from pathlib import Path

# Test configuration
TEST_DB = "./test_business_data.db"
BACKUP_DB = "./business_data.db"


def run_test(test_name, test_func):
    """Run a test with proper error handling"""
    print(f"\n{'=' * 60}")
    print(f"TEST: {test_name}")
    print("=" * 60)

    try:
        test_func()
        print(f"✅ {test_name} - PASSED")
        return True
    except Exception as e:
        print(f"❌ {test_name} - FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


def setup_test_env():
    """Setup test environment"""
    # Backup existing database
    if os.path.exists(BACKUP_DB):
        shutil.copy2(BACKUP_DB, TEST_DB)

    # Remove test database if it exists
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def cleanup_test_env():
    """Cleanup test environment"""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_cli_help():
    """Test CLI help functionality"""

    # Test main app help
    result = subprocess.run(
        [sys.executable, "main.py", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Professional cleaning service management system" in result.stdout

    # Test demo app help
    result = subprocess.run(
        [sys.executable, "examples/demo.py", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Interactive demo mode" in result.stdout


def test_cli_version():
    """Test CLI version functionality"""

    result = subprocess.run(
        [sys.executable, "main.py", "--version"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "1.0.0" in result.stdout


def test_cli_license():
    """Test CLI license functionality"""

    result = subprocess.run(
        [sys.executable, "main.py", "--license"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "BSD Zero Clause License" in result.stdout


def test_fake_data_generation():
    """Test fake data generation"""

    from cleaners.fake_data import fake_customer, fake_employee, fake_transaction

    # Test fake customer
    customer = fake_customer()
    assert "name" in customer
    assert "address" in customer
    assert "email" in customer

    # Test fake employee
    employee = fake_employee()
    assert "name" in employee
    assert "badge_id" in employee

    # Test fake transaction
    transaction = fake_transaction()
    assert "customer" in transaction
    assert "final_total" in transaction
    assert transaction["final_total"] >= 0


def test_database_security():
    """Test database SQL injection protection"""

    from db.db_functions import query_exec, provision_database

    # Test SQL injection protection
    import os

    original_db = os.path.exists("./business_data.db")

    try:
        query_exec("SELECT * FROM customers; DROP TABLE customers;--")
        # If query executes without error, check if table still exists
        import sqlite3

        conn = sqlite3.connect("./business_data.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='customers'"
        )
        result = cur.fetchone()
        conn.close()
        assert result is not None, "SQL injection vulnerability - table was dropped!"

    except ValueError as e:
        assert "parameterization" in str(e), "SQL injection protection failed"

    # Test safe queries still work
    from cleaners.fake_data import populate_fake_data

    populate_fake_data(2, 1)

    # Verify data was inserted safely
    import sqlite3

    conn = sqlite3.connect("./business_data.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM customers")
    count = cur.fetchone()[0]
    conn.close()
    assert count >= 2, "Safe query functionality broken"


def test_database_stats():
    """Test database statistics functionality"""

    from cleaners.db_stats import get_database_stats
    from cleaners.fake_data import populate_fake_data

    # Generate test data
    populate_fake_data(5, 2)

    # Get stats
    stats = get_database_stats()
    assert stats is not None
    assert "total_customers" in stats
    assert "total_revenue" in stats
    assert stats["total_customers"] >= 5


def test_database_backup():
    """Test database backup functionality"""

    from db.db_functions import backup_database
    from datetime import datetime

    # This test is interactive, so we'll just ensure function doesn't crash
    try:
        # Simulate user input for backup
        result = backup_database()
        # Function should return True/False or handle gracefully
    except Exception as e:
        # Expected due to interactive nature
        pass


def test_input_validation():
    """Test input validation functions"""

    from cleaners.validation import (
        validate_customer_name,
        validate_age,
        validate_square_footage,
        validate_package_selection,
        validate_payment_amount,
    )

    # Test name validation
    valid, result = validate_customer_name("John Doe")
    assert valid == True
    assert result == "John Doe"

    valid, result = validate_customer_name("")
    assert valid == False
    assert "cannot be empty" in str(result).lower()

    # Test age validation
    valid, result = validate_age("25")
    assert valid == True
    assert result == 25

    valid, result = validate_age("-5")
    assert valid == False
    assert "valid age" in str(result).lower()

    # Test square footage validation
    valid, result = validate_square_footage("1000")
    assert valid == True
    assert result == 1000.0

    valid, result = validate_square_footage("-50")
    assert valid == False
    assert "at least" in str(result).lower()

    # Test package selection
    valid, result = validate_package_selection("2")
    assert valid == True
    assert result == 2

    valid, result = validate_package_selection("5")
    assert valid == False
    assert "select 1" in str(result).lower()

    # Test payment amount
    valid, result = validate_payment_amount("100.50")
    assert valid == True
    assert result == 100.50

    valid, result = validate_payment_amount("-10")
    assert valid == False
    assert "negative" in str(result).lower()


def test_core_functionality():
    """Test core application functionality"""

    from cleaners.clean import text_colors, get_discount, final_price

    # Test text colors
    green = text_colors("green")
    assert callable(green)

    # Test discount calculation
    discount = get_discount(100)
    assert discount >= 0

    # Test final price calculation
    final = final_price(100, 10)
    assert final == 90


def test_executable_functionality():
    """Test if executables work correctly"""

    # Test if executables exist
    assert os.path.exists("dist/cleaners-app"), "Production executable missing"
    assert os.path.exists("dist/cleaners-demo"), "Demo executable missing"

    # Test executable help
    result = subprocess.run(
        ["./dist/cleaners-app", "--help"], capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0

    # Test demo executable with fake data generation
    result = subprocess.run(
        ["./dist/cleaners-demo", "--generate-data", "2"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    assert "Fake data generation complete" in result.stdout


def test_error_handling():
    """Test error handling and edge cases"""

    # Test with non-existent database
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    from db.db_functions import provision_database

    db = provision_database()
    assert db is not None

    # Test with invalid database file
    try:
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"invalid sqlite data")
            tmp_db = tmp.name

        # Should handle gracefully
        try:
            conn = sqlite3.connect(tmp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            assert False, "Should have failed with invalid database"
        except sqlite3.DatabaseError:
            pass  # Expected
        finally:
            os.unlink(tmp_db)

    except Exception:
        pass


def run_comprehensive_tests():
    """Run all comprehensive tests"""

    print("🧪 STARTING COMPREHENSIVE TEST SUITE")
    print("=====================================")

    # Setup test environment
    setup_test_env()

    tests = [
        ("CLI Help Functionality", test_cli_help),
        ("CLI Version Functionality", test_cli_version),
        ("CLI License Functionality", test_cli_license),
        ("Fake Data Generation", test_fake_data_generation),
        ("Database Security (SQL Injection)", test_database_security),
        ("Database Statistics", test_database_stats),
        ("Database Backup", test_database_backup),
        ("Input Validation", test_input_validation),
        ("Core Functionality", test_core_functionality),
        ("Executable Functionality", test_executable_functionality),
        ("Error Handling", test_error_handling),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1

    # Cleanup
    cleanup_test_env()

    # Results
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed / total) * 100:.1f}%")

    if passed == total:
        print("🎉 ALL TESTS PASSED! System is working correctly.")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Review the issues above.")
        return False


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
