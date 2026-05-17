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

-- INDEXES
CREATE INDEX idx_user_email ON Users(email);
CREATE INDEX idx_account_user ON Accounts(user_id);
CREATE INDEX idx_transaction_account ON Transactions(account_id);
CREATE INDEX idx_transaction_category ON Transactions(category_id);
CREATE INDEX idx_subscription_user ON Subscriptions(user_id);
CREATE INDEX idx_budget_user_category ON Budgets(user_id, category_id);
CREATE INDEX idx_loan_user ON Loans(user_id);
CREATE INDEX idx_installment_loan ON Installments(loan_id);
CREATE INDEX idx_notification_user ON Notifications(user_id);
CREATE INDEX idx_transactions_user_date ON Transactions(user_id, transaction_date);
CREATE INDEX idx_budget_user_month_year ON Budgets(user_id, month, year);

INSERT INTO Users (first_name,last_name,email,date_of_birth,created_at) VALUES
('Aarav','Sharma','aarav.sharma@example.com','2001-04-12','2023-01-10 09:00:00'),
('Meera','Iyer','meera.iyer@example.com','2005-08-21','2024-02-11 10:15:00'),
('Kabir','Patel','kabir.patel@example.com','2002-02-05','2022-03-12 11:30:00'),
('Nitya','Verma','nitya.verma@example.com','2006-11-18','2025-04-13 12:45:00'),
('Riya','Rao','riya.rao@example.com','2003-07-09','2021-05-14 13:05:00'),
('Arjun','Mehta','arjun.mehta@example.com','2004-06-25','2020-06-15 09:30:00'),
('Sneha','Iyer','sneha.iyer@example.com','2007-09-14','2024-07-16 10:10:00'),
('Vihaan','Nair','vihaan.nair@example.com','2001-12-02','2023-08-17 14:10:00'),
('Priya','Kapoor','priya.kapoor@example.com','2005-04-30','2022-09-18 16:25:00'),
('Karan','Malhotra','karan.malhotra@example.com','2000-10-17','2025-10-19 17:00:00'),
('Neha','Sethi','neha.sethi@example.com','2008-01-08','2024-11-20 09:50:00'),
('Rohan','Das','rohan.das@example.com','2002-05-27','2021-12-21 13:15:00'),
('Pooja','Mishra','pooja.mishra@example.com','2003-08-11','2020-01-22 11:05:00'),
('Vikram','Singh','vikram.singh@example.com','2001-09-29','2022-02-23 07:40:00'),
('Nisha','Khan','nisha.khan@example.com','2006-12-19','2023-03-24 15:10:00'),
('Aman','Jain','aman.jain@example.com','2004-03-03','2025-04-25 10:30:00'),
('Meera','Joshi','meera.joshi@example.com','2007-06-07','2024-05-26 08:20:00'),
('Yash','Gupta','yash.gupta@example.com','2002-11-23','2021-06-27 18:10:00'),
('Isha','Bose','isha.bose@example.com','2000-07-15','2020-07-28 19:40:00'),
('Dev','Kulkarni','dev.kulkarni@example.com','2009-02-28','2025-08-29 12:10:00'),
('Anaya','Shetty','anaya.shetty@example.com','2003-09-09','2022-09-30 09:05:00'),
('Sahil','Chopra','sahil.chopra@example.com','2001-10-10','2023-10-31 17:35:00'),
('Tanvi','Bhat','tanvi.bhat@example.com','2005-01-16','2024-12-01 08:55:00'),
('Harsh','Reddy','harsh.reddy@example.com','2006-05-22','2021-01-02 14:45:00'),
('Kavya','Menon','kavya.menon@example.com','2004-08-01','2025-02-03 16:15:00');

INSERT INTO Accounts (user_id,account_type,balance) VALUES
(1,'bank',25000.00),(1,'wallet',1500.00),
(2,'bank',18000.00),(3,'cash',2200.00),
(4,'bank',30500.00),(5,'wallet',1000.00),
(6,'bank',27500.00),(7,'cash',3200.00),
(8,'bank',19800.00),(9,'wallet',1200.00),
(10,'bank',25600.00),(11,'cash',1800.00),
(12,'bank',22200.00),(13,'bank',31000.00),
(14,'wallet',900.00),(15,'bank',28700.00),
(16,'cash',1500.00),(17,'bank',20500.00),
(18,'wallet',1100.00),(19,'bank',33000.00),
(20,'cash',2600.00),(21,'bank',19500.00),
(22,'wallet',1400.00),(23,'bank',21400.00),
(24,'cash',1750.00),(25,'bank',29000.00);

