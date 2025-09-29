from flask import Blueprint, request, jsonify
from my_project.auth.service.card_service import CardService

card_bp = Blueprint('cards', __name__)

@card_bp.route('/cards', methods=['GET'])
def get_cards():
    """
    Get all cards
    ---
    tags:
      - Cards
    responses:
      200:
        description: A list of all cards
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  card_number:
                    type: string
                  expiry_date:
                    type: string
                  account_id:
                    type: integer
    """
    cards = CardService.get_all_cards()
    return jsonify([card.to_dict() for card in cards])

@card_bp.route('/cards/<int:id>', methods=['GET'])
def get_card(id):
    """
    Get card by ID
    ---
    tags:
      - Cards
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
        description: Card ID
    responses:
      200:
        description: Card object
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                card_number:
                  type: string
                expiry_date:
                  type: string
                account_id:
                  type: integer
      404:
        description: Card not found
    """

    card = CardService.get_card_by_id(id)
    if card:
        return jsonify(card.to_dict())
    return jsonify({'message': 'Card not found'}), 404

@card_bp.route('/cards', methods=['POST'])
def create_card():
    """
    Create a new card
    ---
    tags:
      - Cards
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              card_number:
                type: string
              expiry_date:
                type: string
              account_id:
                type: integer
    responses:
      201:
        description: Card created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    CardService.create_card(data)
    return jsonify({'message': 'Card created successfully'}), 201

@card_bp.route('/cards/<int:id>', methods=['PUT'])
def update_card(id):
    """
    Update card by ID
    ---
    tags:
      - Cards
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
        description: Card ID
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              card_number:
                type: string
              expiry_date:
                type: string
              account_id:
                type: integer
    responses:
      200:
        description: Card updated successfully
      404:
        description: Card not found
    """
    data = request.get_json()
    card = CardService.update_card(id, data)
    if card:
        return jsonify({'message': 'Card updated successfully'})
    return jsonify({'message': 'Card not found'}), 404

@card_bp.route('/cards/<int:id>', methods=['DELETE'])
def delete_card(id):
    """
    Delete card by ID
    ---
    tags:
      - Cards
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
        description: Card ID
    responses:
      200:
        description: Card deleted successfully
      404:
        description: Card not found
    """
    card = CardService.delete_card(id)
    if card:
        return jsonify({'message': 'Card deleted successfully'})
    return jsonify({'message': 'Card not found'}), 404
