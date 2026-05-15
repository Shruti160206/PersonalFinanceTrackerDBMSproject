CREATE VIEW MonthlyExpenseTracker AS
SELECT u.full_name, MONTH(t.date) AS month, SUM(t.amount) AS total_expense
FROM Users u
JOIN Accounts a ON u.user_id = a.user_id
JOIN Transactions t ON a.account_id = t.account_id
WHERE t.transaction_type = 'expense'
GROUP BY u.user_id, MONTH(t.date);

CREATE VIEW ActiveSubscriptionsView AS
SELECT u.full_name, s.service_name, s.monthly_fee, s.next_due_date
FROM Users u
JOIN Subscriptions s ON u.user_id = s.user_id
WHERE s.status = 'Active';

CREATE VIEW LoanStatusView AS
SELECT u.full_name, l.loan_name, l.principal_amount, l.status
FROM Users u
JOIN Loans l ON u.user_id = l.user_id;