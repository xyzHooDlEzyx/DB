from extensions import db


class Customer(db.Model):
    __tablename__ = 'customers'

    CustomerID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100), nullable=False)
    LastName = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Phone = db.Column(db.String(15), unique=True, nullable=False)

    accounts = db.relationship('Account', backref='customer', lazy=True, cascade="all, delete")
    bank_details = db.relationship('BankDetail', backref='customer', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Customer {self.FirstName} {self.LastName}>"

    def to_dict(self):
        return {
            'CustomerID': self.CustomerID,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Email': self.Email,
            'Phone': self.Phone
        }


class Account(db.Model):
    __tablename__ = 'accounts'

    AccountID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customers.CustomerID'), nullable=False)
    AccountNumber = db.Column(db.String(20), unique=True, nullable=False)
    Balance = db.Column(db.Numeric(10, 2), nullable=False)
    Currency = db.Column(db.String(10), nullable=False)
    AccountType = db.Column(db.String(50), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    cards = db.relationship('Card', backref='account', lazy=True, cascade="all, delete")
    account_bank_details = db.relationship('AccountBankDetail', backref='account', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Account {self.AccountNumber}>"

    def to_dict(self):
        return {
            'AccountID': self.AccountID,
            'CustomerID': self.CustomerID,
            'AccountNumber': self.AccountNumber,
            'Balance': str(self.Balance),
            'Currency': self.Currency,
            'AccountType': self.AccountType,
            'CreatedAt': self.CreatedAt
        }


class Card(db.Model):
    __tablename__ = 'cards'

    CardID = db.Column(db.Integer, primary_key=True)
    AccountID = db.Column(db.Integer, db.ForeignKey('accounts.AccountID'), nullable=False)
    CardNumber = db.Column(db.String(16), unique=True, nullable=False)
    ExpiryDate = db.Column(db.Date, nullable=False)
    CardType = db.Column(db.String(50), nullable=False)

    bank_detail = db.relationship('BankDetail', backref='card', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Card {self.CardNumber}>"

    def to_dict(self):
        return {
            'CardID': self.CardID,
            'AccountID': self.AccountID,
            'CardNumber': self.CardNumber,
            'ExpiryDate': self.ExpiryDate,
            'CardType': self.CardType
        }


class BankDetail(db.Model):
    __tablename__ = 'bankdetails'

    BankDetailsID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customers.CustomerID'), nullable=False)
    BankName = db.Column(db.String(100), nullable=False)
    BankCode = db.Column(db.String(20), nullable=False)
    CardID = db.Column(db.Integer, db.ForeignKey('cards.CardID'), nullable=False)

    def __repr__(self):
        return f"<BankDetail {self.BankName}>"

    def to_dict(self):
        return {
            'BankDetailsID': self.BankDetailsID,
            'CustomerID': self.CustomerID,
            'BankName': self.BankName,
            'BankCode': self.BankCode,
            'CardID': self.CardID
        }


class AccountBankDetail(db.Model):
    __tablename__ = 'accountbankdetails'

    AccountID = db.Column(db.Integer, db.ForeignKey('accounts.AccountID'), primary_key=True, nullable=False)
    BankDetailsID = db.Column(db.Integer, db.ForeignKey('bankdetails.BankDetailsID'), primary_key=True, nullable=False)

    def __repr__(self):
        return f"<AccountBankDetail {self.AccountID} - {self.BankDetailsID}>"

    def to_dict(self):
        return {
            'AccountID': self.AccountID,
            'BankDetailsID': self.BankDetailsID
        }


class Beneficiary(db.Model):
    __tablename__ = 'beneficiaries'

    BeneficiaryID = db.Column(db.Integer, primary_key=True)
    BeneficiaryName = db.Column(db.String(255), nullable=False)
    BankDetailsID = db.Column(db.Integer, db.ForeignKey('bankdetails.BankDetailsID'), nullable=False)
    BeneficiaryType = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Beneficiary {self.BeneficiaryName}>"

    def to_dict(self):
        return {
            'BeneficiaryID': self.BeneficiaryID,
            'BeneficiaryName': self.BeneficiaryName,
            'BankDetailsID': self.BankDetailsID,
            'BeneficiaryType': self.BeneficiaryType
        }


class CustomerAccount(db.Model):
    __tablename__ = 'customeraccounts'

    CustomerID = db.Column(db.Integer, db.ForeignKey('customers.CustomerID'), primary_key=True, nullable=False)
    AccountID = db.Column(db.Integer, db.ForeignKey('accounts.AccountID'), primary_key=True, nullable=False)

    def __repr__(self):
        return f"<CustomerAccount {self.CustomerID} - {self.AccountID}>"

    def to_dict(self):
        return {
            'CustomerID': self.CustomerID,
            'AccountID': self.AccountID
        }


class TransactionType(db.Model):
    __tablename__ = 'transactiontypes'

    TransactionTypeID = db.Column(db.Integer, primary_key=True)
    TransactionTypeName = db.Column(db.String(100))

    def __repr__(self):
        return f"<TransactionType {self.TransactionTypeName}>"

    def to_dict(self):
        return {
            'TransactionTypeID': self.TransactionTypeID,
            'TransactionTypeName': self.TransactionTypeName
        }


class Transaction(db.Model):
    __tablename__ = 'transactions'

    TransactionID = db.Column(db.Integer, primary_key=True)
    FromAccountID = db.Column(db.Integer, db.ForeignKey('accounts.AccountID'), nullable=False)
    BeneficiaryID = db.Column(db.Integer, db.ForeignKey('beneficiaries.BeneficiaryID'), nullable=False)
    TransactionTypeID = db.Column(db.Integer, db.ForeignKey('transactiontypes.TransactionTypeID'), nullable=False)
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    TransactionDate = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    Status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Transaction {self.TransactionID} - {self.Status}>"

    def to_dict(self):
        return {
            'TransactionID': self.TransactionID,
            'FromAccountID': self.FromAccountID,
            'BeneficiaryID': self.BeneficiaryID,
            'TransactionTypeID': self.TransactionTypeID,
            'Amount': str(self.Amount),
            'TransactionDate': self.TransactionDate,
            'Status': self.Status
        }


class TransferHistory(db.Model):
    __tablename__ = 'transferhistory'

    TransferID = db.Column(db.Integer, primary_key=True)
    TransactionID = db.Column(db.Integer, db.ForeignKey('transactions.TransactionID'), nullable=False)
    FromAccountID = db.Column(db.Integer, db.ForeignKey('accounts.AccountID'), nullable=False)
    BeneficiaryID = db.Column(db.Integer, db.ForeignKey('beneficiaries.BeneficiaryID'), nullable=False)
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    TransferDate = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    Description = db.Column(db.String(255))

    def __repr__(self):
        return f"<TransferHistory {self.TransferID} - {self.Amount}>"

    def to_dict(self):
        return {
            'TransferID': self.TransferID,
            'TransactionID': self.TransactionID,
            'FromAccountID': self.FromAccountID,
            'BeneficiaryID': self.BeneficiaryID,
            'Amount': str(self.Amount),
            'TransferDate': self.TransferDate,
            'Description': self.Description
        }
