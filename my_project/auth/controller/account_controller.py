from flask import Blueprint, request, jsonify
from my_project.auth.DAO.models import Account
from my_project.auth.service.account_service import AccountService

account_bp = Blueprint('accounts', __name__)

@account_bp.route('/accounts', methods=['GET'])
def get_accounts():
    """
    Get all accounts
    ---
    tags:
      - Accounts
    responses:
      200:
        description: A list of accounts
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  AccountID:
                    type: integer
                  Balance:
                    type: number
                  CustomerID:
                    type: integer
    """
    accounts = AccountService.get_all_accounts()
    return jsonify([account.to_dict() for account in accounts])

@account_bp.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    """
    Get account by ID
    ---
    tags:
      - Accounts
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
        description: Account ID
    responses:
      200:
        description: A single account
        content:
          application/json:
            schema:
              type: object
              properties:
                AccountID:
                  type: integer
                Balance:
                  type: number
                CustomerID:
                  type: integer
      404:
        description: Account not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    account = AccountService.get_account_by_id(id)
    if account:
        return jsonify(account.to_dict())
    return jsonify({'message': 'Account not found'}), 404

@account_bp.route('/accounts', methods=['POST'])
def create_account():
    """
    Create new account
    ---
    tags:
      - Accounts
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              Balance:
                type: number
              CustomerID:
                type: integer
              Currency:
                type: string
                nullable: true
    responses:
      201:
        description: Account created successfully
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
    AccountService.create_account(data)
    return jsonify({'message': 'Account created successfully'}), 201

@account_bp.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    """
    Update account by ID
    ---
    tags:
      - Accounts
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
        description: Account ID
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              Balance:
                type: number
              CustomerID:
                type: integer
              Status:
                type: string
                nullable: true
    responses:
      200:
        description: Account updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Account not found
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    data = request.get_json()
    account = AccountService.update_account(id, data)
    if account:
        return jsonify({'message': 'Account updated successfully'})
    return jsonify({'message': 'Account not found'}), 404

@account_bp.route('/accounts/<int:id>/cards', methods=['GET'])
def get_account_cards(id):
    """
    Get all cards by account ID
    ---
    tags:
      - Accounts
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
        description: Account ID
    responses:
      200:
        description: List of cards for the account
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  CardID:
                    type: integer
                  CardNumber:
                    type: string
                  ExpiryDate:
                    type: string
      404:
        description: No cards found or account does not exist
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    cards = AccountService.get_cards_by_account_id(id)
    if cards is not None:
        return jsonify([card.to_dict() for card in cards])
    return jsonify({'message': 'No cards found for this account or account does not exist'}), 404
