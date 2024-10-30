from flask import Blueprint, request, jsonify
from my_project.auth.service.card_service import CardService

card_bp = Blueprint('cards', __name__)

@card_bp.route('/cards', methods=['GET'])
def get_cards():
    cards = CardService.get_all_cards()
    return jsonify([card.to_dict() for card in cards])

@card_bp.route('/cards/<int:id>', methods=['GET'])
def get_card(id):
    card = CardService.get_card_by_id(id)
    if card:
        return jsonify(card.to_dict())
    return jsonify({'message': 'Card not found'}), 404

@card_bp.route('/cards', methods=['POST'])
def create_card():
    data = request.get_json()
    CardService.create_card(data)
    return jsonify({'message': 'Card created successfully'}), 201

@card_bp.route('/cards/<int:id>', methods=['PUT'])
def update_card(id):
    data = request.get_json()
    card = CardService.update_card(id, data)
    if card:
        return jsonify({'message': 'Card updated successfully'})
    return jsonify({'message': 'Card not found'}), 404

@card_bp.route('/cards/<int:id>', methods=['DELETE'])
def delete_card(id):
    card = CardService.delete_card(id)
    if card:
        return jsonify({'message': 'Card deleted successfully'})
    return jsonify({'message': 'Card not found'}), 404
