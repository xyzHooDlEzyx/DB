from flask import Blueprint, request, jsonify
from my_project.auth.DAO.models import Customer, Account, CustomerAccount
from my_project.auth.service.customer_service import CustomerService

customer_bp = Blueprint('customers', __name__)

@customer_bp.route('/customers', methods=['GET'])
def get_customers():
    """
    Get all customers
    ---
    tags:
      - Customers
    responses:
      200:
        description: List of customers
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  CustomerID:
                    type: integer
                  FirstName:
                    type: string
                  LastName:
                    type: string
                  Email:
                    type: string
                  Phone:
                    type: string
    """
    customers = CustomerService.get_all_customers()
    return jsonify([customer.to_dict() for customer in customers])

@customer_bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    """
    Get customer by ID
    ---
    tags:
      - Customers
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
        description: ID of the customer
    responses:
      200:
        description: Customer data
        content:
          application/json:
            schema:
              type: object
              properties:
                CustomerID:
                  type: integer
                FirstName:
                  type: string
                LastName:
                  type: string
                Email:
                  type: string
                Phone:
                  type: string
      404:
        description: Customer not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    customer = CustomerService.get_customer_by_id(id)
    if customer:
        return jsonify(customer.to_dict())
    return jsonify({'message': 'Customer not found'}), 404

@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    """
    Create a new customer
    ---
    tags:
      - Customers
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              FirstName:
                type: string
              LastName:
                type: string
              Email:
                type: string
              Phone:
                type: string
    responses:
      201:
        description: Customer created successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      400:
        description: Invalid input
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    data = request.get_json()
    CustomerService.create_customer(data)
    return jsonify({'message': 'Customer created successfully'}), 201

@customer_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    """
    Update a customer
    ---
    tags:
      - Customers
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              FirstName:
                type: string
              LastName:
                type: string
              Email:
                type: string
              Phone:
                type: string
    responses:
      200:
        description: Customer updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Customer not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    data = request.get_json()
    customer = CustomerService.update_customer(id, data)
    if customer:
        return jsonify({'message': 'Customer updated successfully'})
    return jsonify({'message': 'Customer not found'}), 404

@customer_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    """
    Delete a customer
    ---
    tags:
      - Customers
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Customer deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Customer not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    customer = CustomerService.delete_customer(id)
    if customer:
        return jsonify({'message': 'Customer deleted successfully'})
    return jsonify({'message': 'Customer not found'}), 404

@customer_bp.route('/customers/<int:id>/accounts', methods=['GET'])
def get_customer_accounts(id):
    """
    Get all accounts for a specific customer
    ---
    tags:
      - Customers
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: List of accounts for the customer
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  AccountID:
                    type: integer
                  AccountNumber:
                    type: string
                  Balance:
                    type: string
                  Currency:
                    type: string
                  AccountType:
                    type: string
                  CreatedAt:
                    type: string
      404:
        description: Customer not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    customer = CustomerService.get_customer_by_id(id)
    if customer:
        accounts = Account.query.filter_by(CustomerID=id).all()
        return jsonify([account.to_dict() for account in accounts])
    return jsonify({'message': 'Customer not found'}), 404


@customer_bp.route('/customers_with_accounts', methods=['GET'])
def get_customers_with_accounts():
    """
    Get all customers with their accounts
    ---
    tags:
      - Customers
    responses:
      200:
        description: List of customers with accounts
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  CustomerID:
                    type: integer
                  FirstName:
                    type: string
                  LastName:
                    type: string
                  Email:
                    type: string
                  Phone:
                    type: string
                  accounts:
                    type: array
                    items:
                      type: object
                      properties:
                        AccountID:
                          type: integer
                        AccountNumber:
                          type: string
                        Balance:
                          type: string
                        Currency:
                          type: string
                        AccountType:
                          type: string
                        CreatedAt:
                          type: string
    """
    customers = Customer.query.all()
    result = []

    for customer in customers:
        customer_data = customer.to_dict()
        accounts = Account.query.join(CustomerAccount, Account.AccountID == CustomerAccount.AccountID) \
            .filter(CustomerAccount.CustomerID == customer.CustomerID).all()

        customer_data['accounts'] = [account.to_dict() for account in accounts]
        result.append(customer_data)

    return jsonify(result)

@customer_bp.route('/customers/bulk', methods=['POST'])
def insert_bulk_customers():
    """
    Insert bulk customers
    ---
    tags:
      - Customers
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              base_name:
                type: string
              start_number:
                type: integer
    responses:
      201:
        description: Bulk customers inserted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      400:
        description: Invalid input or error
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    try:
        data = request.get_json()
        base_name = data['base_name']
        start_number = data['start_number']

        CustomerService.insert_bulk_customers(base_name, start_number)
        return jsonify({'message': 'Bulk customers inserted successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
