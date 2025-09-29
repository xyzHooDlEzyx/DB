from flask import Blueprint, request, jsonify
from my_project.auth.service.transaction_service import TransactionService

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """
    Get all transactions
    ---
    tags:
      - Transactions
    responses:
      200:
        description: List of all transactions
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    transactions = TransactionService.get_all_transactions()
    return jsonify([transaction.to_dict() for transaction in transactions])

@transaction_bp.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    """
    Get a transaction by ID
    ---
    tags:
      - Transactions
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: ID of the transaction
    responses:
      200:
        description: Transaction details
        content:
          application/json:
            schema:
              type: object
      404:
        description: Transaction not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Transaction not found
    """
    transaction = TransactionService.get_transaction_by_id(id)
    if transaction:
        return jsonify(transaction.to_dict())
    return jsonify({'message': 'Transaction not found'}), 404

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    from flask import Blueprint, request, jsonify
from my_project.auth.service.transaction_service import TransactionService

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """
    Get all transactions
    ---
    tags:
      - Transactions
    responses:
      200:
        description: List of all transactions
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    transactions = TransactionService.get_all_transactions()
    return jsonify([transaction.to_dict() for transaction in transactions])


@transaction_bp.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    """
    Get a transaction by ID
    ---
    tags:
      - Transactions
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: ID of the transaction
    responses:
      200:
        description: Transaction details
        content:
          application/json:
            schema:
              type: object
      404:
        description: Transaction not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Transaction not found
    """
    transaction = TransactionService.get_transaction_by_id(id)
    if transaction:
        return jsonify(transaction.to_dict())
    return jsonify({'message': 'Transaction not found'}), 404


@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """
    Create a new transaction
    ---
    tags:
      - Transactions
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            example:
              FromAccountID: 1
              BeneficiaryID: 2
              TransactionTypeID: 1
              Amount: 100.50
              Status: Completed
    responses:
      201:
        description: Transaction created successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Transaction created successfully
    """
    data = request.get_json()
    TransactionService.create_transaction(data)
    return jsonify({'message': 'Transaction created successfully'}), 201

@transaction_bp.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    """
    Update an existing transaction
    ---
    tags:
      - Transactions
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: ID of the transaction to update
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            example:
              Amount: 200.00
              Status: Pending
    responses:
      200:
        description: Transaction updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Transaction updated successfully
      404:
        description: Transaction not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Transaction not found
    """
    data = request.get_json()
    transaction = TransactionService.update_transaction(id, data)
    if transaction:
        return jsonify({'message': 'Transaction updated successfully'})
    return jsonify({'message': 'Transaction not found'}), 404

@transaction_bp.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    """
    Delete a transaction by ID
    ---
    tags:
      - Transactions
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: ID of the transaction to delete
    responses:
      200:
        description: Transaction deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Transaction deleted successfully
      404:
        description: Transaction not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Transaction not found
    """
    transaction = TransactionService.delete_transaction(id)
    if transaction:
        return jsonify({'message': 'Transaction deleted successfully'})
    return jsonify({'message': 'Transaction not found'}), 404
