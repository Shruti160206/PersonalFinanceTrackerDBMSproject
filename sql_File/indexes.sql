CREATE INDEX idx_user_email ON Users(email);
CREATE INDEX idx_account_user ON Accounts(user_id);
CREATE INDEX idx_transaction_account ON Transactions(account_id);
CREATE INDEX idx_transaction_category ON Transactions(category_id);
CREATE INDEX idx_subscription_user ON Subscriptions(user_id);
CREATE INDEX idx_budget_user_category ON Budgets(user_id, category_id);
CREATE INDEX idx_loan_user ON Loans(user_id);
CREATE INDEX idx_installment_loan ON Installments(loan_id);
CREATE INDEX idx_notification_user ON Notifications(user_id);