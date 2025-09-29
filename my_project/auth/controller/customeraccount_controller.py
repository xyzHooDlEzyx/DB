from flask import Blueprint, request, jsonify
from my_project.auth.service.customeraccount_service import CustomerAccountService

customeraccount_bp = Blueprint('customeraccounts', __name__)

@customeraccount_bp.route('/customeraccounts', methods=['POST'])
def create_customer_account():
    """
    Link a customer to an account
    ---
    tags:
      - CustomerAccounts
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            CustomerID:
              type: integer
              example: 1
            AccountID:
              type: integer
              example: 101
    responses:
      201:
        description: Customer account linked successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Customer account linked successfully
      400:
        description: Invalid input or error
        schema:
          type: object
          properties:
            message:
              type: string
              example: Error message
    """
    data = request.get_json()
    try:
        CustomerAccountService.insert_customer_account(data)
        return jsonify({'message': 'Customer account linked successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
