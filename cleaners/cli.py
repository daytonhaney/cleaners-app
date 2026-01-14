#!/usr/bin/env python3
"""Command-line interface for cleaners application"""

import argparse
import sys
import os
from pathlib import Path

# Version information
try:
    from importlib.metadata import version

    VERSION = version("cleaners-app")
except ImportError:
    VERSION = "1.0.0"
LICENSE_TEXT = """
BSD Zero Clause License

Copyright (c) 2024 Miguel

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""


def print_man_page():
    """Display the man page content"""
    man_file = Path(__file__).parent / "cleaners-app.1"

    if man_file.exists():
        with open(man_file, "r") as f:
            content = f.read()

        # Check if less command is available
        if os.system("command -v less >/dev/null 2>&1") == 0:
            try:
                os.system(f"less '{man_file}'")
                return
            except:
                pass

        # Fallback: print to stdout
        print(content)
    else:
        print("Man page not found.")
        sys.exit(1)


def handle_main_args():
    """Handle command-line arguments for main application"""
    parser = argparse.ArgumentParser(
        prog="cleaners-app",
        description="Professional cleaning service management system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run production application
  %(prog)s --help             # Show this help message
  %(prog)s --version          # Show version information
  %(prog)s --license          # Show license information

Files:
  ./business_data.db          # SQLite database
  ./app.py                   # Production entry point
  ./examples/demo.py         # Demo entry point

For more information, run: %(prog)s --man
        """,
    )

    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s {VERSION}"
    )
    parser.add_argument(
        "--license", action="store_true", help="Show license information and exit"
    )
    parser.add_argument(
        "--man", action="store_true", help="Display manual page and exit"
    )

    return parser.parse_args()


def handle_demo_args():
    """Handle command-line arguments for demo application"""
    parser = argparse.ArgumentParser(
        prog="cleaners-demo",
        description="Interactive demo mode with fake data generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Run interactive demo
  %(prog)s --help                    # Show this help message
  %(prog)s --version                 # Show version information
  %(prog)s --generate-data 25        # Generate 25 fake customers
  %(prog)s --demo-stats               # Show database statistics
  %(prog)s --man                     # Display manual page
        """,
    )

    parser.add_argument(
        "--version", "-v", action="version", version=f"%(prog)s {VERSION}"
    )
    parser.add_argument(
        "--license", action="store_true", help="Show license information and exit"
    )
    parser.add_argument(
        "--man", action="store_true", help="Display manual page and exit"
    )
    parser.add_argument(
        "--generate-data",
        nargs="?",
        const=10,
        type=int,
        metavar="COUNT",
        help="Generate fake data (default: 10 customers)",
    )
    parser.add_argument(
        "--demo-stats",
        action="store_true",
        help="Show database statistics without interactive menu",
    )

    return parser.parse_args()


def process_args(mode="main"):
    """Process command-line arguments based on mode"""

    if mode == "main":
        args = handle_main_args()

        if args.license:
            print("Cleaners App License")
            print("=" * 40)
            print(LICENSE_TEXT)
            sys.exit(0)

        elif args.man:
            print_man_page()
            sys.exit(0)

    elif mode == "demo":
        args = handle_demo_args()

        if args.license:
            print("Cleaners App License")
            print("=" * 40)
            print(LICENSE_TEXT)
            sys.exit(0)

        elif args.man:
            print_man_page()
            sys.exit(0)

        elif args.generate_data is not None:
            from cleaners.fake_data import populate_fake_data
            from db.db_functions import provision_database

            print(f"Generating {args.generate_data} fake customers and employees...")
            provision_database()
            populate_fake_data(args.generate_data, max(3, args.generate_data // 3))
            print("Fake data generation complete!")
            sys.exit(0)

        elif args.demo_stats:
            from cleaners.db_stats import display_database_stats

            display_database_stats()
            sys.exit(0)

    return None


if __name__ == "__main__":
    # Test CLI functionality
    print("Cleaners App CLI Module")
    print("This module provides command-line argument handling.")
    print("Use through app.py or examples/demo.py")
