from my_project.auth.DAO.models import Transaction
from extensions import db

class TransactionService:
    @staticmethod
    def get_all_transactions():
        return Transaction.query.all()

    @staticmethod
    def get_transaction_by_id(transaction_id):
        return Transaction.query.get(transaction_id)

    @staticmethod
    def create_transaction(data):
        new_transaction = Transaction(
            FromAccountID=data['FromAccountID'],
            BeneficiaryID=data['BeneficiaryID'],
            TransactionTypeID=data['TransactionTypeID'],
            Amount=data['Amount'],
            Status=data['Status']
        )
        db.session.add(new_transaction)
        db.session.commit()
        return new_transaction

    @staticmethod
    def update_transaction(transaction_id, data):
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            transaction.Amount = data['Amount']
            transaction.Status = data['Status']
            db.session.commit()
            return transaction
        return None

    @staticmethod
    def delete_transaction(transaction_id):
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
            return transaction
        return None
