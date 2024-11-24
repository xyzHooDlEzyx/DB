from my_project.auth.DAO.models import Customer
from sqlalchemy.sql import text
from extensions import db

class CustomerService:
    @staticmethod
    def get_all_customers():
        return Customer.query.all()

    @staticmethod
    def get_customer_by_id(customer_id):
        return Customer.query.get(customer_id)

    @staticmethod
    def create_customer(data):
        new_customer = Customer(
            FirstName=data['FirstName'],
            LastName=data['LastName'],
            Email=data['Email'],
            Phone=data['Phone']
        )
        db.session.add(new_customer)
        db.session.commit()
        return new_customer

    @staticmethod
    def update_customer(customer_id, data):
        customer = Customer.query.get(customer_id)
        if customer:
            customer.FirstName = data['FirstName']
            customer.LastName = data['LastName']
            customer.Email = data['Email']
            customer.Phone = data['Phone']
            db.session.commit()
            return customer
        return None

    @staticmethod
    def delete_customer(customer_id):
        customer = Customer.query.get(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return customer
        return None


    @staticmethod
    def insert_bulk_customers(base_name, start_number):
        query = text("""
        CALL InsertNonameRows(:base_name, :start_number, 'customers')
        """)
        db.session.execute(query, {
            'base_name': base_name,
            'start_number': start_number
        })
        db.session.commit()
