# Cleaning Service Application

A Python console application for managing cleaning service transactions, customer information, and employee data with an interactive Rich-based UI.

## Features

- Customer management and transaction processing
- Employee information tracking
- Discount calculation and application
- SQLite database integration
- Rich text-based user interface
- Daily transaction summaries and reporting
- Database backup functionality

## Requirements

- Python 3.7 or higher

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cleaners-app
```

### 2. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

The application provides an interactive console interface for:
- Adding new customers
- Selecting cleaning packages
- Processing transactions with discounts
- Viewing employee information
- Generating daily summaries

## Database

Uses SQLite with automatic database creation (`business_data.db`). Tables:
- `customers` - Customer information and transactions
- `employees` - Employee details

## Project Structure

```
cleaners-app/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── cleaners/              # Main package
│   ├── clean.py          # Core logic
│   ├── fig.py            # Text formatting
│   └── rich_ui.py        # Rich UI components
└── db/                   # Database functions
    └── db_functions.py   # SQLite operations
```

## Dependencies

- `rich>=13.0.0` - Enhanced text UI
- `sqlite3` - Database (built-in)

## License
BSD Zero Clause License.

![ex](https://github.com/user-attachments/assets/a69f6def-5cc1-4ba4-84c4-80634d7e8ab5)
