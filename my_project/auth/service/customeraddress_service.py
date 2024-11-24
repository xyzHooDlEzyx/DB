from sqlalchemy.sql import text
from extensions import db

class CustomerAddressService:
    @staticmethod
    def insert_customer_address(data):
        query = text("""
        CALL InsertCustomerAddress(
            :CustomerID,
            :Street,
            :City,
            :State,
            :PostalCode,
            :Country
        )
        """)
        db.session.execute(query, {
            'CustomerID': data['CustomerID'],
            'Street': data['Street'],
            'City': data['City'],
            'State': data.get('State'),
            'PostalCode': data['PostalCode'],
            'Country': data['Country']
        })
        db.session.commit()
