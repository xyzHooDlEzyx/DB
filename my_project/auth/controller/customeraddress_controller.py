from flask import Blueprint, request, jsonify
from my_project.auth.service.customeraddress_service import CustomerAddressService

customeraddress_bp = Blueprint('customeraddresses', __name__)

@customeraddress_bp.route('/customeraddresses', methods=['POST'])
def create_customer_address():
    """
    Insert a new customer address
    ---
    tags:
      - CustomerAddresses
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              CustomerID:
                type: integer
                example: 1
              Street:
                type: string
                example: "123 Main St"
              City:
                type: string
                example: "Kyiv"
              State:
                type: string
                example: "Kyiv Oblast"
              PostalCode:
                type: string
                example: "01001"
              Country:
                type: string
                example: "Ukraine"
    responses:
      201:
        description: Customer address inserted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Customer address inserted successfully
      400:
        description: Invalid input or error
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Error message
    """
    data = request.get_json()
    try:
        CustomerAddressService.insert_customer_address(data)
        return jsonify({'message': 'Customer address inserted successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400
