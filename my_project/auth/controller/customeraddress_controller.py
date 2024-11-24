from flask import Blueprint, request, jsonify
from my_project.auth.service.customeraddress_service import CustomerAddressService

customeraddress_bp = Blueprint('customeraddresses', __name__)

@customeraddress_bp.route('/customeraddresses', methods=['POST'])
def create_customer_address():
    data = request.get_json()
    try:
        CustomerAddressService.insert_customer_address(data)
        return jsonify({'message': 'Customer address inserted successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
