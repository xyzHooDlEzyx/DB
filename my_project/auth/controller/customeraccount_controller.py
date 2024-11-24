from flask import Blueprint, request, jsonify
from my_project.auth.service.customeraccount_service import CustomerAccountService

customeraccount_bp = Blueprint('customeraccounts', __name__)

@customeraccount_bp.route('/customeraccounts', methods=['POST'])
def create_customer_account():
    data = request.get_json()
    try:
        CustomerAccountService.insert_customer_account(data)
        return jsonify({'message': 'Customer account linked successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