INSERT INTO TransactionCategories (category_name) VALUES
('Food'),('Travel'),('Rent'),('Salary'),
('Entertainment'),('Shopping'),('Bills'),
('Health'),('Education'),('Investment'),
('Groceries'),('Utilities'),('Fitness'),('Gifts');

INSERT INTO Transactions (user_id,account_id,category_id,amount,type,transaction_date) VALUES
(1,1,4,5000.00,'income','2021-03-01'),
(1,1,1,450.00,'expense','2021-03-02'),
(2,3,4,6000.00,'income','2022-04-01'),
(2,3,2,800.00,'expense','2022-04-03'),
(3,4,1,250.00,'expense','2023-05-04'),
(4,5,3,7000.00,'expense','2024-06-05'),
(4,5,4,15000.00,'income','2024-06-01'),
(5,6,6,600.00,'expense','2021-07-06'),
(6,7,4,12000.00,'income','2022-07-01'),
(6,7,7,950.00,'expense','2022-07-07'),
(7,8,8,500.00,'expense','2023-08-08'),
(8,9,2,1200.00,'expense','2024-08-08'),
(9,10,5,450.00,'expense','2025-09-09'),
(10,11,4,9000.00,'income','2021-09-01'),
(10,11,1,550.00,'expense','2021-09-10'),
(11,12,9,2000.00,'expense','2022-10-11'),
(12,13,10,3000.00,'expense','2023-10-11'),
(13,14,4,14000.00,'income','2024-11-01'),
(14,15,6,750.00,'expense','2024-11-12'),
(15,16,3,6500.00,'expense','2021-11-12'),
(16,17,4,11000.00,'income','2022-12-01'),
(17,18,1,400.00,'expense','2022-12-13'),
(18,19,5,350.00,'expense','2023-12-13'),
(19,20,7,1200.00,'expense','2025-01-14'),
(20,21,4,13000.00,'income','2025-01-01'),
(21,22,8,650.00,'expense','2024-01-14'),
(22,23,2,900.00,'expense','2023-02-15'),
(23,24,6,700.00,'expense','2022-02-15'),
(24,25,4,10000.00,'income','2021-03-01'),
(25,25,1,500.00,'expense','2025-03-16'),
(1,2,11,980.00,'expense','2026-04-02'),
(2,3,12,2100.00,'expense','2026-04-04'),
(3,4,13,400.00,'expense','2026-05-06'),
(4,5,14,1200.00,'expense','2026-06-07'),
(5,6,11,760.00,'expense','2026-07-08');

INSERT INTO Subscriptions (user_id,service_name,monthly_fee,start_date,next_due_date,status) VALUES
(1,'Netflix',55.00,'2021-01-01','2026-04-01','Active'),
(2,'Spotify',20.00,'2022-02-01','2026-04-05','Active'),
(3,'Amazon Prime',30.00,'2023-01-15','2026-04-15','Active'),
(4,'YouTube',25.00,'2024-02-10','2026-04-10','Active'),
(5,'Disney+',40.00,'2021-01-20','2026-04-20','Inactive'),
(6,'Canva',35.00,'2022-03-01','2026-04-01','Active'),
(7,'Microsoft 365',28.00,'2023-02-12','2026-04-12','Active'),
(8,'Apple Music',18.00,'2024-01-25','2026-04-25','Active'),
(9,'Hotstar',22.00,'2021-01-28','2026-04-28','Inactive'),
(10,'Coursera',45.00,'2022-02-05','2026-04-05','Active'),
(11,'Zomato Gold',19.00,'2023-04-05','2026-04-30','Active'),
(12,'Adobe',60.00,'2024-05-10','2026-05-10','Active');

