CREATE FUNCTION CalculateTotalMonthlySpending(userId INT, monthVal INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);
    SELECT SUM(t.amount) INTO total
    FROM Transactions t
    JOIN Accounts a ON t.account_id = a.account_id
    WHERE a.user_id = userId
      AND MONTH(t.date) = monthVal
      AND t.transaction_type = 'expense';
    RETURN total;
END;

CREATE FUNCTION RemainingBudget(userId INT, categoryId INT)
RETURNS DECIMAL(10,2)
BEGIN
    RETURN 0;
END;