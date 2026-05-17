import mysql.connector
import os

# =========================
# CONNECT TO MYSQL SERVER
# =========================
conn = mysql.connector.connect(
    host="localhost",
    user="root",          # change if needed
    password=os.getenv("DB_PASSWORD", "password")
)

cursor = conn.cursor()

# =========================
# SQL SCRIPT (YOUR ENTIRE DB)
# =========================
sql_script = """
DROP DATABASE IF EXISTS UserFinanceTracker;
CREATE DATABASE UserFinanceTracker;
USE UserFinanceTracker;

-- USERS
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ACCOUNTS
CREATE TABLE Accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    account_type VARCHAR(20) NOT NULL,
    balance DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (balance >= 0),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    CHECK (account_type IN ('bank','wallet','cash'))
);

-- CATEGORIES
CREATE TABLE TransactionCategories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

-- TRANSACTIONS
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    account_id INT,
    category_id INT,
    amount DECIMAL(10,2) CHECK (amount > 0),
    transaction_type VARCHAR(10),
    transaction_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES TransactionCategories(category_id),
    CHECK (transaction_type IN ('income','expense'))
);

-- SUBSCRIPTIONS
CREATE TABLE Subscriptions (
    subscription_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    service_name VARCHAR(50) NOT NULL,
    monthly_fee DECIMAL(10,2) NOT NULL CHECK (monthly_fee > 0),
    start_date DATE NOT NULL,
    next_due_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    CHECK (status IN ('Active','Inactive','Cancelled'))
);

-- BUDGETS
CREATE TABLE Budgets (
    budget_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    limit_amount DECIMAL(10,2) NOT NULL CHECK (limit_amount > 0),
    month INT NOT NULL CHECK (month BETWEEN 1 AND 12),
    year INT NOT NULL CHECK (year >= 2000),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES TransactionCategories(category_id)
);

-- LOANS
CREATE TABLE Loans (
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    loan_type VARCHAR(50) NOT NULL,
    loan_amount DECIMAL(10,2) NOT NULL CHECK (loan_amount > 0),
    interest_rate DECIMAL(5,2) NOT NULL CHECK (interest_rate >= 0),
    start_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- INSTALLMENTS
CREATE TABLE Installments (
    installment_id INT PRIMARY KEY AUTO_INCREMENT,
    loan_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    due_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (loan_id) REFERENCES Loans(loan_id) ON DELETE CASCADE,
    CHECK (status IN ('Pending','Paid'))
);

-- NOTIFICATIONS
CREATE TABLE Notifications (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    message VARCHAR(255) NOT NULL,
    notification_date DATE NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);
"""

# =========================
# EXECUTE SQL SCRIPT
# =========================
for statement in sql_script.split(";"):
    stmt = statement.strip()
    if stmt:
        cursor.execute(stmt)

conn.commit()
print("Database and tables created successfully!")

# =========================
# CLOSE CONNECTION
# =========================
cursor.close()
conn.close()