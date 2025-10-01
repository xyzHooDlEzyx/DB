from sqlalchemy.sql import text

from extensions import db

class CustomerAccountService:
    @staticmethod
    def insert_customer_account(data):
        query = text("""
        CALL InsertCustomerAccount(
            :FirstName,
            :LastName,
            :AccountNumber
        )
        """)
        try:
            db.session.execute(query, {
                'FirstName': data['FirstName'],
                'LastName': data['LastName'],
                'AccountNumber': data['AccountNumber']
            })
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