INSERT INTO Budgets (user_id,category_id,limit_amount,month,year) VALUES
(1,1,2000.00,3,2021),
(2,2,1500.00,3,2022),
(3,1,1200.00,3,2023),
(4,3,8000.00,3,2024),
(5,6,2000.00,3,2025),
(6,7,2500.00,4,2026),
(7,8,1800.00,4,2022),
(8,2,2200.00,4,2023),
(9,5,1300.00,4,2024),
(10,1,2500.00,4,2025),
(11,11,1600.00,5,2026),
(12,12,2400.00,6,2026);

INSERT INTO Loans (user_id,loan_type,loan_amount,interest_rate,start_date) VALUES
(1,'Education',50000.00,8.50,'2021-01-01'),
(4,'Car',300000.00,9.00,'2022-02-01'),
(6,'Personal',100000.00,12.00,'2023-01-15'),
(10,'Home',800000.00,7.50,'2024-03-01'),
(15,'Bike',90000.00,10.00,'2025-02-10'),
(18,'Business',250000.00,11.25,'2026-06-18'),
(21,'Medical',70000.00,9.75,'2024-09-12');

INSERT INTO Installments (loan_id,amount,due_date,status) VALUES
(1,4500.00,'2025-04-10','Pending'),
(1,4500.00,'2025-05-10','Pending'),
(2,15000.00,'2025-04-15','Pending'),
(2,15000.00,'2025-05-15','Pending'),
(3,9000.00,'2025-04-20','Paid'),
(3,9000.00,'2025-05-20','Pending'),
(4,25000.00,'2025-04-25','Pending'),
(4,25000.00,'2025-05-25','Pending'),
(5,8000.00,'2025-04-18','Paid'),
(5,8000.00,'2025-05-18','Pending'),
(6,12000.00,'2026-07-18','Pending'),
(7,6500.00,'2026-08-12','Pending');

INSERT INTO Notifications (user_id,message,notification_date,is_read) VALUES
(1,'Netflix due soon','2025-03-28',FALSE),
(2,'Travel budget exceeded','2024-03-25',TRUE),
(3,'Subscription reminder','2023-03-30',FALSE),
(4,'Loan due soon','2022-03-31',FALSE),
(5,'Payment successful','2021-03-27',TRUE),
(6,'Bills updated','2026-03-26',TRUE),
(7,'Health expense recorded','2024-03-28',FALSE),
(8,'Subscription inactive','2023-03-29',FALSE),
(9,'Budget alert','2022-03-29',FALSE),
(10,'Home loan due','2021-03-31',FALSE),
(11,'Fitness budget warning','2026-04-01',FALSE),
(12,'Utility bill reminder','2026-04-02',TRUE);

-- MONTHLY EXPENSE VIEW
CREATE VIEW MonthlyExpenseTracker AS
SELECT
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) AS user_name,
    YEAR(t.transaction_date) AS trans_year,
    MONTH(t.transaction_date) AS trans_month,
    tc.category_name,
    SUM(t.amount) AS total_expense
FROM Transactions t
JOIN Users u ON t.user_id = u.user_id
JOIN TransactionCategories tc ON t.category_id = tc.category_id
WHERE t.type = 'expense'
GROUP BY u.user_id, user_name, trans_year, trans_month, tc.category_name;

-- ACTIVE SUBSCRIPTIONS VIEW
CREATE VIEW ActiveSubscriptionsView AS
SELECT
    s.subscription_id,
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) AS user_name,
    s.service_name,
    s.monthly_fee,
    s.start_date,
    s.next_due_date,
    s.status
FROM Subscriptions s
JOIN Users u ON s.user_id = u.user_id
WHERE s.status = 'Active';

-- LOAN STATUS VIEW
CREATE VIEW LoanStatusView AS
SELECT
    l.loan_id,
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) AS user_name,
    l.loan_type,
    l.loan_amount,
    l.interest_rate,
    l.start_date,
    COUNT(i.installment_id) AS total_installments,
    SUM(CASE WHEN i.status = 'Paid' THEN 1 ELSE 0 END) AS paid_installments,
    SUM(CASE WHEN i.status = 'Pending' THEN 1 ELSE 0 END) AS pending_installments
FROM Loans l
JOIN Users u ON l.user_id = u.user_id
LEFT JOIN Installments i ON l.loan_id = i.loan_id
GROUP BY l.loan_id, u.user_id, user_name, l.loan_type, l.loan_amount, l.interest_rate, l.start_date;

