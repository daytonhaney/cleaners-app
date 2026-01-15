# Cleaners App

A cleaning service management system for processing customer transactions, managing employee data, and generating daily summaries.

![ex](https://github.com/user-attachments/assets/a69f6def-5cc1-4ba4-84c4-80634d7e8ab5)

## Installation

### Container (Recommended)
```bash
podman build -t cleaners-app .
podman run -it --rm cleaners-app
```

### Development Setup
```bash
git clone https://github.com/daytonhaney/cleaners-app.git
cd cleaners-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Usage

The application provides an interactive console interface for:
- Customer registration and transaction processing
- Cleaning package selection (Regular, Premium, Outdoor)
- Senior discount application (15% for customers 65+)
- Employee information display
- Daily transaction summaries

## Features

- Customer management with SQLite database
- Three cleaning packages with automatic pricing
- Labor calculation ($0.15 per square foot)
- Automatic database creation and backup
- Rich text-based user interface

## Package Pricing

- **[1] Regular**: General cleaning services - $100.00
- **[2] Premium**: Regular plus bathrooms, closets, laundry - $200.00  
- **[3] Outdoor**: Lawn care services - $300.00

## Database

Uses SQLite (`business_data.db`) with automatic creation and backup functionality.

## System Requirements

- Python 3.11+
- Rich library (included in requirements.txt)
- 2GB+ RAM
- 50MB+ disk space

## License

BSD Zero Clause License - Free for commercial and personal use.
