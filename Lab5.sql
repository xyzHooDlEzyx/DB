CREATE DATABASE IF NOT EXISTS `private_bank_lab5` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `private_bank_lab5`;
DROP TABLE IF EXISTS transferhistory;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS transactiontypes;
DROP TABLE IF EXISTS customeraccounts;
DROP TABLE IF EXISTS beneficiaries;
DROP TABLE IF EXISTS accountbankdetails;
DROP TABLE IF EXISTS bankdetails;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS customers;

-- drop database `private_bank_lab5`;

CREATE TABLE IF NOT EXISTS `Customers` (
    `CustomerID` INT NOT NULL AUTO_INCREMENT,
    `FirstName` VARCHAR(100) NOT NULL,
    `LastName` VARCHAR(100) NOT NULL,
    `Email` VARCHAR(100) NOT NULL UNIQUE,    
    `Phone` VARCHAR(15) NOT NULL UNIQUE,
    PRIMARY KEY (`CustomerID`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Accounts` (
    `AccountID` INT NOT NULL AUTO_INCREMENT,
    `AccountNumber` VARCHAR(20) NOT NULL UNIQUE,
    `Balance` DECIMAL(10,2) NOT NULL,
    `Currency` VARCHAR(10) NOT NULL,
    `AccountType` VARCHAR(50) NOT NULL,
    `CreatedAt` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`AccountID`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Cards` (
    `CardID` INT NOT NULL AUTO_INCREMENT,
    `AccountID` INT NOT NULL,
    `CardNumber` VARCHAR(16) NOT NULL UNIQUE,
    `ExpiryDate` DATE NOT NULL,
    `CardType` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`CardID`),
    FOREIGN KEY (`AccountID`) REFERENCES `Accounts`(`AccountID`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `BankDetails` (
    `BankDetailsID` INT NOT NULL AUTO_INCREMENT,
    `CustomerID` INT NOT NULL,
    `BankName` VARCHAR(100) NOT NULL,
    `BankCode` VARCHAR(20) NOT NULL,
    `CardID` INT NOT NULL,
    PRIMARY KEY (`BankDetailsID`),
    FOREIGN KEY (`CustomerID`) REFERENCES `Customers`(`CustomerID`),
    FOREIGN KEY (`CardID`) REFERENCES `Cards`(`CardID`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `AccountBankDetails` (
    `AccountID` INT NOT NULL,
    `BankDetailsID` INT NOT NULL,
    PRIMARY KEY (`AccountID`, `BankDetailsID`),
    FOREIGN KEY (`AccountID`) REFERENCES `Accounts`(`AccountID`),
    FOREIGN KEY (`BankDetailsID`) REFERENCES `BankDetails`(`BankDetailsID`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Beneficiaries` (
    `BeneficiaryID` INT NOT NULL AUTO_INCREMENT,
    `BeneficiaryName` VARCHAR(255) NOT NULL,
    `BankDetailsID` INT NOT NULL,
    `BeneficiaryType` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`BeneficiaryID`),
    FOREIGN KEY (`BankDetailsID`) REFERENCES `BankDetails`(`BankDetailsID`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `CustomerAccounts` (
    `CustomerID` INT NOT NULL,
    `AccountID` INT NOT NULL,
    PRIMARY KEY (`CustomerID`, `AccountID`),
    FOREIGN KEY (`CustomerID`) REFERENCES `Customers`(`CustomerID`),
    FOREIGN KEY (`AccountID`) REFERENCES `Accounts`(`AccountID`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `TransactionTypes` (
    `TransactionTypeID` INT NOT NULL AUTO_INCREMENT,
    `TransactionTypeName` VARCHAR(100) NULL DEFAULT NULL,
    PRIMARY KEY (`TransactionTypeID`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Transactions` (
    `TransactionID` INT NOT NULL AUTO_INCREMENT,
    `FromAccountID` INT NOT NULL,
    `BeneficiaryID` INT NOT NULL,
    `TransactionTypeID` INT NOT NULL,
    `Amount` DECIMAL(10,2) NOT NULL,
    `TransactionDate` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `Status` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`TransactionID`),
    FOREIGN KEY (`FromAccountID`) REFERENCES `Accounts`(`AccountID`),
    FOREIGN KEY (`BeneficiaryID`) REFERENCES `Beneficiaries`(`BeneficiaryID`),
    FOREIGN KEY (`TransactionTypeID`) REFERENCES `TransactionTypes`(`TransactionTypeID`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `TransferHistory` (
    `TransferID` INT NOT NULL AUTO_INCREMENT,
    `TransactionID` INT NOT NULL,
    `FromAccountID` INT NOT NULL,
    `BeneficiaryID` INT NOT NULL,
    `Amount` DECIMAL(10,2) NOT NULL,
    `TransferDate` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `Description` VARCHAR(255) NULL DEFAULT NULL,
    PRIMARY KEY (`TransferID`, `TransactionID`),
    FOREIGN KEY (`FromAccountID`) REFERENCES `Accounts`(`AccountID`),
    FOREIGN KEY (`BeneficiaryID`) REFERENCES `Beneficiaries`(`BeneficiaryID`),
    FOREIGN KEY (`TransactionID`) REFERENCES `Transactions`(`TransactionID`)
) ENGINE = InnoDB;

-- Індекси додаються наприкінці
CREATE INDEX `idx_account_id_cards` ON `Cards` (`AccountID`);
CREATE INDEX `idx_customer_id_bankdetails` ON `BankDetails` (`CustomerID`);
CREATE INDEX `idx_card_id_bankdetails` ON `BankDetails` (`CardID`);
CREATE INDEX `idx_bank_details_beneficiaries` ON `Beneficiaries` (`BankDetailsID`);
CREATE INDEX `idx_account_id_customeraccounts` ON `CustomerAccounts` (`AccountID`);
CREATE INDEX `idx_beneficiary_id_transactions` ON `Transactions` (`BeneficiaryID`);
CREATE INDEX `idx_transaction_type_id_transactions` ON `Transactions` (`TransactionTypeID`);
CREATE INDEX `idx_from_account_transactions` ON `Transactions` (`FromAccountID`);
CREATE INDEX `idx_transaction_date_transactions` ON `Transactions` (`TransactionDate`);
CREATE INDEX `idx_from_account_transferhistory` ON `TransferHistory` (`FromAccountID`);
CREATE INDEX `idx_beneficiary_id_transferhistory` ON `TransferHistory` (`BeneficiaryID`);




INSERT INTO Customers (FirstName, LastName, Email, Phone)
VALUES
('John', 'Doe', 'johndoe@example.com', '1234567890'),
('Jane', 'Smith', 'janesmith@example.com', '0987654321'),
('Jon', 'Snow', 'jonsonw@example.com', '5678901234'),
('Emily', 'Brown', 'emilybrown@example.com', '4567890123'),
('Daniel', 'Kravchyk', 'danielkravchyk@example.com', '8765432109'),
('Natalia', 'Koval', 'natalik@example.com', '2345678901'),
('Aboba', 'Test', 'abtest@example.com', '3456789012'),
('Yuriy', 'Pavlenko', 'yuriy.pavlenko@gmail.com', '5556667777'),
('Random', 'Guy', 'randomguy@example.com', '6547891230'),
('Volodymyr', 'Lysenko', 'volodymyr.lysenko@gmail.com', '0987123456');

INSERT INTO Accounts (AccountNumber, Balance, Currency, AccountType)
VALUES
('123456789012', 1000.00, 'USD', 'Savings'),
('987654321098', 1500.50, 'USD', 'Checking'),
('123456789999', 500.00, 'USD', 'Savings'),
('555666777888', 2000.75, 'EUR', 'Savings'),
('111222333444', 2500.00, 'UAH', 'Savings'),
('444555666777', 3000.00, 'EUR', 'Checking'),
('888999000111', 3500.25, 'USD', 'Savings'),
('222333444555', 4000.50, 'USD', 'Checking'),
('666777888999', 4500.75, 'UAH', 'Savings'),
('999888777666', 5000.00, 'USD', 'Savings');

INSERT INTO Cards (AccountID, CardNumber, ExpiryDate, CardType)
VALUES
(1, '5555444433332222', '2026-07-15', 'Debit'),
(1, '1111222233334444', '2025-12-31', 'Credit'),
(2, '5555666677778888', '2026-01-31', 'Debit'),
(3, '9999000011112222', '2027-05-15', 'Credit'),
(4, '3333444455556666', '2024-08-20', 'Debit'),
(5, '7777888899990000', '2025-10-10', 'Credit'),
(6, '2222333344445555', '2026-02-28', 'Debit'),
(7, '6666777788889999', '2025-07-12', 'Credit'),
(8, '0000111122223333', '2026-11-22', 'Debit'),
(9, '8888999900001111', '2027-03-25', 'Credit'),
(10, '4444555566667777', '2024-09-30', 'Debit');

INSERT INTO BankDetails (CustomerID, BankName, BankCode, CardID)
VALUES
(1, 'PrivatBank', 'PBUAUA2X', 1),
(2, 'Oschadbank', 'OSCHUA2X', 2),
(3, 'Raiffeisen Bank Aval', 'AVALUAUK', 3),
(4, 'Ukreximbank', 'EXBSUAUX', 4),
(5, 'Alfa-Bank', 'ALFAUAUK', 5),
(6, 'PUMB', 'FUIBUA2X', 6),
(7, 'Kredobank', 'WUCBUA2X', 7),
(8, 'OTP Bank', 'OTPVUAUK', 8),
(9, 'UkrSibbank', 'KHABUA2K', 9),
(10, 'Ukrgasbank', 'UGASUAUX', 10);

INSERT INTO AccountBankDetails (AccountID, BankDetailsID)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO Beneficiaries (BeneficiaryName, BankDetailsID, BeneficiaryType)
VALUES
('Amazon', 1, 'Company'),
('Netflix', 2, 'Company'),
('John Doe', 3, 'Individual'),
('Rodyna Kovbaska', 4, 'Company'),
('Rozetka', 5, 'Company'),
('Nova Poshta', 6, 'Company'),
('Monobank', 7, 'Company'),
('Epicentr', 8, 'Company'),
('Silpo', 9, 'Company'),
('ATB', 10, 'Company');

INSERT INTO CustomerAccounts (CustomerID, AccountID)
VALUES
(1, 1),
(2, 2),
(2, 3),
(3, 4),
(4, 5),
(5, 6),
(6, 7),
(7, 8),
(8, 9),
(9, 10);

INSERT INTO TransactionTypes (TransactionTypeName)
VALUES
('Payment'),
('Transfer'),
('Refund'),
('Withdrawal'),
('Deposit'),
('Bill Payment'),
('Online Purchase'),
('Cashback'),
('Direct Debit'),
('Loan Repayment');

INSERT INTO Transactions (FromAccountID, BeneficiaryID, TransactionTypeID, Amount, Status)
VALUES
(1, 1, 1, 100.50, 'Completed'),
(2, 2, 2, 200.75, 'Pending'),
(3, 3, 3, 150.00, 'Failed'),
(4, 4, 4, 75.25, 'Completed'),
(5, 5, 5, 300.50, 'Completed'),
(6, 6, 6, 400.75, 'Completed'),
(7, 7, 7, 500.00, 'Pending'),
(8, 8, 8, 600.00, 'Completed'),
(9, 9, 9, 700.50, 'Completed'),
(10, 10, 10, 1200.00, 'Pending');

INSERT INTO TransferHistory (TransactionID, FromAccountID, BeneficiaryID, Amount, Description)
VALUES
(1, 1, 1, 100.50, 'Payment for order #123'),
(2, 2, 2, 200.75, 'Transfer to savings account'),
(3, 3, 3, 150.00, 'Refund for order #456'),
(4, 4, 4, 75.25, 'Withdrawal from ATM'),
(5, 5, 5, 300.50, 'Deposit from paycheck'),
(6, 6, 6, 400.75, 'Bill payment for electricity'),
(7, 7, 7, 500.00, 'Online purchase on Amazon'),
(8, 8, 8, 600.00, 'Cashback from purchase'),
(9, 9, 9, 700.50, 'Direct debit for insurance'),
(10, 10, 10, 1200.00, 'Loan repayment for car');