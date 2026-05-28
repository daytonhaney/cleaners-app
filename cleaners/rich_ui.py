#!/usr/bin/env python3
"""Cleaning Service Rich UI components"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.columns import Columns
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, IntPrompt
from rich import box
import time

console = Console()


def rich_title():
    """Display the application title with Rich styling"""
    title_text = """
[bold cyan]     ___          ___      ___        _   [/bold cyan]
[bold cyan]    |_ _|_ __    ( _ )    / _ \\ _   _| |_ [/bold cyan]
[bold cyan]     | || '_ \\   / _ \\/\\ | | | | | | | __|[/bold cyan]
[bold cyan]     | || | | | | (_>  < | |_| | |_| | |_ [/bold cyan]
[bold cyan]    |___|_| |_|  \\___/\\/  \\___/ \\__,_|\\__|[/bold cyan]
[bold green]      ____ _                  _                ____                  [/bold green]
[bold green]     / ___| | ___  __ _ _ __ (_)_ __   __ _   / ___|___  _ __ _ __   [/bold green]
[bold green]    | |   | |/ _ \\/ _` | '_ \\| | '_ \\ / _` | | |   / _ \\| '__| '_ \\  [/bold green]
[bold green]    | |___| |  __/ (_| | | | | | | | | (_| | | |__| (_) | |  | |_) | [/bold green]
[bold green]     \\____|_|\\___|\\__,_|_| |_|_|_| |_|\\__, |  \\____\\___/|_|  | .__(_) [/bold green]
[bold green]                                  |___/                  |_|     [/bold green]
"""

    panel = Panel(
        title_text, box=box.ROUNDED, border_style="bright_blue", padding=(1, 2)
    )
    console.print(panel)
    console.print()


def rich_employee_info(employee_list):
    """Display employee information in a Rich table"""
    if not employee_list:
        return

    table = Table(
        title="[bold green]Employee Information[/bold green]", box=box.ROUNDED
    )
    table.add_column("Field", style="cyan", width=15)
    table.add_column("Value", style="white")

    for emp in employee_list:
        name, date, region, badge_id = emp
        table.add_row("Name", name)
        table.add_row("Date", date)
        table.add_row("Region", region)
        table.add_row("Badge ID", badge_id)
        table.add_row("", "")  # Empty row for spacing

    console.print(table)
    console.print()


def rich_package_selection():
    """Display cleaning packages in a Rich table"""
    table = Table(title="[bold yellow]Cleaning Packages[/bold yellow]", box=box.DOUBLE)
    table.add_column("Select", style="magenta", justify="center", width=8)
    table.add_column("Package", style="cyan", justify="center", width=12)
    table.add_column("Services", style="white", width=30)
    table.add_column("Price", style="green", justify="right", width=10)

    table.add_row(
        "[bold]1[/bold]", "Regular", "General-Tidying, Sweep, Dust, Mop", "$100.00"
    )
    table.add_row(
        "[bold]2[/bold]",
        "Premium",
        "Regular Service+, Bathrooms, Closets, Laundry",
        "$200.00",
    )
    table.add_row(
        "[bold]3[/bold]", "Outdoor", "Mowing, Weed-Wack, Shrubs, Leaves", "$300.00"
    )

    console.print(table)

    # Display discount info
    discount_panel = Panel(
        "[bold green]Age 65+ 15% Discount Applied![/bold green]",
        box=box.ROUNDED,
        border_style="green",
    )
    console.print(discount_panel)

    console.print("[yellow]Labor Charge: $0.15 per square foot[/yellow]")
    console.print()


def rich_customer_input(prompt_text):
    """Get customer input using Rich prompt"""
    try:
        return Prompt.ask(prompt_text)
    except (EOFError, KeyboardInterrupt):
        # Fallback for non-interactive environments
        import sys

        if not sys.stdin.isatty():
            return input(prompt_text + " ")
        raise



def rich_int_input(prompt_text):
    """Get integer input using Rich prompt"""
    try:
        return IntPrompt.ask(prompt_text)
    except (EOFError, KeyboardInterrupt):
        # Fallback for non-interactive environments
        import sys

        if not sys.stdin.isatty():
            try:
                return int(input(prompt_text + " "))
            except ValueError:
                return None
        raise
    except:
        return None


def rich_area_input():
    """Get area measurements with Rich styling"""
    try:
        console.print("[cyan]Measure Length and width of exterior for price[/cyan]")

        while True:
            try:
                length = float(Prompt.ask("Length"))
                width = float(Prompt.ask("Width"))
                area = length * width
                console.print(f"[green]Area: {area:.2f} square feet[/green]")
                return length, width, area
            except ValueError:
                console.print("[red]Please enter valid numbers[/red]")
    except (EOFError, KeyboardInterrupt):
        # Fallback for non-interactive environments
        import sys

        if not sys.stdin.isatty():
            try:
                length = float(input("Length: "))
                width = float(input("Width: "))
                area = length * width
                print(f"Area: {area:.2f} square feet")
                return length, width, area
            except ValueError:
                print("Please enter valid numbers")
                return None, None, None
        raise


def rich_transaction_summary(package_name, package_price, area, labor_cost, total):
    """Display transaction summary with Rich styling"""

    summary_table = Table(box=box.ROUNDED, show_header=False)
    summary_table.add_column("Item", style="cyan")
    summary_table.add_column("Amount", style="white", justify="right")

    summary_table.add_row("Package", f"{package_name}")
    summary_table.add_row("Package Price", f"${package_price:.2f}")
    summary_table.add_row("Area", f"{area:.2f} sq ft")
    summary_table.add_row("Labor Cost", f"${labor_cost:.2f}")
    summary_table.add_row("", "")  # Separator
    summary_table.add_row("[bold]Subtotal[/bold]", f"[bold]${total:.2f}[/bold]")

    console.print(
        Panel(
            summary_table,
            title="[bold green]Transaction Summary[/bold green]",
            box=box.ROUNDED,
            border_style="green",
        )
    )
    console.print()


def rich_discount_applied(discount_amount):
    """Display discount information"""
    discount_table = Table(box=box.ROUNDED, show_header=False)
    discount_table.add_column("Item", style="cyan")
    discount_table.add_column("Amount", style="green", justify="right")

    discount_table.add_row("Discount Applied", f"${discount_amount:.2f}")

    console.print(
        Panel(
            discount_table,
            title="[bold green]Discount Information[/bold green]",
            box=box.ROUNDED,
            border_style="green",
        )
    )


def rich_final_total(final_amount):
    """Display final total with emphasis"""
    panel = Panel(
        f"[bold green blink]Final Total: ${final_amount:.2f}[/bold green blink]",
        box=box.DOUBLE,
        border_style="green",
        padding=(1, 2),
    )
    console.print(panel)
    console.print()


def rich_customer_daily_summary(customers_data: object) -> None:
    """Display daily customer summary in a Rich table"""
    if not customers_data:
        console.print("[yellow]No customers processed today[/yellow]")
        return

    table = Table(
        title="[bold blue]Today's Customer Summary[/bold blue]", box=box.DOUBLE
    )
    table.add_column("Customer Name", style="cyan", width=20)
    table.add_column("Address", style="white", width=25)
    table.add_column("Discount", style="yellow", width=15)
    table.add_column("Total", style="green", justify="right", width=15)

    total_earnings = 0

    for customer in customers_data:
        name, address, discount, total = customer
        table.add_row(name, address, str(discount), f"${total:.2f}")
        total_earnings += total

    console.print(table)

    # Display total earnings
    earnings_panel = Panel(
        f"[bold green blink]Cash Earned: ${total_earnings:.2f}[/bold green blink]",
        box=box.DOUBLE,
        border_style="green",
        padding=(1, 2),
    )
    console.print(earnings_panel)


def rich_loading(message="Processing..."):
    """Show a loading spinner"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(message, total=None)
        time.sleep(1)  # Simulate processing


def rich_error(message):
    """Display error message"""
    console.print(f"[red]Error: {message}[/red]")


def rich_success(message):
    """Display success message"""
    console.print(f"[green]✓ {message}[/green]")


def rich_info(message):
    """Display info message"""
    console.print(f"[blue]ℹ {message}[/blue]")


def rich_warning(message):
    """Display warning message"""
    console.print(f"[yellow]⚠ {message}[/yellow]")


def rich_separator():
    """Print a decorative separator"""
    console.print("=" * console.width)


def rich_newlines(count=2):
    """Print multiple newlines"""
    console.print("\n" * (count - 1))
