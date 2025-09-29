from flask import Blueprint, request, jsonify
from my_project.auth.service.bankdetail_service import BankDetailService

bankdetail_bp = Blueprint('bankdetails', __name__)

@bankdetail_bp.route('/bankdetails', methods=['GET'])
def get_bankdetails():
    """
    Get all bank details
    ---
    tags:
      - BankDetails
    responses:
      200:
        description: A list of bank details
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              bank_name:
                type: string
              branch:
                type: string
              swift_code:
                type: string
    """
    bankdetails = BankDetailService.get_all_bankdetails()
    return jsonify([bankdetail.to_dict() for bankdetail in bankdetails])

@bankdetail_bp.route('/bankdetails/<int:id>', methods=['GET'])
def get_bankdetail(id):
    """
    Get bank detail by ID
    ---
    tags:
      - BankDetails
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Bank detail ID
    responses:
      200:
        description: Bank detail object
      404:
        description: Bank detail not found
    """
    bankdetail = BankDetailService.get_bankdetail_by_id(id)
    if bankdetail:
        return jsonify(bankdetail.to_dict())
    return jsonify({'message': 'Bank detail not found'}), 404

@bankdetail_bp.route('/bankdetails', methods=['POST'])
def create_bankdetail():
    """
    Create a new bank detail
    ---
    tags:
      - BankDetails
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            bank_name:
              type: string
            branch:
              type: string
            swift_code:
              type: string
    responses:
      201:
        description: Bank detail created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    BankDetailService.create_bankdetail(data)
    return jsonify({'message': 'Bank detail created successfully'}), 201

@bankdetail_bp.route('/bankdetails/<int:id>', methods=['PUT'])
def update_bankdetail(id):
    """
    Update bank detail by ID
    ---
    tags:
      - BankDetails
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            bank_name:
              type: string
            branch:
              type: string
            swift_code:
              type: string
    responses:
      200:
        description: Bank detail updated successfully
      404:
        description: Bank detail not found
    """
    data = request.get_json()
    bankdetail = BankDetailService.update_bankdetail(id, data)
    if bankdetail:
        return jsonify({'message': 'Bank detail updated successfully'})
    return jsonify({'message': 'Bank detail not found'}), 404

@bankdetail_bp.route('/bankdetails/<int:id>', methods=['DELETE'])
def delete_bankdetail(id):
    """
    Delete bank detail by ID
    ---
    tags:
      - BankDetails
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Bank detail deleted successfully
      404:
        description: Bank detail not found
    """
    bankdetail = BankDetailService.delete_bankdetail(id)
    if bankdetail:
        return jsonify({'message': 'Bank detail deleted successfully'})
    return jsonify({'message': 'Bank detail not found'}), 404
