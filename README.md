# LIBRARY MANAGEMENT SYSTEM

A GUI-based Library Management System developed using Python, Tkinter, and MySQL.

# PROJECT OVERVIEW

The objective of this project is to manage library books, issue and return operations, search books, store transaction records, and generate reports through a user-friendly graphical interface.

# TECHNOLOGIES USED

- Python
- Tkinter
- MySQL
- mysql-connector-python
- VS Code

# KEY FEATURES

## 1. Book Management
- Add new books
- View all books
- Update book details
- Delete books
- Track available quantity

## 2. Search Book
Books can be searched using:
- Book ID
- Book Name
- Author Name

## 3. Issue and Return Books
- Issue books to students
- Return issued books
- Automatically update book quantity
- Maintain issue and return dates
- Track transaction status

## 4. Database Management

MySQL is used to store:

- Book records
- Student information
- Issue records
- Return records
- Transaction status

## 5. Reports

The system provides:

- Available Books Report
- Issued Books Report
- Complete Transaction Report

## 6. Validation

The system validates:

- Empty fields
- Invalid quantities
- Invalid Book IDs
- Invalid Transaction IDs
- Unavailable books
- Invalid search input

# PROJECT STRUCTURE

```text
Library-Management-System/
│
├── main.py
├── database.py
├── book_management.py
├── issue_return.py
├── reports.py
├── requirements.txt
└── README.md

DATABASE :-

    Database Name: library_db


BOOKS TABLE :-

Stores:
- Book ID
- Book Name
- Author
- Quantity

TRANSACTIONS TABLE :-

Stores:
- Transaction ID
- Book ID
- Student Name
- Issue Date
- Return Date
- Status

HOW TO RUN :-

Step 1: Install Python
    Make sure Python is installed on your computer.

Step 2: Install Required Package
    Open the terminal and run:
    pip install -r requirements.txt

Step 3: Create MySQL Database
    Create a database named: library_db
    Create the required books and transactions tables in MySQL.

Step 4: Configure Database
    Open: database.py
    Enter your local MySQL username and password.

Step 5: Run the Application
    Run: python main.py


PROJECT WORKFLOW :-

1. Create Book Management Module
2. Implement Book Issue and Return
3. Store records in MySQL Database
4. Implement Search Functionality
5. Generate Reports
6. Validate System Operations

CONCLUSION :-

The Library Management System provides an efficient and user-friendly solution for managing books, issuing and returning books, searching records, maintaining transaction data, and generating library reports.