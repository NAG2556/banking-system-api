# Banking Transaction System

A complete backend project using Python, Flask, and SQLite.

## Features
- **User Authentication**: Secure registration and JWT-based login using `Flask-Bcrypt` and `Flask-JWT-Extended`
- **Account Management**: Create accounts, retrieve bank account details, zero negative balance bounds
- **Transaction Processing**: Securely deposit, withdraw, and transfer funds
- **Transaction History**: Audit logs for all account transactions
- **SQLite Database**: Designed using `Flask-SQLAlchemy`

## Project Structure
```
banking_system/
├── app/
│   ├── models/           # SQLAlchemy Data Models (User, Account, Transaction)
│   ├── routes/           # RESTful API Endpoints (Auth, Accounts, Transactions)
│   ├── services/         # Business Logic (e.g., handling balance calculation reliably)
│   ├── __init__.py       # App initialization
│   └── config.py         # Configuration settings
├── run.py                # Main application entry point
├── requirements.txt      # Required dependencies
├── README.md             # Project documentation
└── sample_requests.md    # API usage examples with cURL
```

## Setup Instructions

### 1. Create a virtual environment and activate it

MacOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python run.py
```

The server will automatically create the database `banking.db` and run on `http://127.0.0.1:5001`.

## API Documentation
Please see `sample_requests.md` for complete cURL examples grouped by actions (register, login, create account, transfer, etc.).
