DELIMITER //
CREATE PROCEDURE AddTransaction(
    IN p_account_id INT,
    IN p_category_id INT,
    IN p_amount DECIMAL(10,2),
    IN p_type VARCHAR(20),
    IN p_description VARCHAR(255)
)
BEGIN
    INSERT INTO Transactions(account_id, category_id, amount, transaction_type, description, date)
    VALUES (p_account_id, p_category_id, p_amount, p_type, p_description, NOW());
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GenerateLoanInstallments(IN p_loan_id INT)
BEGIN
    -- Installment generation logic here
END //
DELIMITER ;