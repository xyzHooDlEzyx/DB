-- Task 1

CREATE TABLE IF NOT EXISTS `CustomerAddresses` (
    `AddressID` INT NOT NULL AUTO_INCREMENT,
    `CustomerID` INT NOT NULL,
    `Street` VARCHAR(255) NOT NULL,
    `City` VARCHAR(100) NOT NULL,
    `State` VARCHAR(100) NULL,
    `PostalCode` VARCHAR(20) NOT NULL,
    `Country` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`AddressID`)
) ENGINE = InnoDB;

DELIMITER $$

CREATE TRIGGER `before_insert_customer_address`
BEFORE INSERT ON `CustomerAddresses`
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Customers WHERE CustomerID = NEW.CustomerID) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CustomerID does not exist in Customers table.';
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER `before_update_customer_address`
BEFORE UPDATE ON `CustomerAddresses`
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Customers WHERE CustomerID = NEW.CustomerID) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CustomerID does not exist in Customers table.';
    END IF;
END$$

DELIMITER ;

-- INSERT INTO CustomerAddresses (CustomerID, Street, City, State, PostalCode, Country)
-- VALUES
-- (1, 'Hrushevskoho Street, 1', 'Kyiv', NULL, '01001', 'Ukraine'),
-- (2, 'Sumskaya Street, 15', 'Kharkiv', NULL, '61000', 'Ukraine'),
-- (3, 'Deribasivska Street, 3', 'Odesa', NULL, '65000', 'Ukraine'),
-- (4, 'Freedom Avenue, 20', 'Lviv', NULL, '79000', 'Ukraine'),
-- (5, 'Shevchenko Street, 8', 'Dnipro', NULL, '49000', 'Ukraine'),
-- (6, 'Peace Street, 5', 'Zaporizhzhia', NULL, '69000', 'Ukraine'),
-- (7, 'Soborna Street, 12', 'Vinnytsia', NULL, '21000', 'Ukraine'),
-- (8, 'Cossack Street, 7', 'Poltava', NULL, '36000', 'Ukraine'),
-- (9, 'Victory Avenue, 10', 'Cherkasy', NULL, '18000', 'Ukraine'),
-- (10, 'Franko Street, 2', 'Ivano-Frankivsk', NULL, '76000', 'Ukraine');
	
