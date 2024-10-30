from flask import Blueprint, request, jsonify
from my_project.auth.service.bankdetail_service import BankDetailService

bankdetail_bp = Blueprint('bankdetails', __name__)

@bankdetail_bp.route('/bankdetails', methods=['GET'])
def get_bankdetails():
    bankdetails = BankDetailService.get_all_bankdetails()
    return jsonify([bankdetail.to_dict() for bankdetail in bankdetails])

@bankdetail_bp.route('/bankdetails/<int:id>', methods=['GET'])
def get_bankdetail(id):
    bankdetail = BankDetailService.get_bankdetail_by_id(id)
    if bankdetail:
        return jsonify(bankdetail.to_dict())
    return jsonify({'message': 'Bank detail not found'}), 404

@bankdetail_bp.route('/bankdetails', methods=['POST'])
def create_bankdetail():
    data = request.get_json()
    BankDetailService.create_bankdetail(data)
    return jsonify({'message': 'Bank detail created successfully'}), 201

@bankdetail_bp.route('/bankdetails/<int:id>', methods=['PUT'])
def update_bankdetail(id):
    data = request.get_json()
    bankdetail = BankDetailService.update_bankdetail(id, data)
    if bankdetail:
        return jsonify({'message': 'Bank detail updated successfully'})
    return jsonify({'message': 'Bank detail not found'}), 404

@bankdetail_bp.route('/bankdetails/<int:id>', methods=['DELETE'])
def delete_bankdetail(id):
    bankdetail = BankDetailService.delete_bankdetail(id)
    if bankdetail:
        return jsonify({'message': 'Bank detail deleted successfully'})
    return jsonify({'message': 'Bank detail not found'}), 404
