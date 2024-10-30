from flask import Blueprint, request, jsonify
from my_project.auth.service.transaction_service import TransactionService

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = TransactionService.get_all_transactions()
    return jsonify([transaction.to_dict() for transaction in transactions])

@transaction_bp.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = TransactionService.get_transaction_by_id(id)
    if transaction:
        return jsonify(transaction.to_dict())
    return jsonify({'message': 'Transaction not found'}), 404

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    TransactionService.create_transaction(data)
    return jsonify({'message': 'Transaction created successfully'}), 201

@transaction_bp.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    data = request.get_json()
    transaction = TransactionService.update_transaction(id, data)
    if transaction:
        return jsonify({'message': 'Transaction updated successfully'})
    return jsonify({'message': 'Transaction not found'}), 404

@transaction_bp.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = TransactionService.delete_transaction(id)
    if transaction:
        return jsonify({'message': 'Transaction deleted successfully'})
    return jsonify({'message': 'Transaction not found'}), 404