-- ADD TRANSACTION PROCEDURE
DELIMITER $$
CREATE PROCEDURE AddTransaction(
    IN p_user_id INT,
    IN p_account_id INT,
    IN p_category_id INT,
    IN p_amount DECIMAL(10,2),
    IN p_type VARCHAR(10),
    IN p_date DATE
)
BEGIN
    INSERT INTO Transactions(user_id, account_id, category_id, amount, type, transaction_date)
    VALUES (p_user_id, p_account_id, p_category_id, p_amount, p_type, p_date);
END $$

-- LOAN INSTALLMENTS PROCEDURE
CREATE PROCEDURE GiveLoanInstallments(
    IN p_loan_id INT,
    IN p_installment_amount DECIMAL(10,2),
    IN p_due_date DATE,
    IN p_count INT
)
BEGIN
    DECLARE i INT DEFAULT 0;

    WHILE i < p_count DO
        INSERT INTO Installments(loan_id, amount, due_date, status)
        VALUES (p_loan_id, p_installment_amount, DATE_ADD(p_due_date, INTERVAL i MONTH), 'Pending');

        SET i = i + 1;
    END WHILE;
END $$
DELIMITER ;

-- TOTAL MONTHLY SPENDING FUNCTION
DELIMITER $$
CREATE FUNCTION TotalMonthlySpending(p_user_id INT, p_month INT, p_year INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);

    SELECT SUM(amount) INTO total
    FROM Transactions
    WHERE user_id = p_user_id
      AND type = 'expense'
      AND MONTH(transaction_date) = p_month
      AND YEAR(transaction_date) = p_year;

    RETURN IFNULL(total, 0);
END $$

-- REMAINING BUDGET FUNCTION
CREATE FUNCTION RemainingBudget(p_budget_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE limit_amt DECIMAL(10,2);
    DECLARE spent DECIMAL(10,2);

    SELECT limit_amount INTO limit_amt
    FROM Budgets
    WHERE budget_id = p_budget_id;

    SELECT IFNULL(SUM(t.amount),0) INTO spent
    FROM Transactions t
    JOIN Budgets b ON t.category_id = b.category_id
    WHERE b.budget_id = p_budget_id
      AND t.type = 'expense'
      AND MONTH(t.transaction_date) = b.month
      AND YEAR(t.transaction_date) = b.year;

    RETURN limit_amt - spent;
END $$
DELIMITER ;

-- BUDGET ALERT TRIGGER
DELIMITER $$
CREATE TRIGGER Budget_Overspend_Alert
AFTER INSERT ON Transactions
FOR EACH ROW
BEGIN
    DECLARE limit_amt DECIMAL(10,2);
    DECLARE spent DECIMAL(10,2);

    SELECT limit_amount INTO limit_amt
    FROM Budgets
    WHERE user_id = NEW.user_id
      AND category_id = NEW.category_id
    LIMIT 1;

    IF limit_amt IS NOT NULL THEN

        SELECT SUM(amount) INTO spent
        FROM Transactions
        WHERE user_id = NEW.user_id
          AND category_id = NEW.category_id
          AND type = 'expense';

        IF spent > limit_amt THEN
            INSERT INTO Notifications(user_id, message, notification_date)
            VALUES (NEW.user_id, 'Budget exceeded!', CURDATE());
        END IF;

    END IF;
END $$

-- SUBSCRIPTION TRIGGER
CREATE TRIGGER Subscription_Reminder
AFTER INSERT ON Subscriptions
FOR EACH ROW
BEGIN
    INSERT INTO Notifications(user_id, message, notification_date)
    VALUES (NEW.user_id, CONCAT('Subscription due: ', NEW.service_name), CURDATE());
END $$

-- LOAN TRIGGER
CREATE TRIGGER Loan_Payment_Reminder
AFTER INSERT ON Installments
FOR EACH ROW
BEGIN
    INSERT INTO Notifications(user_id, message, notification_date)
    VALUES (
        (SELECT user_id FROM Loans WHERE loan_id = NEW.loan_id),
        'Loan installment due soon',
        CURDATE()
    );
END $$
DELIMITER ;