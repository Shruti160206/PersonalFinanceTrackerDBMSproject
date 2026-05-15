CREATE TRIGGER BudgetOverspendAlert
AFTER INSERT ON Transactions
FOR EACH ROW
BEGIN
    -- Overspend alert logic
END;

CREATE TRIGGER SubscriptionReminderTrigger
BEFORE UPDATE ON Subscriptions
FOR EACH ROW
BEGIN
    -- Reminder logic
END;

CREATE TRIGGER LoanPaymentReminderTrigger
BEFORE UPDATE ON Installments
FOR EACH ROW
BEGIN
    -- Loan reminder logic
END;