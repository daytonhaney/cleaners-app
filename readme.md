# CleanersApp - Cleaning Service Management


A comprehensive application for managing cleaning service transactions, customer information, and employee data with an interactive Rich-based UI.

## Features

- Customer management and transaction processing
- Employee information tracking
- Discount calculation and application
- SQLite database integration
- Rich text-based user interface
- Daily transaction summaries and reporting
- Database backup functionality

# Installation Options

### Option 1: Quick Start (Recommended for End Users)

**Download the Executable - No Installation Required!**

1. Go to [Releases](https://github.com/daytonhaney/cleaners-app/releases)
2. Download `CleanersApp.exe` (Windows) or `CleanersApp` (Linux/Mac)
3. Double-click to run - nothing to install!

### Option 2: Manual Setup (For Developers)

#### Step 1: Clone Repository
```bash
git clone https://github.com/daytonhaney/cleaners-app.git
cd cleaners-app
```

#### Step 2: Create and Activate Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
May need to -
$chmod u+x CleanersApp if on linux to run from terminal


#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### For End Users (Executable)
1. **Windows**: Double-click `CleanersApp.exe` or run from Command Prompt:
   ```cmd
   CleanersApp.exe
   ```
2. **Linux/Mac**: Run from terminal:
   ```bash
   ./CleanersApp
   ``
   `

### For Developers (Source Code)
```bash
python main.py
```

The application provides an interactive console interface for:
- Adding new customers
- Selecting cleaning packages (Regular, Premium, Outdoor)
- Processing transactions with senior discounts
- Viewing employee information
- Generating daily summaries
- Automatic database creation and backup

## System Requirements

### For Executable Version
- **Windows 7+** (Windows 10/11 recommended)
- **Linux** (Ubuntu 18.04+, CentOS 7+, etc.)
- **macOS** (10.14+)
- **No Python installation required**
- **No additional dependencies**

### For Source Code Version
- **Python 3.7+** (3.8+ recommended)
- **2GB+ RAM**
- **50MB+ disk space**

## Database

Uses SQLite with automatic database creation (`business_data.db`). The database is created automatically when you first run the app.

**Tables:**
- `customers` - Customer information and transactions
- `employees` - Employee details

**Backup**: Automatic backup when exiting the application

## Database

Uses SQLite with automatic database creation (`business_data.db`). Tables:
- `customers` - Customer information and transactions
- `employees` - Employee details

## Package Pricing

| Package | Services | Price |
|----------|-----------|--------|
| **[1] Regular** | General-Tidying, Sweep, Dust, Mop | $100.00 |
| **[2] Premium** | Regular Service+, Bathrooms, Closets, Laundry | $200.00 |
| **[3] Outdoor** | Mowing, Weed-Wack, Shrubs, Leaves | $300.00 |

### Discounts & Labor
- **15% discount** for customers 65+
- **Labor charge**: $0.15 per square foot
- **Package selection**: Enter 1, 2, or 3

## Project Structure

```
cleaners-app/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── setup.py              # Package configuration
├── LICENSE               # BSD Zero Clause License
├── cleaners/              # Main application package
│   ├── clean.py          # Core business logic
│   ├── fig.py            # Text formatting utilities
│   ├── rich_ui.py        # Rich UI components
│   ├── config.py         # Configuration management
│   └── validation.py     # Input validation
└── db/                   # Database layer
    └── db_functions.py   # SQLite operations
```

## Dependencies

**Executable Version**: All dependencies are bundled - nothing to install!

**Source Code Version**:
- `rich>=13.0.0` - Enhanced text UI
- `sqlite3` - Database (built-in to Python)

## Getting Started Video Tutorial

[Coming Soon] - Quick setup and usage walkthrough

## Troubleshooting

### Windows Users
**Problem**: "Windows protected your PC"
**Solution**: Click "More info" → "Run anyway" - this is normal for new executables

**Problem**: "Application won't start"
**Solution**: Right-click → "Run as administrator"

**Problem**: Missing database
**Solution**: Database is created automatically on first run

### All Users
**Problem**: App crashes
**Solution**: 
1. Check if enough disk space
2. Run with administrator privileges
3. Contact support: jpp@iocleaning.com

## Support

- **Email**: jpp@iocleaning.com
- **Issues**: [GitHub Issues](https://github.com/daytonhaney/cleaners-app/issues)
## License

BSD Zero Clause License - Free for commercial and personal use.

![ex](https://github.com/user-attachments/assets/a69f6def-5cc1-4ba4-84c4-80634d7e8ab5)
