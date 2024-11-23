from my_project.auth.DAO.models import Account
from extensions import db

class AccountService:
    @staticmethod
    def get_all_accounts():
        return Account.query.all()

    @staticmethod
    def get_account_by_id(account_id):
        return Account.query.get(account_id)

    @staticmethod
    def create_account(data):
        new_account = Account(
            CustomerID=data['CustomerID'],
            AccountNumber=data['AccountNumber'],
            Balance=data['Balance'],
            Currency=data['Currency'],
            AccountType=data['AccountType']
        )
        db.session.add(new_account)
        db.session.commit()
        return new_account

    @staticmethod
    def update_account(account_id, data):
        account = Account.query.get(account_id)
        if account:
            account.Balance = data['Balance']
            account.Currency = data['Currency']
            account.AccountType = data['AccountType']
            db.session.commit()
            return account
        return None

    @staticmethod
    def delete_account(account_id):
        account = Account.query.get(account_id)
        if account:
            db.session.delete(account)
            db.session.commit()
            return account
        return None

    @staticmethod
    def get_cards_by_account_id(account_id):
        account = Account.query.get(account_id)
        return account.cards if account else None
