from flask import Blueprint, request, jsonify
from my_project.auth.service.account_service import AccountService

account_bp = Blueprint('accounts', __name__)

@account_bp.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = AccountService.get_all_accounts()
    return jsonify([account.to_dict() for account in accounts])

@account_bp.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = AccountService.get_account_by_id(id)
    if account:
        return jsonify(account.to_dict())
    return jsonify({'message': 'Account not found'}), 404

@account_bp.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    AccountService.create_account(data)
    return jsonify({'message': 'Account created successfully'}), 201

@account_bp.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    data = request.get_json()
    account = AccountService.update_account(id, data)
    if account:
        return jsonify({'message': 'Account updated successfully'})
    return jsonify({'message': 'Account not found'}), 404

@account_bp.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = AccountService.delete_account(id)
    if account:
        return jsonify({'message': 'Account deleted successfully'})
    return jsonify({'message': 'Account not found'}), 404
