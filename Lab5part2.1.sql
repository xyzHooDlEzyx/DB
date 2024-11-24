-- Task 2.1

DELIMITER $$

CREATE PROCEDURE InsertCustomerAddress(
    IN p_CustomerID INT,
    IN p_Street VARCHAR(255),
    IN p_City VARCHAR(100),
    IN p_State VARCHAR(100),
    IN p_PostalCode VARCHAR(20),
    IN p_Country VARCHAR(100)
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Customers WHERE CustomerID = p_CustomerID) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CustomerID does not exist in Customers table.';
    ELSE
        INSERT INTO CustomerAddresses (CustomerID, Street, City, State, PostalCode, Country)
        VALUES (p_CustomerID, p_Street, p_City, p_State, p_PostalCode, p_Country);
    END IF;
END$$

DELIMITER ;

SHOW PROCEDURE STATUS WHERE Db = 'private_bank_lab5';


-- Task 2.2

DELIMITER $$

CREATE PROCEDURE InsertCustomerAccount(
    IN FirstName VARCHAR(100),
    IN LastName VARCHAR(100),
    IN AccountNumber VARCHAR(20)
)
BEGIN
    DECLARE customer_id INT;
    DECLARE account_id INT;

    SELECT CustomerID INTO customer_id
    FROM Customers
    WHERE FirstName = FirstName AND LastName = LastName;

    SELECT AccountID INTO account_id
    FROM Accounts
    WHERE AccountNumber = AccountNumber;

    IF EXISTS (
        SELECT 1
        FROM CustomerAccounts
        WHERE CustomerID = customer_id AND AccountID = account_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate CustomerAccount entry exists';
    ELSE
        INSERT INTO CustomerAccounts (CustomerID, AccountID)
        VALUES (customer_id, account_id);
    END IF;
END$$

DELIMITER ;

-- Викликаємо збережену процедуру для вставки нового запису
CALL InsertCustomerAccount('John', 'Doe', '123456789012');


-- Task2.3

DELIMITER $$

CREATE PROCEDURE InsertNonameRows(
    IN base_name VARCHAR(50),
    IN start_number INT,
    IN table_name VARCHAR(50)
)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE full_name VARCHAR(255);

    WHILE i < 10 DO
        SET full_name = CONCAT(base_name, start_number + i);

        SET @insert_query = CONCAT(
            'INSERT INTO ', table_name, ' (FirstName, LastName, Email, Phone) ',
            'VALUES (\'', full_name, '\', \'User\', \'', full_name, '@example.com\', \'12345678', start_number + i, '\')'
        );
        PREPARE stmt FROM @insert_query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        SET i = i + 1; -- Збільшуємо лічильник
    END WHILE;
END$$

DELIMITER ;

-- task 2.4

DELIMITER $$

CREATE FUNCTION GetBalanceStat(stat_type VARCHAR(3))
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE result DECIMAL(10, 2);

    -- Вибір статистики на основі параметра stat_type
    IF stat_type = 'MAX' THEN
        SELECT MAX(Balance) INTO result FROM Accounts;
    ELSEIF stat_type = 'MIN' THEN
        SELECT MIN(Balance) INTO result FROM Accounts;
    ELSEIF stat_type = 'SUM' THEN
        SELECT SUM(Balance) INTO result FROM Accounts;
    ELSEIF stat_type = 'AVG' THEN
        SELECT AVG(Balance) INTO result FROM Accounts;
    ELSE
        SET result = NULL;
    END IF;

    RETURN result;
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE GetAccountsBalanceStat(stat_type VARCHAR(3))
BEGIN
    SELECT GetBalanceStat(stat_type) AS BalanceStat;
END $$

DELIMITER ;

CALL GetAccountsBalanceStat('MAX');


-- task 2.5

DELIMITER $$

CREATE PROCEDURE SplitAccountsIntoRandomTables()
BEGIN
    DECLARE v_table1_name VARCHAR(255);
    DECLARE v_table2_name VARCHAR(255);
    DECLARE v_account_id INT;
    DECLARE v_account_number VARCHAR(255);
    DECLARE v_balance DECIMAL(10, 2);
    DECLARE v_currency VARCHAR(10);
    DECLARE v_account_type VARCHAR(50);
    DECLARE done INT DEFAULT 0;

    -- Курсор для вибору даних із таблиці accounts
    DECLARE account_cursor CURSOR FOR SELECT AccountID, AccountNumber, Balance, Currency, AccountType FROM accounts;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	
    -- Створюємо імена для нових таблиць із поточним штампом часу
    SET v_table1_name = CONCAT('Accounts_part1_', UNIX_TIMESTAMP());
    SET v_table2_name = CONCAT('Accounts_part2_', UNIX_TIMESTAMP());

    -- Створюємо структуру для першої таблиці
    SET @create_table1_sql = CONCAT('CREATE TABLE ', v_table1_name, ' LIKE accounts');
    PREPARE stmt FROM @create_table1_sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Створюємо структуру для другої таблиці
    SET @create_table2_sql = CONCAT('CREATE TABLE ', v_table2_name, ' LIKE accounts');
    PREPARE stmt FROM @create_table2_sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    -- Відкриваємо курсор для вибору рядків з таблиці accounts
    OPEN account_cursor;
    FETCH account_cursor INTO v_account_id, v_account_number, v_balance, v_currency, v_account_type;

    -- Копіюємо дані з таблиці accounts у випадкові нові таблиці
    WHILE done = 0 DO
        -- Випадковим чином визначаємо, куди вставляти дані
        SET @random_table = IF(RAND() < 0.5, v_table1_name, v_table2_name);

        -- Генеруємо SQL для вставки даних
        SET @insert_sql = CONCAT(
            'INSERT INTO ', @random_table, 
            ' (AccountID, AccountNumber, Balance, Currency, AccountType) VALUES (',
            v_account_id, ', "', v_account_number, '", ', v_balance, ', "', v_currency, '", "', v_account_type, '")'
        );

        -- Виконуємо SQL вставки
        PREPARE stmt FROM @insert_sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        FETCH account_cursor INTO v_account_id, v_account_number, v_balance, v_currency, v_account_type;
    END WHILE;

    -- Закриваємо курсор
    CLOSE account_cursor;

    -- Повертаємо імена створених таблиць
    SELECT v_table1_name AS Table1, v_table2_name AS Table2;
END $$

DELIMITER ;

CALL SplitAccountsIntoRandomTables();

-- task 3.1

DELIMITER $$

CREATE TRIGGER prevent_update BEFORE UPDATE ON `Beneficiaries`
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Updates are not allowed on the Beneficiaries table';
END $$

CREATE TRIGGER prevent_insert BEFORE INSERT ON `Beneficiaries`
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Inserts are not allowed on the Beneficiaries table';
END $$

CREATE TRIGGER prevent_delete BEFORE DELETE ON `Beneficiaries`
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Deletes are not allowed on the Beneficiaries table';
END $$

DELIMITER ;

UPDATE `Beneficiaries`
SET `BeneficiaryName` = 'New Beneficiary Name'
WHERE `BeneficiaryID` = 1;

INSERT INTO `Beneficiaries` (`BeneficiaryName`, `BankDetailsID`, `BeneficiaryType`)
VALUES ('New Beneficiary', 1, 'Company');

DELETE FROM `Beneficiaries`
WHERE `BeneficiaryID` = 1;


-- task 3.2

-- Створення таблиці для журналу
CREATE TABLE IF NOT EXISTS `change_log` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `action_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `action_type` VARCHAR(10),
    `old_data` TEXT,
    `new_data` TEXT
) ENGINE = InnoDB;


DELIMITER $$
-- Тригер для запису змін після оновлення в таблиці Transactions
CREATE TRIGGER log_transaction_update AFTER UPDATE ON `Transactions`
FOR EACH ROW
BEGIN
    INSERT INTO `change_log` (`action_type`, `old_data`, `new_data`)
    VALUES ('UPDATE', 
            CONCAT('FromAccountID: ', OLD.FromAccountID, ', Amount: ', OLD.Amount), 
            CONCAT('FromAccountID: ', NEW.FromAccountID, ', Amount: ', NEW.Amount));
END $$

-- Тригер для запису змін після вставки в таблицю Transactions
CREATE TRIGGER log_transaction_insert AFTER INSERT ON `Transactions`
FOR EACH ROW
BEGIN
    INSERT INTO `change_log` (`action_type`, `old_data`, `new_data`)
    VALUES ('INSERT', NULL, CONCAT('FromAccountID: ', NEW.FromAccountID, ', Amount: ', NEW.Amount));
END $$

-- Тригер для запису змін після видалення з таблиці Transactions
CREATE TRIGGER log_transaction_delete AFTER DELETE ON `Transactions`
FOR EACH ROW
BEGIN
    INSERT INTO `change_log` (`action_type`, `old_data`, `new_data`)
    VALUES ('DELETE', CONCAT('FromAccountID: ', OLD.FromAccountID, ', Amount: ', OLD.Amount), NULL);
END $$

DELIMITER ;

UPDATE `Transactions`
SET `Amount` = 250.00
WHERE `TransactionID` = 1;

INSERT INTO `Transactions` (`FromAccountID`, `BeneficiaryID`, `TransactionTypeID`, `Amount`, `Status`)
VALUES (1, 2, 1, 300.50, 'Completed');

DELETE FROM `Transactions`
WHERE `TransactionID` = 11;


-- task 3.3

DELIMITER $$

CREATE TRIGGER validate_account_number BEFORE INSERT ON `Accounts`
FOR EACH ROW
BEGIN
    IF NOT NEW.AccountNumber REGEXP '^[A-KL-NP-QST-Z]{2}-[0-9]{3}-[0-9]{2}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'AccountNumber must follow the format: 2 letters (except M and R), "-", 3 digits, "-", 2 digits.';
    END IF;
END $$

DELIMITER ;

INSERT INTO `Accounts` (`AccountNumber`, `Balance`, `Currency`, `AccountType`)
VALUES ('AB-123-45', 1000.00, 'USD', 'Savings');

INSERT INTO `Accounts` (`AccountNumber`, `Balance`, `Currency`, `AccountType`)
VALUES ('MR-123-45', 1000.00, 'USD', 'Savings');



