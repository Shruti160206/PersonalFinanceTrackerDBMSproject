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

-- CATEGORIES
CREATE TABLE TransactionCategories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

-- TRANSACTIONS
CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    category_id INT,
    amount DECIMAL(10,2) CHECK (amount > 0),
    transaction_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES TransactionCategories(category_id)
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

-- NOTIFICATIONS
CREATE TABLE Notifications (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    message VARCHAR(255) NOT NULL,
    notification_date DATE NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

INSERT INTO TransactionCategories (category_name) VALUES ('Housing');

INSERT INTO TransactionCategories (category_name) VALUES ('Food & Dining');

INSERT INTO TransactionCategories (category_name) VALUES ('Transportation');
"""

# =========================
# EXECUTE SQL SCRIPT
# =========================
for statement in sql_script.split(";"):
    stmt = statement.strip()
    if stmt:
        cursor.execute(stmt)

# ==================================================================
# TRIGGER 1: Check for notification after a transaction is created
# ==================================================================
trigger_insert = """
CREATE TRIGGER trg_transaction_after_insert
AFTER INSERT ON Transactions
FOR EACH ROW
BEGIN

    DECLARE total_spent DECIMAL(10,2);
    DECLARE budget_limit DECIMAL(10,2);
    DECLARE cat_name VARCHAR(50);

    -- safe category lookup
    SELECT IFNULL(category_name, 'Unknown Category')
    INTO cat_name
    FROM TransactionCategories
    WHERE TransactionCategories.category_id = NEW.category_id;

    -- calculate total spent
    SELECT IFNULL(SUM(amount), 0)
    INTO total_spent
    FROM Transactions
    WHERE user_id = NEW.user_id
      AND category_id = NEW.category_id
      AND MONTH(transaction_date) = MONTH(NEW.transaction_date)
      AND YEAR(transaction_date) = YEAR(NEW.transaction_date);

    -- fetch budget
    SELECT limit_amount
    INTO budget_limit
    FROM Budgets
    WHERE user_id = NEW.user_id
      AND category_id = NEW.category_id
      AND month = MONTH(NEW.transaction_date)
      AND year = YEAR(NEW.transaction_date)
    LIMIT 1;

    -- ONLY insert if message is valid
    IF budget_limit IS NOT NULL
       AND total_spent > budget_limit THEN

        INSERT INTO Notifications (
            user_id,
            message,
            notification_date,
            is_read
        )
        VALUES (
            NEW.user_id,
            CONCAT(
                'Budget exceeded for ',
                IFNULL(cat_name, 'category'),
                '. Limit: AED ',
                budget_limit,
                ', Spent: AED ',
                total_spent
            ),
            CURDATE(),
            FALSE
        );

    END IF;

END
"""

cursor.execute(trigger_insert)

# ==================================================================
# TRIGGER 2: Check for notification after a transaction is deleted
# ==================================================================
trigger_delete = """
CREATE TRIGGER trg_transaction_after_delete
AFTER DELETE ON Transactions
FOR EACH ROW
BEGIN

    DECLARE total_spent DECIMAL(10,2);
    DECLARE budget_limit DECIMAL(10,2);
    DECLARE cat_name VARCHAR(50);

    -- safe category lookup
    SELECT IFNULL(category_name, 'Unknown Category')
    INTO cat_name
    FROM TransactionCategories
    WHERE category_id = OLD.category_id
    LIMIT 1;

    -- recalculate total spent after deletion
    SELECT IFNULL(SUM(amount), 0)
    INTO total_spent
    FROM Transactions
    WHERE user_id = OLD.user_id
      AND category_id = OLD.category_id
      AND MONTH(transaction_date) = MONTH(OLD.transaction_date)
      AND YEAR(transaction_date) = YEAR(OLD.transaction_date);

    -- fetch budget
    SELECT limit_amount
    INTO budget_limit
    FROM Budgets
    WHERE user_id = OLD.user_id
      AND category_id = OLD.category_id
      AND month = MONTH(OLD.transaction_date)
      AND year = YEAR(OLD.transaction_date)
    LIMIT 1;

    -- notify if back within budget
    IF budget_limit IS NOT NULL
       AND total_spent <= budget_limit THEN

        INSERT INTO Notifications (
            user_id,
            message,
            notification_date,
            is_read
        )
        VALUES (
            OLD.user_id,
            COALESCE(
                CONCAT(
                    'Budget is now within limit for ',
                    COALESCE(cat_name, 'category'),
                    '. Current spending: AED ',
                    COALESCE(total_spent, 0)
                ),
                'Budget status updated'
            ),
            CURDATE(),
            FALSE
        );

    END IF;

END
"""

cursor.execute(trigger_delete)

dashboard_summary_procedure = """
DELIMITER $$

CREATE PROCEDURE GetDashboardSummary (
    IN p_user_id INT
)
BEGIN

    DECLARE v_monthly_expense DECIMAL(10,2);
    DECLARE v_notification_count INT;

    -- monthly expense
    SELECT IFNULL(SUM(amount), 0)
    INTO v_monthly_expense
    FROM Transactions
    WHERE user_id = p_user_id
      AND MONTH(transaction_date) = MONTH(CURDATE())
      AND YEAR(transaction_date) = YEAR(CURDATE());

    -- notification count this month
    SELECT COUNT(*)
    INTO v_notification_count
    FROM Notifications
    WHERE user_id = p_user_id
      AND MONTH(notification_date) = MONTH(CURDATE())
      AND YEAR(notification_date) = YEAR(CURDATE());

    -- return result as a single row
    SELECT 
        v_monthly_expense AS monthly_expense,
        v_notification_count AS monthly_notification_count;

END $$

DELIMITER ;
"""

cursor.execute(dashboard_summary_procedure)

conn.commit()
print("Database, tables and triggers created successfully!")

# =========================
# CLOSE CONNECTION
# =========================
cursor.close()
conn.close()